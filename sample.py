# coding=utf-8

from iyzico import Iyzico
from iyzico_objects import IyzicoCard, IyzicoCustomer,\
     IyzicoCardToken, IyzicoHTTPException, IyzicoValueException

if __name__ == '__main__':
    my_card = IyzicoCard("4242424242424242", "10", "2015", "000",
                         "Python Test")

    my_customer = IyzicoCustomer("First Name", "Last Name",
                                 "email@email")

    my_token = IyzicoCardToken("str_card_token")

    payment = Iyzico()

    try:
        result = payment.debit(1, my_card,
                                        "Iyzico python library test",
                                        "TRY", my_customer, True)
        if result.success:
            print result.transaction_state
            print result.transaction_id
            print result.reference_id
            print result.request_id
        else:
            print result.error_code
            print result.error_message
    except (IyzicoHTTPException, IyzicoValueException) as ex:
        print ex

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



