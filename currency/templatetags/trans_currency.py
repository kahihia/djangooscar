from decimal import Decimal
from django import template
from django.conf import settings

register = template.Library()

KRW_PER_USD = settings.CURRENCY_KRW_PER_USD  # 달러
KRW_PER_RMB = settings.CURRENCY_KRW_PER_RMB  # 위안


# AbstractStockRecord에서 price 사용
@register.simple_tag
def trans_usd_currency(krw_price):
    usd_price = Decimal(krw_price/KRW_PER_USD)
    usd_price = round(usd_price,2)
    usd_price = "$" + str(usd_price)
    return usd_price


@register.simple_tag
def trans_rmb_currency(krw_price):
    rmb_price = Decimal(krw_price / KRW_PER_RMB)
    rmb_price = round(rmb_price ,2)
    rmb_price = "¥" + str(rmb_price)
    return rmb_price
