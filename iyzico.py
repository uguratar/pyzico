# coding=utf-8
__author__ = 'Ugur Atar <ugur@kahvekap.com>'
import requests
import requests.exceptions
import settings

from iyzico_objects import IyzicoSettings, IyzicoPayloadBuilder, \
    IyzicoResponse


class Iyzico():

    url = settings.url
    delete_card_url = settings.delete_card_url
    register_card_url = settings.register_card_url

    def __init__(self):
        #init with default settings from settings.py
        self._settings = IyzicoSettings()
        self._payload_builder = IyzicoPayloadBuilder(self._settings)

    def debit_with_token(self, amount, card_token,
                         description, currency,
                         customer=None):

        payload = \
            self._payload_builder.debit_with_token(card_token,
                                                   amount,
                                                   description,
                                                   currency,
                                                   customer)

        try:
            raw_response = requests.post(self.url, payload)
            response = IyzicoResponse(raw_response)
            return response.success, response
        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message
        except Exception as e:
            return False, e.message

    def debit(self, amount, card,
              description, currency, customer=None,
              card_register=False):

        payload = \
            self._payload_builder.debit(card, amount, description,
                                        currency, customer,
                                        card_register)

        try:
            raw_response = requests.post(self.url, payload, )
            response = IyzicoResponse(raw_response)
            return response.success, response

        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message

    def pre_authorize(self, amount, card, description, currency,
                      customer=None,):
        payload = \
            self._payload_builder.pre_authorization(card, amount,
                                                    description,
                                                    currency,
                                                    customer,)

        try:
            raw_response = requests.post(self.url, payload)
            response = IyzicoResponse(raw_response)
            return response.success, response

        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message

    def capture(self, amount, transaction_id, description, currency,
                customer=None,):
        payload = \
            self._payload_builder.capture(transaction_id, amount,
                                          description,
                                          currency,
                                          customer,)

        try:
            raw_response = requests.post(self.url, payload)
            response = IyzicoResponse(raw_response)
            return response.success, response

        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message

    def refund(self, amount, transaction_id, description, currency,
               customer=None,):
        payload = \
            self._payload_builder.refund(transaction_id, amount,
                                         description,
                                         currency,
                                         customer,)

        try:
            raw_response = requests.post(self.url, payload)
            response = IyzicoResponse(raw_response)
            return response.success, response

        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message

    def reversal(self, amount, transaction_id, description, currency,
                 customer=None,):
        payload = \
            self._payload_builder.reversal(transaction_id, amount,
                                           description,
                                           currency,
                                           customer,)

        try:
            raw_response = requests.post(self.url, payload)
            response = IyzicoResponse(raw_response)
            return response.success, response

        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message

    def register_card(self, card):

        payload = \
            self._payload_builder.register_card(card)

        try:
            raw_response = requests.post(self.register_card_url, payload)
            response = IyzicoResponse(raw_response)
            return response.success, response
        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message
        except Exception as e:
            return False, e.message

    def delete_card(self, card_token):

        payload = \
            self._payload_builder.delete_card(card_token)

        try:
            raw_response = requests.post(self.delete_card_url,
                                         payload)
            response = IyzicoResponse(raw_response)
            return response.success, response
        except ValueError as value_error:
            return False, value_error.message
        except requests.exceptions.Timeout as timeout:
            return False, timeout.message
        except Exception as e:
            return False, e.message
