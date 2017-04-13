
# 작업중

class PaypalResource(object):
    def get_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


class PayPalCreateResource(PaypalResource):
    """
    intent = <enum> <sale, authorize, order> - required
    payer = PaypalPayerResource() - required
    transations = PaypalTrnasationsResource() - required
    experience_profile_id = String 	### Optionally, specify the PayPal-generated ID for a web experience profile.
    note_to_payer = String
    redirect_urls = PaypalRedirectUrlResource() -
    """

    def __init__(self, intent, payer, transations, experience_profile_id=None, note_to_payer=None,
                 redirect_urls=None):
        self.intent = intent  # required
        self.payer = payer.get_dict()  # required
        self.transations = transations.get_dict()  # required
        self.experience_profile_id = experience_profile_id
        self.note_to_payer = note_to_payer
        self.redirect_urls = redirect_urls


class PaypalPayerResource(PaypalResource):
    """
    payer_method = [enum] <credit_card, paypal>
    status = [enum] <VERIFIED, UNVERIFIED>  : Read Only
    funding_instruments
    external_selected_funding_instrument_type
    payer_info = PayerInfoResource() -
    """

    def __init__(self, payment_method, funding_instruments=None, payer_info=None,
                 external_selected_funding_instrument_type=None,
                 status=None):
        self.payment_method = payment_method
        self.funding_instruments = funding_instruments
        self.payer_info = payer_info
        self.external_selected_funding_instrument_type = external_selected_funding_instrument_type
        self.status = status


class TransactionsResource(PaypalResource):
    def __init__(self, reference_id=None, amount=None, description=None, note_to_payee=None, custom=None,
                 invoice_number=None, soft_descriptor=None, payment_options=None, item_list=None, notify_url=None,
                 order_url=None, related_resource=None):
        self.reference_id = reference_id
        self.amount = amount
        self.description = description
        self.note_to_payee = note_to_payee
        self.custom = custom
        self.invoice_number = invoice_number
        self.soft_descriptor = soft_descriptor
        self.payment_options = payment_options
        self.item_list = item_list
        self.notify_url = notify_url
        self.order_url = order_url
        self.related_resource = related_resource


class PaypalAmountResource(PaypalResource):
    def __init__(self, currency=None, total=None, details=None):
        self.currency = currency
        self.total = total
        self.details = details


class PaypalDetailsResource(PaypalResource):
    def __init__(self, subtotal=None, shipping=None, tax=None, handling_fee=None, shipping_discount=None,
                 insurance=None, gift_wrap=None):
        self.subtotal = subtotal
        self.shipping = shipping
        self.tax = tax
        self.handling_fee = handling_fee
        self.shipping_discount = shipping_discount
        self.insurance = insurance
        self.gift_wrap = gift_wrap


class PaypalItemListResource(PaypalResource):
    def __init__(self, items=None, shipping_addres=None, shipping_method=None, shipping_phone_number=None):
        self.items = items
        self.shipping_addres = shipping_addres
        self.shipping_method = shipping_method
        self.shipping_phone_number = shipping_phone_number


class PaypalItemResource(PaypalResource):
    def __init__(self, sku=None, name=None, description=None, quantity=None, price=None, currency=None, tax=None,
                 url=None):
        self.sku = sku
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.currency = currency
        self.tax = tax
        self.url = url


transactions = TransactionsResource()
payer = PaypalPayerResource(payment_method="paypal")
payment = PayPalCreateResource("sale", payer, transactions)


class PayerInfoResource(PaypalResource):
    def __init__(self, email=None, external_remember_me_id=None, buyer_account_number=None, saluation=None,
                 first_name=None, middle_name=None, last_name=None, suffix=None, payer_id=None, phone=None,
                 phone_type=None, birth_date=None, tax_id=None, tax_id_type=None, country_code=None,
                 billing_address=None, shipping_address=None):
        self.email = email
        self.external_remember_me_id = external_remember_me_id
        self.buyer_account_number = buyer_account_number
        self.saluation = saluation
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix
        self.payer_id = payer_id
        self.phone = phone
        self.phone_type = phone_type
        self.birth_date = birth_date
        self.tax_id = tax_id
        self.tax_id_type = tax_id_type
        self.country_code = country_code
        self.billing_address = billing_address  # AddressResource
        self.shipping_address = shipping_address  # ShippingAddressResource()  # ShippingAddressResource


class AddressResource(PaypalResource):
    def __init__(self, line1, line2, city, country_code, postal_code, state, phone, normalization_status, status):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.country_code = country_code
        self.postal_code = postal_code
        self.state = state
        self.phone = phone
        self.normalization_status = normalization_status
        self.status = status
        self.line1 = line1
        super().__init__()


class ShippingAddressResource(AddressResource):
    recipient_name = None
