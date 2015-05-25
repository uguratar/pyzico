import unittest

import settings
from iyzico_objects import IyzicoCustomer, IyzicoCardToken, \
    IyzicoSettings, IyzicoPayloadBuilder
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

if __name__ == '__main__':
    unittest.main()