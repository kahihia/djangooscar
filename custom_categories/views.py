from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.views.generic import FormView, View, TemplateView

from custom_categories.forms import WirelessReservationForm


class WirelessReservationView(FormView):
    form_class = WirelessReservationForm
    template_name = 'custom/wireless.html'
    success_url = '/wireless/'

    today = datetime.today()
    able_date = today + timedelta(days=2)

    def get_success_url(self):
        messages.info(self.request, "예약이 되었습니다. 메일로 연락을 드리겠습니다.")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        kwargs['today_year'] = self.able_date.year
        kwargs['today_month'] = self.able_date.month
        kwargs['today_day'] = self.able_date.day
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        reservation = form.save(commit=False)

        send_mail(
                "[휴대폰 예약]" + reservation.user_name + "  " + reservation.meet_place + " " + str(
                        reservation.meet_date) + "  " + str(reservation.meet_time),
                '휴대폰 예약이 왔습니다' + '\n' +
                'user_name: ' + reservation.user_name + "\n" +
                'user_email: ' + reservation.user_email + '\n' +
                'meet_place: ' + reservation.meet_place + '\n' +
                'meet_date: ' + str(reservation.meet_date) + '\n' +
                'meet_time: ' + str(reservation.meet_time) + '\n' +
                'recommended_user_id: ' + reservation.recommended_user_email + '\n',
                'admin@kamper.co.kr',
                ['kamper_sales@kamper.co.kr'],
                fail_silently=False,
        )
        reservation.save()

        return super(WirelessReservationView, self).form_valid(form)


class DateCheckView(View):
    def get(self):
        return "A"

    def post(self):
        print("DD")


class DeliveryView(TemplateView):
    template_name = 'custom/delivery.html'


# class BasketAddView(FormView):
#     """
#     Handles the add-to-basket submissions, which are triggered from various
#     parts of the site. The add-to-basket form is loaded into templates using
#     a templatetag from module basket_tags.py.
#     """
#
#     form_class = AddToBasketForm
#     product_model = get_model('catalogue', 'product')
#     add_signal = signals.basket_addition
#     http_method_names = ['post']
#
#
#     def post(self, request, *args, **kwargs):
#         self.product = shortcuts.get_object_or_404(
#                 self.product_model, pk=kwargs['pk'])
#         return super(BasketAddView, self).post(request, *args, **kwargs)
#
#     def get_form_kwargs(self):
#         kwargs = super(BasketAddView, self).get_form_kwargs()
#         kwargs['basket'] = self.request.basket
#         kwargs['product'] = self.product
#
#         return kwargs
#
#     def form_invalid(self, form):
#         msgs = []
#         for error in form.errors.values():
#             msgs.append(error.as_text())
#         clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
#         messages.error(self.request, ",".join(clean_msgs))
#
#         return redirect_to_referrer(self.request, 'basket:summary')
#
#     def form_valid(self, form):
#         offers_before = self.request.basket.applied_offers()
#
#         self.request.basket.add_product(
#                 form.product, form.cleaned_data['quantity'],
#                 form.cleaned_options())
#
#         messages.success(self.request, self.get_success_message(form),
#                          extra_tags='safe noicon')
#
#         # Check for additional offer messages
#         BasketMessageGenerator().apply_messages(self.request, offers_before)
#
#         # Send signal for basket addition
#         self.add_signal.send(
#                 sender=self, product=form.product, user=self.request.user,
#                 request=self.request)
#         return super(BasketAddView, self).form_valid(form)
#
#     def get_success_message(self, form):
#         return render_to_string(
#                 'basket/messages/addition.html',
#                 {'product': form.product,
#                  'quantity': form.cleaned_data['quantity']})
#
#     def get_success_url(self):
#         post_url = self.request.POST.get('next')
#
#         if post_url and is_safe_url(post_url, self.request.get_host()):
#             return post_url
#         return safe_referrer(self.request, 'basket:summary')
