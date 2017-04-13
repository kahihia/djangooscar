 # paypal payment

# CreatePayment using credit card Sample
# This sample code demonstrate how you can process
# a payment with a credit card.
# API used: /v1/payments/payment

from django.conf import settings
import paypalrestsdk

import logging

from currency.utils import trans_usd

logging.basicConfig(level=logging.INFO)

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

web_profile = settings.PAYPAL_WEB_PROFILE

paypal_currency = settings.PAYPAL_CURRENCY


def create_payment(submission):
    shipping_address = submission['shipping_address']
    shipping_method = submission['shipping_method']
    basket = submission['basket']
    billing_address = submission['billing_address']
    order_total = submission['order_total']
    shipping_charge = submission['shipping_charge']

    result_items = []
    total_line_price = 0
    for item in basket.all_lines():
        item_price = trans_usd(item.unit_price_incl_tax)

        item_total_price = item_price * item.quantity

        total_line_price += item_total_price

        result_items.append({
            'name': item.product.get_title(),
            'sku': item.product.upc,
            'price': str(item_price),
            'currency': paypal_currency,
            'quantity': str(item.quantity),
            # 'description':
        })

    shipping_usd_charge = trans_usd(shipping_charge.incl_tax)

    order_total_price = shipping_usd_charge + total_line_price

    payment_attr = {
        "intent": "sale",  # express checkout
        "experience_profile_id": web_profile,
        "redirect_urls": {
            "return_url": settings.PAYPAL_RETURN_URI,
            "cancel_url": settings.PAYPAL_CANCEL_URI
        },
        "payer": {
            "payment_method": "paypal",  # paypal
            "payer_info": {
                # 'shipping_address': {
                #     'postal_code': shipping_address.postcode,
                #     'line1': shipping_address.line1 + shipping_address.line2,
                #     'line2': shipping_address.line3,
                #     'city': shipping_address.line4,
                #     'country_code': shipping_address.country.iso_3166_1_a2,
                #     'recipient_name': shipping_address.name
                # }
            }
        },
        "transactions": [
            {
                # ItemList
                "item_list": {
                    "items": result_items,

                    # "shipping_address": {
                    #     "recipient_name": shipping_address.name,
                    #     "line1": shipping_address.line1 + shipping_address.line2 + shipping_address.line3,
                    #     "city": shipping_address.line4,
                    #     "country_code": shipping_address.country.iso_3166_1_a2,
                    #     "postal_code": shipping_address.postcode,
                    #     "state": shipping_address.state
                    # }

                },
                # Amount
                # Let's you specify a payment amount.
                "amount": {
                    # "total": str(order_total.incl_tax),  # 금액
                    "total": str(order_total_price),  # 금액
                    "currency": "USD",
                    "details": {
                        "subtotal": str(order_total_price - shipping_usd_charge),
                        "shipping": str(shipping_usd_charge),
                    }
                    # https://developer.paypal.com/docs/integration/direct/rest-api-payment-country-currency-support/
                },
                "description": "Thank you",
            }
        ]
    }
    if shipping_address is not None:
        payment_attr['payer']['payer_info']['shipping_address'] = {
            'postal_code': shipping_address.postcode,
            'line1': shipping_address.line1 + shipping_address.line2,
            'line2': shipping_address.line3,
            'city': shipping_address.line4,
            'country_code': shipping_address.country.iso_3166_1_a2,
            'recipient_name': shipping_address.name
        }
        if shipping_address.line3 is None:
            shipping_address.line3 = ""
        if shipping_address.state is None:
            shipping_address.state = ""
    else:
        payment_attr['payer']['payer_info']['shipping_address'] = {
            'postal_code': "",
            'line1': "",
            'line2': "",
            'city': "",
            'country_code': "",
            'recipient_name': ""
        }

    print("AA")


    if shipping_address is not None:
        if shipping_address.get_phone_number() is not None:
            payment_attr["payer"]["payer_info"]["shipping_address"]["phone"] = submission[
                'shipping_address'].get_phone_number

    payment = paypalrestsdk.Payment(payment_attr)
    # Create Payment and return status( True or False )
    if payment.create():
        print("Payment[%s] created successfully" % payment.id)
    else:
        print("Error while creating payment:")
        print(payment.error)

    return payment


def create_web_experience_profile():
    web_profile = paypalrestsdk.WebProfile({
        "name": "KAMPER",
        "presentation": {
            "brand_name": "KAMPER PAYPAL",
            "logo_image": "https://kamper.co.kr/static/kamper/images/logo.jpg",
            "locale_code": "KR"
        },
        "input_fields": {
            "allow_note": True,
            "no_shipping": 2,
            "address_override": 1,
        },
        "flow_config": {

        }
    })
    if web_profile.create():
        print("Web Profile[%s] created successfully" % (web_profile.id))
    else:
        print(web_profile.error)
    return web_profile


def make_json(root, dics):
    """
    여러개 들어갈때
    :param root:
    :param dics:
    :return:
    """
    result_json = {}
    for key, value in dics:
        result_json[root][key] = value
    return result_json


class KamperPaypal(object):
    def create_payment(self, submission):

        # payment

        shipping_address = submission['shipping_address']
        shipping_method = submission['shipping_method']
        basket = submission['basket']
        billing_address = submission['billing_address']
        order_total = submission['order_total']
        shipping_charge = submission['shipping_charge']
        if billing_address is None:
            billing_address = shipping_address
        items = basket.all_lines()
        result_items = []
        for item in items:
            result_items.append({
                'name': item.product.get_title(),
                'sku': item.product.get_title(),
                'price': str(item.unit_price_incl_tax),
                'currency': item.price_currency,
                'quantity': str(item.quantity),
                # 'description':
            })
        result_items.append({
            'name': "shipping fee",
            'sku': 'shipping fee',
            'price': "3",
            'currency': 'USD'
        })
        payment = paypalrestsdk.Payment(
                {
                    "intent": "sale",  # express checkout
                    "redirect_urls": {
                        "return_url": settings.PAYPAL_RETURN_URI,
                        "cancel_url": settings.PAYPAL_CANCEL_URI
                    },

                    # Payer
                    # A resource representing a Payer that funds a payment
                    # Use the List of `FundingInstrument` and the Payment Method
                    # as 'credit_card'
                    "payer": {
                        "payment_method": "paypal",  # paypal
                    },
                    # Transaction
                    # A transaction defines the contract of a
                    # payment - what is the payment for and who
                    # is fulfilling it.
                    "transactions": [
                        {
                            # ItemList
                            "item_list": {
                                "items": result_items,
                            },

                            # Amount
                            # Let's you specify a payment amount.
                            "amount": {
                                "total": str(order_total.incl_tax),  # 금액
                                "currency": "USD"  # 통화  3-letter currency code. PayPal does not support all currencies.
                                # https://developer.paypal.com/docs/integration/direct/rest-api-payment-country-currency-support/

                            },
                            "description": "description",

                        }
                    ]
                }
        )
        # Create Payment and return status( True or False )
        if payment.create():
            print("Payment[%s] created successfully" % (payment.id))
        else:
            print("Error while creating payment:")
            print(payment.error)

        return payment
