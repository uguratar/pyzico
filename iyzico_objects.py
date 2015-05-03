# coding=utf-8
__author__ = 'Ugur Atar <ugur@kahvekap.com>'
import requests
import settings
import uuid


class IyzicoValueException(ValueError):

    def __init__(self, *args, **kwargs):
        super(IyzicoValueException, self).__init__(*args, **kwargs)


class IyzicoHTTPException(IOError):

    def __init__(self, *args, **kwargs):
        super(IyzicoHTTPException, self).__init__(*args, **kwargs)


class IyzicoCard:

    def __init__(self, card_number, card_expiry_month,
                 card_expiry_year, card_verification,
                 card_holder_name):
        self.card_number = card_number
        self.card_expiry_month = card_expiry_month
        self.card_expiry_year = card_expiry_year
        self.card_verification = card_verification
        self.card_holder_name = card_holder_name
        self.card_brand = self._card_brand()

    @property
    def card_number(self):
        return self.card_number

    @property
    def card_expiry_month(self):
        return self.expiry_month

    @property
    def card_expiry_year(self):
        return self.card_expiry_year

    @property
    def card_verification(self):
        return self.card_verification

    @property
    def card_brand(self):
        return self.card_brand

    @property
    def card_holder_name(self):
        return self.card_holder_name

    def _card_brand(self):
        number = str(self.card_number)
        card_brand = "Invalid"
        if len(number) == 15:
            if number[:2] == "34" or number[:2] == "37":
                card_brand = "AMEX"
        if len(number) == 13:
            if number[:1] == "4":
                card_brand = "VISA"
        if len(number) == 16:
            if number[:4] == "6011":
                card_brand = "DISCOVER"
            if 51 <= int(number[:2]) <= 55:
                card_brand = "MASTER"
            if number[:1] == "4":
                card_brand = "VISA"
        return card_brand


class IyzicoCustomer:

    def __init__(self, customer_first_name=None,
                 customer_last_name=None,
                 customer_contact_email=None,):
        if customer_first_name is None \
            or customer_last_name is None\
            or customer_first_name is None\
            or len(customer_first_name.strip()) == 0\
            or len(customer_last_name.strip()) == 0 \
                or len(customer_contact_email.strip()) == 0:
            return None
        else:
            self.customer_first_name = customer_first_name
            self.customer_last_name = customer_last_name
            self.customer_contact_email = customer_contact_email

    @property
    def customer_first_name(self):
        return self.customer_first_name

    @property
    def customer_last_name(self):
        return self.customer_last_name

    @property
    def customer_contact_email(self):
        return self.customer_contact_email


class IyzicoCardToken:

    def __init__(self, card_token,):
        self.card_token = card_token

    @property
    def card_token(self):
        return self.card_token


class IyzicoSettings:

    def __init__(self, api_id=None, secret=None,
                 mode=None):
        if api_id is not None and secret is not None and mode is not None:
            self.api_id = api_id
            self.secret = secret
            self.mode = mode
        else:
            self.api_id = settings.api_id
            self.secret = settings.api_secret
            self.mode = settings.mode

    @property
    def api_id(self):
        return self.api_id

    @property
    def secret(self):
        return self.secret

    @property
    def mode(self):
        return self.mode


class IyzicoPayloadBuilder:

    payload = {}

    def __init__(self, settings):
        if not isinstance(settings, IyzicoSettings):
            raise TypeError(str(self.__class__)
                            + ": settings is not instance of "
                            + str(IyzicoSettings))

        self._append_object(settings)
        self.payload['response_mode'] = 'SYNC'

    def debit_with_token(self, card_token, amount, descriptor,
                         currency, customer):

        if not isinstance(card_token, IyzicoCardToken):
            raise TypeError(str(self.__class__)
                            + ": card_token is not instance of "
                            + str(IyzicoCardToken))

        self.payload['external_id'] = uuid.uuid1().hex
        self._append_object(card_token)
        self.payload["type"] = "DB"
        self.payload["amount"] = str(100*(int(amount)))
        self.payload["currency"] = currency
        self.payload["descriptor"] = descriptor

        if customer is not None and isinstance(customer,
                                               IyzicoCustomer):
            self._append_object(customer)

        return self.payload

    def debit(self, card, amount, descriptor, currency,
              customer=None, card_register=False):

        if not isinstance(card, IyzicoCard):
            raise TypeError(str(self.__class__)
                            + ": card is not instance of "
                            + str(IyzicoCard))

        for attr, value in card.__dict__.iteritems():
            self.payload[attr] = value

        self.payload['external_id'] = uuid.uuid1().hex
        self.payload["type"] = "DB"
        self.payload["amount"] = str(100*(int(amount)))
        self.payload["currency"] = currency
        self.payload["descriptor"] = descriptor

        if card_register:
            self.payload["card_register"] = str(int(card_register))

        if customer is not None and isinstance(customer,
                                               IyzicoCustomer):
            self._append_object(customer)

        return self.payload

    def register_card(self, card):
        if not isinstance(card, IyzicoCard):
            raise TypeError(str(self.__class__)
                            + ": card is not instance of "
                            + str(IyzicoCard))

        for attr, value in card.__dict__.iteritems():
            self.payload[attr] = value

        return self.payload

    def delete_card(self, card_token):
        if not isinstance(card_token, IyzicoCardToken):
            raise TypeError(str(self.__class__)
                            + ": card token is not instance of "
                            + str(IyzicoCardToken))

        for attr, value in card_token.__dict__.iteritems():
            self.payload[attr] = value

        return self.payload

    def pre_authorization(self, card, amount, descriptor, currency,
                          customer=None, ):
        if not isinstance(card, IyzicoCard):
            raise TypeError(str(self.__class__)
                            + ": card is not instance of "
                            + str(IyzicoCard))

        for attr, value in card.__dict__.iteritems():
            self.payload[attr] = value

        self.payload['external_id'] = uuid.uuid1().hex
        self.payload["type"] = "PA"
        self.payload["amount"] = str(100*(int(amount)))
        self.payload["currency"] = currency
        self.payload["descriptor"] = descriptor

        if customer is not None and isinstance(customer,
                                               IyzicoCustomer):
            self._append_object(customer)

        return self.payload

    def capture(self, transaction_id, amount, descriptor, currency,
                customer=None, ):

        self.payload['transaction_id'] = transaction_id
        self.payload['external_id'] = uuid.uuid1().hex
        self.payload["type"] = "CP"
        self.payload["amount"] = str(100*(int(amount)))
        self.payload["currency"] = currency
        self.payload["descriptor"] = descriptor

        if customer is not None and isinstance(customer,
                                               IyzicoCustomer):
            self._append_object(customer)

        return self.payload

    def refund(self, transaction_id, amount, descriptor, currency,
               customer=None,):

        self.payload['transaction_id'] = transaction_id
        self.payload['external_id'] = uuid.uuid1().hex
        self.payload["type"] = "RF"
        self.payload["amount"] = str(100*(int(amount)))
        self.payload["currency"] = currency
        self.payload["descriptor"] = descriptor

        if customer is not None and isinstance(customer,
                                               IyzicoCustomer):
            self._append_object(customer)

        return self.payload

    def reversal(self, transaction_id, amount, descriptor, currency,
                 customer=None,):
        self.refund(transaction_id, amount, descriptor, currency,
                    customer)
        self.payload["type"] = "RV"

        return self.payload

    def _append_object(self, obj):
            for attr, value in obj.__dict__.iteritems():
                self.payload[attr] = value


class IyzicoRequest():

    @staticmethod
    def execute(url, payload):
        try:
            raw_response = requests.post(url, payload)
            raw_response.raise_for_status()
            response = IyzicoResponse(raw_response)
            return response
        except requests.RequestException as re:
            raise IyzicoHTTPException(re)
        except ValueError as value_error:
            raise IyzicoValueException(value_error)



class IyzicoResponse():

    def __init__(self, server_response):
        self._raw_response = server_response
        self._json_response = server_response.json()
        self.response = self._json_response["response"]

        if self.response["state"] == "success":
            self.success = True

            try:
                self.mode = self._json_response["mode"]
            except KeyError:
                self.mode = None

            try:
                self.transaction = self._json_response["transaction"]
            except KeyError:
                self.transaction = None

            try:
                self.account = self._json_response["account"]
            except KeyError:
                self.account = None

            try:
                self.customer = self._json_response["customer"]
            except KeyError:
                self.customer = None

            try:
                self.card_token = self._json_response["card_token"]
            except KeyError:
                self.card_token = None

        else:
            self.success = False

    @property
    def response(self):
        return self.response

    @property
    def mode(self):
        return self.mode

    @property
    def card_token(self):
        return self.card_token

    @property
    def transaction(self):
        return self.transaction

    @property
    def customer(self):
        return self.customer

    @property
    def account(self):
        return self.account

    @property
    def success(self):
        return self.success
