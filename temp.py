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
        elif request_action == 'PaypalCheckout':
            return self.handle_paypal_checkout(request)
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