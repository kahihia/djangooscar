from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from oscar.apps.checkout.app import CheckoutApplication as CoreCheckoutApplication
from oscar.core.loading import get_class


class CheckoutApplication(CoreCheckoutApplication):
    name = 'checkout'

    index_view = get_class('checkout.views', 'IndexView')
    shipping_address_view = get_class('checkout.views', 'ShippingAddressView')
    user_address_update_view = get_class('checkout.views',
                                         'UserAddressUpdateView')
    user_address_delete_view = get_class('checkout.views',
                                         'UserAddressDeleteView')
    shipping_method_view = get_class('checkout.views', 'ShippingMethodView')
    payment_method_view = get_class('checkout.views', 'PaymentMethodView')
    payment_details_view = get_class('checkout.views', 'PaymentDetailsView')
    thankyou_view = get_class('checkout.views', 'ThankYouView')

    # paypal_approve_view = get_class('checkout.views', 'PaypalApproveView')
    # paypal_execute_view = get_class('checkout.views', 'PaypalExecuteView')
    # paypal_cancel_view = get_class('checkout.views', 'PaypalCancelView')
    paypal_cancel_view = get_class('checkout.views', 'PaypalCancelView')
    paypal_view = get_class('checkout.views', 'PaypalView')

    def get_urls(self):
        urls = [
            # Checkout Index - 로그인 되어 있는지 확인
            url(r'^$', self.index_view.as_view(), name='index'),

            # Shipping/user address views
            url(r'shipping-address/$',
                self.shipping_address_view.as_view(), name='shipping-address'),
            # User-address 수정
            url(r'user-address/edit/(?P<pk>\d+)/$',
                self.user_address_update_view.as_view(),
                name='user-address-update'),
            # User-address 삭제
            url(r'user-address/delete/(?P<pk>\d+)/$',
                self.user_address_delete_view.as_view(),
                name='user-address-delete'),

            # Shipping method views
            url(r'shipping-method/$',
                self.shipping_method_view.as_view(), name='shipping-method'),

            # Payment views
            url(r'payment-method/$',
                self.payment_method_view.as_view(), name='payment-method'),
            url(r'payment-details/$',
                self.payment_details_view.as_view(), name='payment-details'),

            # Preview and thankyou
            url(r'preview/$',
                self.payment_details_view.as_view(preview=True),
                name='preview'),

            url(r'paypal/approve/$', self.paypal_view.as_view(), name='paypal-approve'),
            url(r'paypal/cancel/$', self.paypal_cancel_view.as_view(), name='paypal-cancel'),

            # 페이팔 생성 및 승인
            # url(r'paypal/approve/$', self.paypal_approve_view.as_view(), name='paypal-approve'),
            # 페이팔 실행
            # url(r'paypal/execute/$', self.paypal_execute_view.as_view(), name='paypal-execute'),


            url(r'thank-you/$', self.thankyou_view.as_view(),
                name='thank-you'),

            # # Checkout with Paypal
            # url(r'paypal/', include('paypal.express.urls')),

        ]
        return self.post_process_urls(urls)

    def get_url_decorator(self, pattern):
        # 익명 결제가 가능하지 않으면 로그인 필요

        if not settings.OSCAR_ALLOW_ANON_CHECKOUT:
            return login_required
        # 한번 더 찾기
        if pattern.name.startswith('user-address'):
            return login_required
        return None


application = CheckoutApplication()
