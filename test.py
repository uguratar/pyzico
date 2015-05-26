import unittest

import settings
from iyzico_objects import IyzicoCustomer, IyzicoCardToken, \
    IyzicoSettings, IyzicoPayloadBuilder, IyzicoCard

__author__ = 'ugur'
# coding=utf-8



class TestIyzicoObjects(unittest.TestCase):

    def test_customer(self):
        customer = IyzicoCustomer("First", "Last",
                                  "email@email")

        self.assertEqual(customer.customer_first_name, 'First')
        self.assertEqual(customer.customer_last_name, 'Last')
        self.assertEqual(customer.customer_contact_email,
                         'email@email')

    def test_card_token(self):
        token = IyzicoCardToken("my token")

        self.assertEqual(token.card_token, 'my token')

    def test_settings(self):
        #Testing settings with constructor params
        settings_setter = IyzicoSettings("api_id", "api_secret", "test")
        self.assertEqual(settings_setter.api_id, 'api_id')
        self.assertEqual(settings_setter.secret, 'api_secret')
        self.assertEqual(settings_setter.mode, 'test')

        #Testing settings with default params
        settings_default\
            = IyzicoSettings()
        self.assertEqual(settings_default.api_id, settings.api_id)
        self.assertEqual(settings_default.secret,
                         settings.api_secret)
        self.assertEqual(settings_default.mode, settings.mode)


class TestPayloadBuilder(unittest.TestCase):

    def test_invalid_settings(self):
        self.assertRaises(TypeError,
                          IyzicoPayloadBuilder,
                          "invalid settings object")

    def setUp(self):
        self.settings_default\
            = IyzicoSettings()
        self.builder = IyzicoPayloadBuilder(self.settings_default)

    def test_init_builder(self):
        settings_default\
            = IyzicoSettings()
        builder = IyzicoPayloadBuilder(settings_default)
        self.assertEqual(builder.payload['api_id'], settings.api_id)
        self.assertEqual(builder.payload['mode'], settings.mode)
        self.assertEqual(builder.payload['response_mode'], "SYNC")
        self.assertEqual(builder.payload['secret'],
                         settings.api_secret)

    def test_debit_with_token(self):
        token = IyzicoCardToken("1234")
        self.builder.debit_with_token(token, 1,
                                      "description", "TL", None)
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['card_token'],
                          "1234")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "DB")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")
        with self.assertRaises(KeyError):
             self.builder.payload['customer_first_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_last_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_contact_email']

    def test_debit_with_token_witch_customer(self):
        token = IyzicoCardToken("1234")
        customer = IyzicoCustomer("first", "last", "email@email")
        self.builder.debit_with_token(token, 1,
                                      "description", "TL", customer)
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['card_token'],
                          "1234")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "DB")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")
        self.assertEquals(
            self.builder.payload['customer_first_name'],
            "first")
        self.assertEquals(
            self.builder.payload['customer_last_name'],
            "last")
        self.assertEquals(
            self.builder.payload['customer_contact_email'],
            "email@email")

    def test_debit(self):

        with self.assertRaises(TypeError):
            self.builder.debit("false card type",
                               1, "description", "TL")

        card = IyzicoCard("4242424242424242", "10", "15", "000",
                          "test card")
        self.builder.debit(card, 1, "description", "TL")
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['card_number'],
                          "4242424242424242")
        self.assertEquals(self.builder.payload['card_expiry_year'],
                          "15")
        self.assertEquals(self.builder.payload['card_expiry_month'],
                          "10")
        self.assertEquals(self.builder.payload['card_verification'],
                          "000")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "DB")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")

        with self.assertRaises(KeyError):
             self.builder.payload['customer_first_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_last_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_contact_email']
        with self.assertRaises(KeyError):
             self.builder.payload['connector_type']
        with self.assertRaises(KeyError):
             self.builder.payload['installment_count']
        with self.assertRaises(KeyError):
             self.builder.payload['card_register']

    def test_debit_with_optional_params(self):

        card = IyzicoCard("4242424242424242", "10", "15", "000",
                          "test card")
        customer = IyzicoCustomer("first", "last", "email@email")

        self.builder.debit(card, 1, "description", "TL",
                           customer=customer,
                           card_register=True,
                           installment=6)

        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['card_number'],
                          "4242424242424242")
        self.assertEquals(self.builder.payload['card_expiry_year'],
                          "15")
        self.assertEquals(self.builder.payload['card_expiry_month'],
                          "10")
        self.assertEquals(self.builder.payload['card_verification'],
                          "000")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "DB")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")
        self.assertEquals(self.builder.
                          payload['customer_first_name'],
                          "first")
        self.assertEquals(self.builder.payload['customer_last_name'],
                          "last")
        self.assertEquals(self.builder.
                          payload['customer_contact_email'],
                          "email@email")

        self.assertEquals(self.builder.
                          payload['card_register'],
                          "1")
        self.assertEquals(self.builder.
                          payload['installment_count'],
                          "6")

    def test_register_card(self):
        with self.assertRaises(TypeError):
            self.builder.register_card("false card type")

        card = IyzicoCard("4242424242424242", "10", "15", "000",
                          "test card")
        self.builder.register_card(card)
        self.assertEquals(self.builder.payload['card_number'],
                          "4242424242424242")
        self.assertEquals(self.builder.payload['card_expiry_year'],
                          "15")
        self.assertEquals(self.builder.payload['card_expiry_month'],
                          "10")
        self.assertEquals(self.builder.payload['card_verification'],
                          "000")

    def test_delete_card(self):
        with self.assertRaises(TypeError):
            self.builder.delete_card("false card type")

        token = IyzicoCardToken("1234")
        self.builder.delete_card(token)
        self.assertEquals(self.builder.payload['card_token'],
                          "1234")

    def test_pre_authorization(self):

        with self.assertRaises(TypeError):
            self.builder.pre_authorization("false card type",
                                           1, "description", "TL")

        card = IyzicoCard("4242424242424242", "10", "15", "000",
                          "test card")
        self.builder.pre_authorization(card, 1, "description", "TL")
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['card_number'],
                          "4242424242424242")
        self.assertEquals(self.builder.payload['card_expiry_year'],
                          "15")
        self.assertEquals(self.builder.payload['card_expiry_month'],
                          "10")
        self.assertEquals(self.builder.payload['card_verification'],
                          "000")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "PA")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")

        with self.assertRaises(KeyError):
             self.builder.payload['customer_first_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_last_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_contact_email']

    def test_pre_authorization_with_customer(self):

        with self.assertRaises(TypeError):
            self.builder.pre_authorization("false card type",
                                           1, "description", "TL")

        customer = IyzicoCustomer("first", "last", "email@email")

        card = IyzicoCard("4242424242424242", "10", "15", "000",
                          "test card")
        self.builder.pre_authorization(card, 1, "description", "TL",
                                       customer)
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['card_number'],
                          "4242424242424242")
        self.assertEquals(self.builder.payload['card_expiry_year'],
                          "15")
        self.assertEquals(self.builder.payload['card_expiry_month'],
                          "10")
        self.assertEquals(self.builder.payload['card_verification'],
                          "000")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "PA")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")
        self.assertEquals(self.builder.
                          payload['customer_first_name'],
                          "first")
        self.assertEquals(self.builder.payload['customer_last_name'],
                          "last")
        self.assertEquals(self.builder.
                          payload['customer_contact_email'],
                          "email@email")

    def test_capture(self):

        self.builder.capture("test_transaction_id", 1, "description",
                             "TL")
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['transaction_id'],
                          "test_transaction_id")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "CP")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")

        with self.assertRaises(KeyError):
             self.builder.payload['customer_first_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_last_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_contact_email']

    def test_capture_with_customer(self):
        customer = IyzicoCustomer("first", "last", "email@email")

        self.builder.capture("test_transaction_id", 1, "description",
                             "TL", customer)
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['transaction_id'],
                          "test_transaction_id")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "CP")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")
        self.assertEquals(self.builder.
                          payload['customer_first_name'],
                          "first")
        self.assertEquals(self.builder.payload['customer_last_name'],
                          "last")
        self.assertEquals(self.builder.
                          payload['customer_contact_email'],
                          "email@email")

    def test_refund(self):

        self.builder.refund("test_transaction_id", 1, "description",
                             "TL")
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['transaction_id'],
                          "test_transaction_id")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "RF")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")

        with self.assertRaises(KeyError):
             self.builder.payload['customer_first_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_last_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_contact_email']

    def test_refund_with_customer(self):
        customer = IyzicoCustomer("first", "last", "email@email")

        self.builder.refund("test_transaction_id", 1, "description",
                             "TL", customer)
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['transaction_id'],
                          "test_transaction_id")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "RF")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")
        self.assertEquals(self.builder.
                          payload['customer_first_name'],
                          "first")
        self.assertEquals(self.builder.payload['customer_last_name'],
                          "last")
        self.assertEquals(self.builder.
                          payload['customer_contact_email'],
                          "email@email")

    def test_reversal(self):

        self.builder.reversal("test_transaction_id", 1,
                              "description", "TL")
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['transaction_id'],
                          "test_transaction_id")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "RV")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")

        with self.assertRaises(KeyError):
             self.builder.payload['customer_first_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_last_name']
        with self.assertRaises(KeyError):
             self.builder.payload['customer_contact_email']

    def test_refund_with_customer(self):
        customer = IyzicoCustomer("first", "last", "email@email")

        self.builder.reversal("test_transaction_id", 1,
                              "description", "TL", customer)
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['transaction_id'],
                          "test_transaction_id")
        self.assertNotEquals(self.builder.payload['external_id'], "")
        self.assertEquals(self.builder.payload['type'], "RV")
        self.assertEquals(self.builder.payload['currency'], "TL")
        self.assertEquals(self.builder.payload['descriptor'],
                          "description")
        self.assertEquals(self.builder.
                          payload['customer_first_name'],
                          "first")
        self.assertEquals(self.builder.payload['customer_last_name'],
                          "last")
        self.assertEquals(self.builder.
                          payload['customer_contact_email'],
                          "email@email")

    def test_installment_matrix(self):
        self.builder.installment_matrix(1, "424242")
        self.assertEquals(self.builder.payload['amount'],
                          str(100*(int(1))))
        self.assertEquals(self.builder.payload['bin_number'],
                          "424242")
        with self.assertRaises(KeyError):
             self.builder.payload['response_mode']

if __name__ == '__main__':
    unittest.main()