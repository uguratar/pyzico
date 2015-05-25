# pyzico
### iyzico için python kütüphanesi.

### Kurulum
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ cp settings.dist.py settings.py
    $ python -m unittest -v test

İlk olarak oluşturduğunuz settings.py dosyasına Iyzico'dan aldığınız api_id ve api_secret parametrelerini yazmanız gerekmekte.

Iyzico api üzerinden "debit", "pre-authorization", "capture", "reversal", "refund" işlemlerini yapabilirsiniz.
Ayrıca kredi kartı bilgilerini saklayarak, kredi kartına ait token ile de debit işlemi yapabilirsiniz.

    
    from iyzico import Iyzico
    from iyzico_objects import IyzicoCard, IyzicoHTTPException, IyzicoValueException
    
    my_card = IyzicoCard("4242424242424242", "10", "2015", "000",
                         "Python Test")
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

Daha fazla örnek için <a href="https://github.com/uguratar/pyzico/blob/master/sample.py">sample.py</a> dosyasına göz atabilirsiniz.

### Todo
  * Testler yazılmalı
  * Taksit matrisini çıkartan installment_matrix metodu farklı bir hesapla  test edilmeli