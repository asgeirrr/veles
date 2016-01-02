from collections import namedtuple
from datetime import date

import responses
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from reporting.fio import convert_transaction_to_django, convert_transactions_to_django, import_transactions
from reporting.models import Transaction

from users.tests.factories import UserFactory


class FioImportTestCase(TestCase):

    TEST_FIO_URL = 'https://www.fio.cz/ib_api/rest/periods/{token}/2000-01-01/{date_to}/transactions.json'
    TEST_TOKEN = 'testtoken'

    TEST_TRANSACTION_DICT = {
        'column8': {'id': 8, 'name': 'Typ', 'value': 'Bezhotovostní platba'},
        'column0': {'id': 0, 'name': 'Datum', 'value': '2016-01-01+0100'},
        'column14': {'id': 14, 'name': 'Měna', 'value': 'CZK'},
        'column25': {'id': 25, 'name': 'Komentář', 'value': 'Test note'},
        'column6': None,
        'column10': None,
        'column16': {'id': 16, 'name': 'Zpráva pro příjemce', 'value': 'Test receiver note'},
        'column3': {'id': 3, 'name': 'Kód banky', 'value': '0300'},
        'column18': None,
        'column9': None,
        'column12': {'id': 12, 'name': 'Název banky', 'value': 'Československá obchodní banka a.s.'},
        'column17': {'id': 17, 'name': 'ID pokynu', 'value': 23232323},
        'column26': None,
        'column2': {'id': 2, 'name': 'Protiúčet', 'value': '1234567890'},
        'column1': {'id': 1, 'name': 'Objem', 'value': -1943.0},
        'column22': {'id': 22, 'name': 'ID pohybu', 'value': 1232131},
        'column4': {'id': 4, 'name': 'KS', 'value': '2342'},
        'column7': {'id': 7, 'name': 'Uživatelská identifikace', 'value': 'Test note'},
        'column5': {'id': 5, 'name': 'VS', 'value': '30572247'}
    }

    TEST_ACCOUNT_STATEMENT = """{
            "accountStatement": {
                "info": {
                    "accountId":"1234567890",
                    "bankId":"2010",
                    "currency":"CZK",
                    "iban":"CZ3748374238474812214",
                    "bic":"FIOB743493",
                    "openingBalance":33333.3,
                    "closingBalance":44444.4,
                    "dateStart":"2015-12-25+0100",
                    "dateEnd":"2015-12-31+0100",
                    "yearList":null,
                    "idList":null,
                    "idFrom":999999997,
                    "idTo":999999998,
                    "idLastDownload":null
                },
                "transactionList": {
                    "transaction": [
                        {
                            "column22":{"value":999999997,"name":"ID pohybu","id":22},
                            "column0":{"value":"2015-12-27+0100","name":"Datum","id":0},
                            "column1":{"value":3333.00,"name":"Objem","id":1},
                            "column14":{"value":"CZK","name":"Měna","id":14},
                            "column2":{"value":"987654321","name":"Protiúčet","id":2},
                            "column10":{"value":"Blahož, Jan","name":"Název protiúčtu","id":10},
                            "column3":{"value":"2010","name":"Kód banky","id":3},
                            "column12":{"value":"Fio banka, a.s.","name":"Název banky","id":12},
                            "column4":null,
                            "column5":null,
                            "column6":null,
                            "column7":null,
                            "column16":{"value":"Test recipient message","name":"Zpráva pro příjemce","id":16},
                            "column8":{"value":"Příjem převodem uvnitř banky","name":"Typ","id":8},
                            "column9":null,
                            "column18":null,
                            "column25":{"value":"Test comment","name":"Komentář","id":25},
                            "column26":null,
                            "column17":{"value":999999997,"name":"ID pokynu","id":17}},
                        {
                            "column22":{"value":999999998,"name":"ID pohybu","id":22},
                            "column0":{"value":"2015-12-28+0100","name":"Datum","id":0},
                            "column1":{"value":-444.00,"name":"Objem","id":1},
                            "column14":{"value":"CZK","name":"Měna","id":14},
                            "column2":{"value":"1234567890","name":"Protiúčet","id":2},
                            "column10":null,
                            "column3":{"value":"3030","name":"Kód banky","id":3},
                            "column12":{"value":"Air Bank a.s.","name":"Název banky","id":12},
                            "column4":null,
                            "column5":null,
                            "column6":null,
                            "column7":{"value":"Test identification","name":"Uživatelská identifikace","id":7},
                            "column16":{"value":"Testing recipient message","name":"Zpráva pro příjemce","id":16},
                            "column8":{"value":"Bezhotovostní platba","name":"Typ","id":8},
                            "column9":{"value":"Sipkova, Ruzenka","name":"Provedl","id":9},
                            "column18":null,
                            "column25":{"value":"Test comment 2","name":"Komentář","id":25},
                            "column26":null,
                            "column17":{"value":999999998,"name":"ID pokynu","id":17}
                        }
                    ]
                }
            }
        }
    """

    def test_should_convert_transaction(self):
        transaction = convert_transaction_to_django(self.TEST_TRANSACTION_DICT)

        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.kind, Transaction.KIND_TRANSFER)
        self.assertEqual(transaction.date, date(2016, 1, 1))
        self.assertEqual(transaction.amount, -1943)
        self.assertEqual(transaction.account_number, '1234567890')
        self.assertEqual(transaction.bank_code, '0300')
        self.assertEqual(transaction.identification, 'Test note')
        self.assertIsNone(transaction.account_name)
        self.assertEqual(transaction.bank_name, 'Československá obchodní banka a.s.')
        self.assertEqual(transaction.currency, Transaction.CURRENCY_CZK)
        self.assertEqual(transaction.recipient_message, 'Test receiver note')

    def test_should_convert_transactions(self):
        transactions = convert_transactions_to_django(self.TEST_ACCOUNT_STATEMENT)

        self.assertEqual(len(transactions), 2)
        self.assertEqual(type(transactions[0]), Transaction)
        self.assertEqual(type(transactions[1]), Transaction)

    @responses.activate
    def test_should_import_transactions(self):
        responses.add(
            responses.GET,
            self.TEST_FIO_URL.format(token=self.TEST_TOKEN, date_to=date.today() - relativedelta(days=1)),
            body=self.TEST_ACCOUNT_STATEMENT, status=200
        )
        Request = namedtuple('Request', ['user', 'session'])
        request = Request(user=UserFactory(), session={'fio_token': self.TEST_TOKEN})
        import_transactions(request)
        self.assertEqual(Transaction.objects.count(), 2)
        request.user.refresh_from_db()
        self.assertEqual(request.user.last_sync, date.today())
