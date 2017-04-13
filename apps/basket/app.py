from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from oscar.core.application import Application as CoreBasketApplication
from oscar.core.loading import get_class



class BasketApplication(CoreBasketApplication):
    """
    기능:
        카트 summary: /
        카트 넣기: /
    보류:
        쿠폰 기능: vouchers/*
        카트 니중에 구매: saved/*
    """
    name = 'basket'
    summary_view = get_class('basket.views', 'BasketView')
    saved_view = get_class('basket.views', 'SavedView')
    add_view = get_class('basket.views', 'BasketAddView')
    add_voucher_view = get_class('basket.views', 'VoucherAddView')
    remove_voucher_view = get_class('basket.views', 'VoucherRemoveView')

    remove_basket_item = get_class('basket.views', 'BasketRemoveItemView')


    def get_urls(self):
        urls = [
            # 카트 화면
            url(r'^$', self.summary_view.as_view(), name='summary'),
            # <KAMPER> 카트에 추가
            url(r'^add/(?P<pk>\d+)/$', self.add_view.as_view(), name='add'),
            url(r'^remove/$', self.remove_basket_item.as_view(), name='remove_item'),


            # url(r'^vouchers/add/$', self.add_voucher_view.as_view(),
            #     name='vouchers-add'),
            # url(r'^vouchers/(?P<pk>\d+)/remove/$',
            #     self.remove_voucher_view.as_view(), name='vouchers-remove'),

            # <KAMPER> 카트에 나중에 사기
            # url(r'^saved/$', login_required(self.saved_view.as_view()),
            #     name='saved'),
        ]
        return self.post_process_urls(urls)


application = BasketApplication()
