# coding=utf-8

from iyzico import Iyzico
from iyzico_objects import IyzicoCard, IyzicoCustomer, \
    IyzicoCardToken, IyzicoHTTPException, IyzicoValueException

if __name__ == '__main__':
    my_card = IyzicoCard("4242424242424242", "10", "2015", "000",
                         "Python Test")

    my_customer = IyzicoCustomer("First Name", "Last Name",
                                 "email@email")

    payment = Iyzico()

    try:
        result = payment.debit_with_installment(6.6612132, my_card,
                                        "Installment "
                                        "Iyzico python library test",
                                        "TRY", my_customer, True, 6)

        if result.success:
            print result.transaction_state
            print result.transaction_id
            print result.reference_id
            print result.request_id
            print result.card_token
            my_token = IyzicoCardToken(result.card_token)

        else:
            print result.error_code
            print result.error_message
    except (IyzicoHTTPException, IyzicoValueException) as ex:
        print ex



    '''result = payment.debit_with_token(1, my_token,
                                      "Python debit with "
                                      "card token",
                                      "TRY")'''

    '''result = payment.register_card(my_card)

    result = payment.delete_card(my_token)'''

    '''result2 = payment.pre_authorize(1, my_card,
                                            "Iyzico python library test",
                                            "TRY")
    print result2.success

    result3 = payment.capture(1, result2.transaction_id,
                             "Iyzico python library test",
                             "TRY")
    print result3.success
    result4 = payment.reversal(1, result.transaction_id,
                                       "Iyzico python library test",
                                       "TRY")
    print result4.success

    result5 = payment.refund(1, result3.transaction_id,
                                     "Iyzico python library test",
                                     "TRY")
    print result5.success'''





