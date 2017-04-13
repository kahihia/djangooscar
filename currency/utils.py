from decimal import Decimal
from django.conf import settings

KRW_PER_USD = settings.CURRENCY_KRW_PER_USD  # 달러
KRW_PER_RMB = settings.CURRENCY_KRW_PER_RMB  # 위안


# AbstractStockRecord에서 price 사용
def trans_usd(krw_price):
    usd_price = Decimal(krw_price / KRW_PER_USD)
    usd_price = round(usd_price, 2)
    return usd_price


def trans_rmb_currency(krw_price):
    rmb_price = Decimal(krw_price / KRW_PER_RMB)
    rmb_price = round(rmb_price, 2)
    return rmb_price
