import logging

from django import http
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail, send_mass_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils import six
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
from django.views import generic

from oscar.apps.shipping.methods import NoShippingRequired
from oscar.core.loading import get_class, get_classes, get_model

from oscar.apps.checkout import signals
from paypalrestsdk import Payment

from kamper_paypal.utils import create_payment

Selector = get_class('partner.strategy', 'Selector')
ShippingAddressForm, ShippingMethodForm, GatewayForm \
    = get_classes('checkout.forms', ['ShippingAddressForm', 'ShippingMethodForm', 'GatewayForm'])
OrderCreator = get_class('order.utils', 'OrderCreator')
UserAddressForm = get_class('address.forms', 'UserAddressForm')
Repository = get_class('shipping.repository', 'Repository')
AccountAuthView = get_class('customer.views', 'AccountAuthView')
RedirectRequired, UnableToTakePayment, PaymentError \
    = get_classes('payment.exceptions', ['RedirectRequired',
                                         'UnableToTakePayment',
                                         'PaymentError'])
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
Order = get_model('order', 'Order')
ShippingAddress = get_model('order', 'ShippingAddress')
CommunicationEvent = get_model('order', 'CommunicationEvent')
PaymentEventType = get_model('order', 'PaymentEventType')
PaymentEvent = get_model('order', 'PaymentEvent')
UserAddress = get_model('address', 'UserAddress')
Basket = get_model('basket', 'Basket')
Email = get_model('customer', 'Email')
Country = get_model('address', 'Country')
CommunicationEventType = get_model('customer', 'CommunicationEventType')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')

# Standard logger for checkout events
logger = logging.getLogger('oscar.checkout')


# INDEX -> shipping-address ->
class IndexView(CheckoutSessionMixin, generic.FormView):
    """
    First page of the checkout.  We prompt user to either sign in, or
    to proceed as a guest (where we still collect their email address).
    """
    template_name = 'checkout/gateway.html'
    form_class = GatewayForm
    success_url = reverse_lazy('checkout:shipping-address')
    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid']

    def get(self, request, *args, **kwargs):
        # We redirect immediately to shipping address stage if the user is
        # signed in.
        if request.user.is_authenticated():
            # We raise a signal to indicate that the user has entered the
            # checkout process so analytics tools can track this event.
            signals.start_checkout.send_robust(
                    sender=self, request=request)
            return self.get_success_response()
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(IndexView, self).get_form_kwargs()
        email = self.checkout_session.get_guest_email()
        if email:
            kwargs['initial'] = {
                'username': email,
            }
        return kwargs

    def form_valid(self, form):
        if form.is_guest_checkout() or form.is_new_account_checkout():
            email = form.cleaned_data['username']
            self.checkout_session.set_guest_email(email)

            # We raise a signal to indicate that the user has entered the
            # checkout process by specifying an email address.
            signals.start_checkout.send_robust(
                    sender=self, request=self.request, email=email)

            if form.is_new_account_checkout():
                messages.info(
                        self.request,
                        _("Create your account and then you will be redirected "
                          "back to the checkout process"))
                self.success_url = "%s?next=%s&email=%s" % (
                    reverse('customer:register'),
                    reverse('checkout:shipping-address'),
                    urlquote(email)
                )
        else:
            user = form.get_user()
            login(self.request, user)

            # We raise a signal to indicate that the user has entered the
            # checkout process.
            signals.start_checkout.send_robust(
                    sender=self, request=self.request)

        return redirect(self.get_success_url())

    def get_success_response(self):
        return redirect(self.get_success_url())


# ================
# SHIPPING ADDRESS
# ================


#
class ShippingAddressView(CheckoutSessionMixin, generic.FormView):
    """
    Determine the shipping address for the order.

    The default behaviour is to display a list of addresses from the users's
    address book, from which the user can choose one to be their shipping
    address.  They can add/edit/delete these USER addresses.  This address will
    be automatically converted into a SHIPPING address when the user checks
    out.

    Alternatively, the user can enter a SHIPPING address directly which will be
    saved in the session and later saved as ShippingAddress model when the
    order is successfully submitted.
    """
    template_name = 'checkout/shipping_address.html'

    # ShippingAddressForm 수정 필요
    form_class = ShippingAddressForm
    success_url = reverse_lazy('checkout:shipping-method')
    pre_conditions = ['check_basket_is_not_empty',
                      'check_basket_is_valid',
                      'check_user_email_is_captured']
    skip_conditions = ['skip_unless_basket_requires_shipping']

    def get_initial(self):
        # shipping-address가 새로 만들어지면 실행한다.
        initial = self.checkout_session.new_shipping_address_fields()
        if initial:
            initial = initial.copy()
            # Convert the primary key stored in the session into a Country
            # instance
            try:
                initial['country'] = Country.objects.get(
                        iso_3166_1_a2=initial.pop('country_id'))
            except Country.DoesNotExist:
                # Hmm, the previously selected Country no longer exists. We
                # ignore this.
                pass
        return initial

    def get_context_data(self, **kwargs):
        ctx = super(ShippingAddressView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            # Look up address book data
            ctx['addresses'] = self.get_available_addresses()
        return ctx

    def get_available_addresses(self):
        # Include only addresses where the country is flagged as valid for
        # shipping. Also, use ordering to ensure the default address comes
        # first.
        return self.request.user.addresses.filter(
                country__is_shipping_country=True).order_by(
                '-is_default_for_shipping')

    def post(self, request, *args, **kwargs):
        # Check if a shipping address was selected directly (eg no form was
        # filled in)
        # 새로운 form이 만들어지면 실행된다.

        # 저장되어 있는 것 선택시 (address_id, action='ship_to')
        if self.request.user.is_authenticated() and 'address_id' in self.request.POST:
            address = UserAddress._default_manager.get(
                    pk=self.request.POST['address_id'], user=self.request.user)
            action = self.request.POST.get('action', None)

            # 저장되어 있는 것 선택시 (address_id, action='ship_to')
            if action == 'ship_to':
                # User has selected a previous address to ship to
                self.checkout_session.ship_to_user_address(address)
                return redirect(self.get_success_url())
            else:
                return http.HttpResponseBadRequest()

        # shipping address가 새로 만들면 else 실행
        else:
            return super(ShippingAddressView, self).post(
                    request, *args, **kwargs)

    def form_valid(self, form):
        # Store the address details in the session and redirect to next step
        # 캠퍼
        # shipping-address가 새로 만들어지면 session에 저장후 redirect 한다.
        address_fields = dict(
                (k, v) for (k, v) in form.instance.__dict__.items()
                if not k.startswith('_'))

        self.checkout_session.ship_to_new_address(address_fields)
        return super(ShippingAddressView, self).form_valid(form)


class UserAddressUpdateView(CheckoutSessionMixin, generic.UpdateView):
    """
    Update a user address
    """
    template_name = 'checkout/user_address_form.html'
    form_class = UserAddressForm
    success_url = reverse_lazy('checkout:shipping-address')

    def get_queryset(self):
        return self.request.user.addresses.all()

    def get_form_kwargs(self):
        kwargs = super(UserAddressUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.info(self.request, _("Address saved"))
        return super(UserAddressUpdateView, self).get_success_url()


class UserAddressDeleteView(CheckoutSessionMixin, generic.DeleteView):
    """
    Delete an address from a user's address book.
    """
    template_name = 'checkout/user_address_delete.html'
    success_url = reverse_lazy('checkout:shipping-address')

    def get_queryset(self):
        return self.request.user.addresses.all()

    def get_success_url(self):
        messages.info(self.request, _("Address deleted"))
        return super(UserAddressDeleteView, self).get_success_url()


# ===============
# Shipping method
# ===============


class ShippingMethodView(CheckoutSessionMixin, generic.FormView):
    """
    View for allowing a user to choose a shipping method.

    Shipping methods are largely domain-specific and so this view
    will commonly need to be subclassed and customised.

    The default behaviour is to load all the available shipping methods
    using the shipping Repository.  If there is only 1, then it is
    automatically selected.  Otherwise, a page is rendered where
    the user can choose the appropriate one.
    """
    template_name = 'checkout/shipping_methods.html'
    form_class = ShippingMethodForm
    pre_conditions = ['check_basket_is_not_empty',
                      'check_basket_is_valid',
                      'check_user_email_is_captured']

    def post(self, request, *args, **kwargs):
        self._methods = self.get_available_shipping_methods()
        return super(ShippingMethodView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # These pre-conditions can't easily be factored out into the normal
        # pre-conditions as they do more than run a test and then raise an
        # exception on failure.


        # Check that shipping is required at all
        # 제품 모두 shipping이 필요 없으면 실행
        if not request.basket.is_shipping_required():
            # No shipping required - we store a special code to indicate so.
            self.checkout_session.use_shipping_method(
                    NoShippingRequired().code)
            return self.get_success_response()

        # Check that shipping address has been completed
        # shipping address가 선택 되지 않았다면
        if not self.checkout_session.is_shipping_address_set():
            messages.error(request, _("Please choose a shipping address"))
            return redirect('checkout:shipping-address')

        # Save shipping methods as instance var as we need them both here
        # and when setting the context vars.
        self._methods = self.get_available_shipping_methods()
        # 메소드가 없으면
        if len(self._methods) == 0:
            # No shipping methods available for given address
            messages.warning(request, _(
                    "Shipping is unavailable for your chosen address - please "
                    "choose another"))
            return redirect('checkout:shipping-address')
        # 메소드가 하나밖에 없으면
        elif len(self._methods) == 1:
            # Only one shipping method - set this and redirect onto the next
            # step
            self.checkout_session.use_shipping_method(self._methods[0].code)
            return self.get_success_response()

        # Must be more than one available shipping method, we present them to
        # the user to make a choice.
        return super(ShippingMethodView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(ShippingMethodView, self).get_context_data(**kwargs)
        kwargs['methods'] = self._methods
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(ShippingMethodView, self).get_form_kwargs()
        kwargs['methods'] = self._methods
        return kwargs

    def get_available_shipping_methods(self):
        """
        Returns all applicable shipping method objects for a given basket.
        """
        # Shipping methods can depend on the user, the contents of the basket
        # and the shipping address (so we pass all these things to the
        # repository).  I haven't come across a scenario that doesn't fit this
        # system.
        return Repository().get_shipping_methods(
                basket=self.request.basket, user=self.request.user,
                shipping_addr=self.get_shipping_address(self.request.basket),
                request=self.request)

    def form_valid(self, form):
        # Save the code for the chosen shipping method in the session
        # and continue to the next step.
        self.checkout_session.use_shipping_method(form.cleaned_data['method_code'])
        return self.get_success_response()

    def form_invalid(self, form):
        messages.error(self.request, _("Your submitted shipping method is not"
                                       " permitted"))
        return super(ShippingMethodView, self).form_invalid(form)

    def get_success_response(self):
        return redirect('checkout:payment-method')


# ==============
# Payment method
# ==============


class PaymentMethodView(CheckoutSessionMixin, generic.TemplateView):
    """
    View for a user to choose which payment method(s) they want to use.

    This would include setting allocations if payment is to be split
    between multiple sources.
    It's not the place for entering sensitive details
    like bankcard numbers though - that belongs on the payment details view.

    Kamper 수정!!!
    """
    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured']
    skip_conditions = ['skip_unless_payment_is_required']

    def get(self, request, *args, **kwargs):
        """
        카드결제 자동이체 무통장 입금등을 적는 곳이다.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # By default we redirect straight onto the payment details view. Shops
        # that require a choice of payment method may want to override this
        # method to implement their specific logic.
        return self.get_success_response()

    def get_success_response(self):
        return redirect('checkout:payment-details')


# ================
# Order submission
# ================


class PaymentDetailsView(OrderPlacementMixin, generic.TemplateView):
    """
    For taking the details of payment and creating the order.

    This view class is used by two separate URLs: 'payment-details' and
    'preview'. The `preview` class attribute is used to distinguish which is
    being used. Chronologically, `payment-details` (preview=False) comes before
    `preview` (preview=True).

    If sensitive details are required (eg a bankcard), then the payment details
    view should submit to the preview URL and a custom implementation of
    `validate_payment_submission` should be provided.

    - If the form data is valid, then the preview template can be rendered with
      the payment-details forms re-rendered within a hidden div so they can be
      re-submitted when the 'place order' button is clicked. This avoids having
      to write sensitive data to disk anywhere during the process. This can be
      done by calling `render_preview`, passing in the extra template context
      vars.

    - If the form data is invalid, then the payment details templates needs to
      be re-rendered with the relevant error messages. This can be done by
      calling `render_payment_details`, passing in the form instances to pass
      to the templates.

    The class is deliberately split into fine-grained methods, responsible for
    only one thing.  This is to make it easier to subclass and override just
    one component of functionality.

    All projects will need to subclass and customise this class as no payment
    is taken by default.

    KAMPER:
        TemplateView FlowChart:
            dispatch()  -> OrderPlacementMixin.dispatch()
            http_method_not_allowed() ->
            get_context_data() ->
    """

    # 최초 실행
    template_name = 'checkout/payment_details.html'

    template_name_preview = 'checkout/preview.html'

    # These conditions are extended at runtime depending on whether we are in
    # 'preview' mode or not.
    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured']

    # If preview=True, then we render a preview template that shows all order
    # details ready for submission.
    preview = False

    def get_pre_conditions(self, request):
        if self.preview:
            # The preview view needs to ensure payment information has been
            # correctly captured.

            # check_payment_data_is_captured
            return self.pre_conditions + ['check_payment_data_is_captured']
        return super(PaymentDetailsView, self).get_pre_conditions(request)

    def get_skip_conditions(self, request):
        if not self.preview:
            # Payment details should only be collected if necessary
            return ['skip_unless_payment_is_required']
        return super(PaymentDetailsView, self).get_skip_conditions(request)

    def post(self, request, *args, **kwargs):
        """
        preview에서 order 주문 했을 때
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # Posting to payment-details isn't the right thing to do.  Form
        # submissions should use the preview URL.
        if not self.preview:
            return http.HttpResponseBadRequest()

        # We use a custom parameter to indicate if this is an attempt to place
        # an order (normally from the preview page).  Without this, we assume a
        # payment form is being submitted from the payment details view. In
        # this case, the form needs validating and the order preview shown.

        request_action = request.POST.get('action', '')
        # KAMPER: Preview에서 주문을 눌렀다면
        if request_action == 'place_order':
            return self.handle_place_order_submission(request)

        # KAMPER payment_detail을 골랏다면
        if request_action == 'Alipay' or request_action == 'Paypal':
            return self.handle_payment_details_submission(request)
        else:
            return http.HttpResponseBadRequest()

    def handle_place_order_submission(self, request):
        """
        preview에서 order 주문 했을 때2

        Handle a request to place an order.

        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.

        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """
        return self.submit(**self.build_submission())

    def handle_payment_details_submission(self, request):
        """
        preview로 보내면서 동시에 결제방법 paypal, alipay form 전달

        Handle a request to submit payment details.

        This method will need to be overridden by projects that require forms
        to be submitted on the payment details view.  The new version of this
        method should validate the submitted form data and:

        - If the form data is valid, show the preview view with the forms
          re-rendered in the page
        - If the form data is invalid, show the payment details view with
          the form errors showing.

        """
        payment_detail_method = request.POST.get('action', '')
        # 잘못된 요청이 왔을 때
        if payment_detail_method != 'Paypal' and payment_detail_method != 'Alipay':
            return http.HttpResponseBadRequest()

        # KAMPER 만든 함수.
        self.checkout_session.set_payment_detail_method(payment_detail_method)

        # No form data to validate by default, so we simply render the preview
        # page.  If validating form data and it's invalid, then call the
        # render_payment_details view.
        return self.render_preview(request)

    def render_preview(self, request, **kwargs):
        """
        Kamper 수정.!

        Show a preview of the order.

        If sensitive data was submitted on the payment details page, you will
        need to pass it back to the view here so it can be stored in hidden
        form inputs.  This avoids ever writing the sensitive data to disk.
        """
        self.preview = True
        ctx = self.get_context_data(**kwargs)

        # template에서 불러올 수 있도록 추가
        ctx['payment_detail_method'] = self.checkout_session.get_payment_detail_method()

        # for line in request.basket:
        #     print(line)
        #     print(type(line))
        # for total in ctx['basket']:
        #     print(total)
        # ctx['order_total']['sum_order_usd'] =

        return self.render_to_response(ctx)

    def render_payment_details(self, request, **kwargs):
        """
        Show the payment details page

        This method is useful if the submission from the payment details view
        is invalid and needs to be re-rendered with form errors showing.
        """
        self.preview = False
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)

    def get_default_billing_address(self):
        """
        Return default billing address for user

        This is useful when the payment details view includes a billing address
        form - you can use this helper method to prepopulate the form.

        Note, this isn't used in core oscar as there is no billing address form
        by default.
        """
        if not self.request.user.is_authenticated():
            return None
        try:
            return self.request.user.addresses.get(is_default_for_billing=True)
        except UserAddress.DoesNotExist:
            return None

    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               shipping_charge, billing_address, order_total,
               payment_kwargs=None, order_kwargs=None):
        """
        Submit a basket for order placement.
        The process runs as follows:

         * Generate an order number - 주문번호 생성
         * Freeze the basket so it cannot be modified any more (important when
           redirecting the user to another site for payment as it prevents the
           basket being manipulated during the payment process).

         * Attempt to take payment for the order
           - If payment is successful, place the order
           - If a redirect is required (eg PayPal, 3DSecure), redirect
           - If payment is unsuccessful, show an appropriate error message


        :order_kwargs: Additional kwargs to pass to the place_order method

        :param user: User
        :param basket: The basket to submit. (model)
        :param shipping_address: 배송 주소
        :param shipping_method: 배송 방법
        :param shipping_charge: 배송 비용
        :param billing_address: 지불 주소
        :param order_total: 주문 금액 (shipping_charge  + basket)
        :param :payment_kwargs:  (paypal or alipay)
                Additional kwargs to pass to the handle_payment
                method. It normally makes sense to pass form
                instances (rather than model instances) so that the
                forms can be re-rendered correctly if payment fails.
        :param order_kwargs:
        :return:
        """

        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}
        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        # We generate the order number first as this will be used
        # in payment requests (ie before the order model has been
        # created).  We also save it in the session for multi-stage
        # checkouts (eg where we redirect to a 3rd party site and place
        # the order on a different request).

        # 주문번호 생성 ( mixins.py) - 숫자 (100000 + basket.id)
        order_number = self.generate_order_number(basket)

        # session에 order_number 추가 (checkout.utils.py)
        self.checkout_session.set_order_number(order_number)

        # 주문번호 로그에 저장
        logger.info("Order #%s: beginning submission process for basket #%d",
                    order_number, basket.id)

        # Basket Freeze작업
        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw if we
        # get an unsuccessful payment response when redirecting to a 3rd party
        # site.
        self.freeze_basket(basket)
        # session에 제출된 basket_id저장
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        # 예상되는 에러메시지
        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        # signal:pre_payment
        # Raised immediately before attempting to take payment in the checkout.
        # Arguments sent with this signal: <The view class instance>
        signals.pre_payment.send_robust(sender=self, view=self)

        try:
            # handle_payment: payment를 전달함
            # order_number: 주문번호, order_total: 주문 금액
            self.handle_payment(order_number, order_total, **payment_kwargs)
        except RedirectRequired as e:
            # Redirect required (eg PayPal, 3DS)
            logger.info("Order #%s: redirecting to %s", order_number, e.url)
            return http.HttpResponseRedirect(e.url)
        except UnableToTakePayment as e:
            # Something went wrong with payment but in an anticipated way.  Eg
            # their bankcard has expired, wrong card number - that kind of
            # thing. This type of exception is supposed to set a friendly error
            # message that makes sense to the customer.
            msg = six.text_type(e)
            logger.warning(
                    "Order #%s: unable to take payment (%s) - restoring basket",
                    order_number, msg)
            self.restore_frozen_basket()

            # We assume that the details submitted on the payment details view
            # were invalid (eg expired bankcard).
            return self.render_payment_details(
                    self.request, error=msg, **payment_kwargs)
        except PaymentError as e:
            # A general payment error - Something went wrong which wasn't
            # anticipated.  Eg, the payment gateway is down (it happens), your
            # credentials are wrong - that king of thing.
            # It makes sense to configure the checkout logger to
            # mail admins on an error as this issue warrants some further
            # investigation.
            msg = six.text_type(e)
            logger.error("Order #%s: payment error (%s)", order_number, msg,
                         exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                    self.request, error=error_msg, **payment_kwargs)
        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.error(
                    "Order #%s: unhandled exception while taking payment (%s)",
                    order_number, e, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                    self.request, error=error_msg, **payment_kwargs)

        # 페이먼트가 일어난 후 즉시 일어남
        # post_payment - Raised immediately after payment has been taken.
        signals.post_payment.send_robust(sender=self, view=self)

        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment successful, placing order",
                    order_number)
        try:
            # order 모델에 쓰고 리턴한다.
            return self.handle_order_placement(
                    order_number, user, basket, shipping_address, shipping_method,
                    shipping_charge, billing_address, order_total, **order_kwargs)
        except UnableToPlaceOrder as e:
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in as a
            # payment transaction may already have taken place, but needs
            # to be handled gracefully.
            msg = six.text_type(e)
            logger.error("Order #%s: unable to place order - %s",
                         order_number, msg, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                    self.request, error=msg, **payment_kwargs)

    # get을 대신함
    def get_template_names(self):
        return [self.template_name_preview] if self.preview else [
            self.template_name]


# =========
# PaypalView
# =========
class PaypalView(PaymentDetailsView):
    """
    KAMPER:
        TemplateView FlowChart:
            dispatch()  -> OrderPlacementMixin.dispatch()
            http_method_not_allowed() ->
            get_context_data() ->
    """
    preview = True
    paypal_approved = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:

            self.payment_id = request.GET['paymentId']
            self.payer_id = request.GET['PayerID']
            self.token = request.GET['token']

        except:
            # Manipulation - redirect to basket page with warning message
            logger.warning("Missing GET params on success response page")
            messages.error(self.request, _("Unable to determine PayPal transaction details"))
            return HttpResponseRedirect(reverse("basket:summary"))

        basket = request.basket
        if not basket:
            return http.HttpResponseBadRequest()

        self.paypal_approved = True

        self.payment = Payment.find(self.payment_id)

        return self.handle_place_order_submission(request)

    def post(self, request, *args, **kwargs):
        """
        preview에서 paypal post요청을 했을 때

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not self.preview:
            return http.HttpResponseBadRequest()

        request_action = request.POST.get('action', '')

        # if request_action == 'Alipay' or request_action == 'Paypal':
        #     return self.handle_payment_details_submission(request)
        if request_action == 'PaypalCheckout':
            return self.handle_approve(request)
        else:
            return http.HttpResponseBadRequest()

    def handle_approve(self, request):

        basket = request.basket
        # shipping_address = self.get_shipping_address(basket)
        submission = self.build_submission()

        payment = create_payment(submission)
        return_urls = payment.links[1].href

        return redirect(return_urls)

    def handle_place_order_submission(self, request):
        """
        preview에서 order 주문 했을 때2

        Handle a request to place an order.

        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.

        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """

        return self.submit(**self.build_submission())
        # def handle_execute(self, request):

    def build_submission(self, **kwargs):
        submission = super(
                PaypalView, self).build_submission(**kwargs)
        if self.paypal_approved:
            # Pass the user email so it can be stored with the order

            # submission['order_kwargs']['guest_email'] = self.txn.value('EMAIL')

            # Pass PP params
            submission['payment_kwargs']['payer_id'] = self.payer_id
            submission['payment_kwargs']['token'] = self.token
            submission['payment_kwargs']['payment_id'] = self.payment_id

        return submission

    def handle_payment(self, order_number, total, **kwargs):
        """
        Complete payment with PayPal - this calls the 'DoExpressCheckout'
        method to capture the money from the initial transaction.
        """

        if self.payment.execute({"payer_id": self.payer_id}):
            print("Payment[%s] execute successfully" % (self.payment.id))
        else:
            print(self.payment.error)
            raise UnableToTakePayment()

        # Record payment source and event
        amount_total = self.payment.transactions[0].amount.total
        source_type, is_created = SourceType.objects.get_or_create(
                name='PayPal')
        source = Source(source_type=source_type,
                        currency=self.payment.transactions[0].amount.currency,
                        amount_allocated=amount_total,
                        amount_debited=amount_total)

        self.add_payment_source(source)
        self.add_payment_event('Settled', amount_total, reference=self.payment.id)

    def get_context_data(self, **kwargs):
        ctx = super(PaypalView, self).get_context_data(**kwargs)

        if not hasattr(self, 'payer_id'):
            return ctx

        # This context generation only runs when in preview mode
        ctx.update({
            'payer_id': self.payer_id,
            'token': self.token,
            # 'paypal_user_email': self.txn.value('EMAIL'),
            # 'paypal_amount': D(self.txn.value('AMT')),
        })

        return ctx


class PaypalCancelView(generic.RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        _basket_id = request.basket.id
        basket = get_object_or_404(Basket, id=_basket_id)
        basket.thaw()

        logger.info("Payment cancelled (token %s) - basket #%s thawed",
                    request.GET.get('token', '<no token>'), basket.id)
        return super(PaypalCancelView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.warning(self.request, _("PayPal transaction cancelled"))
        return reverse('basket:summary')


# =========
# Thank you
# =========


class ThankYouView(generic.DetailView):
    """
    Displays the 'thank you' page which summarises the order just submitted.
    """
    template_name = 'checkout/thank_you.html'
    context_object_name = 'order'

    def paypal_payment_mail(self, email, amount, lines, currency):
        try:
            line_list = []
            print(lines)
            for line in lines:
                line_list.append(
                        (str(line.product.title),
                         str(line.quantity)))
        except Exception as e:
            logger.error(e)
            return False

        try:
            send_mail(
                    subject='[paypal 결제정보]',
                    message='[paypal 결제가 왔습니다] \n \n' +
                            'email: %s \n' % str(email) +
                            '총 금액: %s %s\n' % (str(amount), str(currency)) +
                            '제품:\n %s \n' % str(line_list),
                    from_email='admin@kamper.co.kr',
                    recipient_list=['younsooshin@kamper.co.kr', 'inhojames@kamper.co.kr', 'jjh@kamper.co.kr',
                                    'jaina@kamper.co.kr'],
                    fail_silently=False,
            )
        except Exception as e:
            logger.error(e)
            print("메일 전송 실패")
            return False
        return True

    def get_object(self):
        # We allow superusers to force an order thank-you page for testing
        order = None
        if self.request.user.is_superuser:
            if 'order_number' in self.request.GET:
                order = Order._default_manager.get(
                        number=self.request.GET['order_number'])
            elif 'order_id' in self.request.GET:
                order = Order._default_manager.get(
                        id=self.request.GET['order_id'])

        if not order:
            if 'checkout_order_id' in self.request.session:
                order = Order._default_manager.get(
                        pk=self.request.session['checkout_order_id'])
                # 결제 관련 메일 보내
                self.paypal_payment_mail(email=order.email, amount=order.total_before_discounts_incl_tax,
                                         lines=order.basket.all_lines(), currency=order.currency)
            else:
                raise http.Http404(_("No order found"))

        return order
