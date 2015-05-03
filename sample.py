# coding=utf-8

from iyzico import Iyzico
from iyzico_objects import IyzicoCard, IyzicoCustomer, IyzicoCardToken

if __name__ == '__main__':
    my_card = IyzicoCard("4242424242424242", "10", "2015", "000",
                         "Python Test")

    my_customer = IyzicoCustomer("First Name", "Last Name",
                                 "email@email")

    my_token = IyzicoCardToken("str_card_token")

    payment = Iyzico()


    '''
    success, result = payment.debit_with_token(1, my_token,
                                               "Python card token",
                                               "TRY")

    success, result = payment.register_card(my_card)

    success, result = payment.delete_card(my_token)

    success, result = payment.pre_authorize(1, my_card,
                                            "Iyzico python library test",
                                            "TRY")

    success, result = payment.capture(1,
                                      "TRANSACTION ID",
                                      "Iyzico python library test",
                                      "TRY")

    success, result = payment.reversal(1, "TRANSACTION ID",
                                       "Iyzico python library test",
                                       "TRY")

    success, result = payment.refund(1, "TRANSACTION ID",
                                     "Iyzico python library test",
                                     "TRY")
    '''


    success, result = payment.debit(1, my_card,
                                    "Iyzico python library test",
                                    "TRY", my_customer, True)

    if success:
        if result.success:
            print result.mode
            print result.response
            print result.account
            print result.transaction
            print result.customer
            print result.card_token

        else:
            print result.response
            print result.response["error_message"]
            print result.response["request_id"]
            print result.response["error_code"]
    else:
        print result.response
        print result.response["error_message"]
        print result.response["request_id"]
        print result.response["error_code"]