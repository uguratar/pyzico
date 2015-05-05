# coding=utf-8
__author__ = 'Ugur Atar <ugur@kahvekap.com>'
import settings
from iyzico_objects import IyzicoSettings, IyzicoPayloadBuilder, \
    IyzicoRequest, IyzicoCardException


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
        return IyzicoRequest.execute(self.url, payload)

    def debit(self, amount, card,
              description, currency, customer=None,
              card_register=False):

        if not card.is_valid:
            raise IyzicoCardException("Invalid credit card info.")

        payload = \
            self._payload_builder.debit(card, amount, description,
                                        currency, customer,
                                        card_register)

        return IyzicoRequest.execute(self.url, payload)

    def pre_authorize(self, amount, card, description, currency,
                      customer=None,):
        if not card.is_valid:
            raise IyzicoCardException("Invalid credit card info.")

        payload = \
            self._payload_builder.pre_authorization(card, amount,
                                                    description,
                                                    currency,
                                                    customer,)
        return IyzicoRequest.execute(self.url, payload)

    def capture(self, amount, transaction_id, description, currency,
                customer=None,):
        payload = \
            self._payload_builder.capture(transaction_id, amount,
                                          description,
                                          currency,
                                          customer,)
        return IyzicoRequest.execute(self.url, payload)

    def refund(self, amount, transaction_id, description, currency,
               customer=None,):
        payload = \
            self._payload_builder.refund(transaction_id, amount,
                                         description,
                                         currency,
                                         customer,)
        return IyzicoRequest.execute(self.url, payload)

    def reversal(self, amount, transaction_id, description, currency,
                 customer=None,):
        payload = \
            self._payload_builder.reversal(transaction_id, amount,
                                           description,
                                           currency,
                                           customer,)
        return IyzicoRequest.execute(self.url, payload)

    def register_card(self, card):

        if not card.is_valid:
            raise IyzicoCardException("Invalid credit card info.")

        payload = \
            self._payload_builder.register_card(card)
        return IyzicoRequest.execute(self.register_card_url, payload)

    def delete_card(self, card_token):

        payload = \
            self._payload_builder.delete_card(card_token)
        return IyzicoRequest.execute(self.delete_card_url, payload)
