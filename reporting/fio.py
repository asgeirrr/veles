import json
from datetime import date
from decimal import Decimal

import requests
from dateutil import parser
from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.utils.translation import ugettext

from reporting.models import Transaction


FIO_URL_PATTERN = 'https://www.fio.cz/ib_api/rest/periods/{token}/{date_from}/{date_to}/transactions.json'
DEFAULT_DATE_FROM = date(2000, 1, 1)

FIO_FIELD_MAPPING = {
    0: 'date',
    1: 'amount',
    2: 'account_number',
    3: 'bank_code',
    7: 'identification',
    8: 'kind',
    10: 'account_name',
    12: 'bank_name',
    14: 'currency',
    16: 'recipient_message',
}

FIO_KIND_MAPPING = {
    'Příjem převodem uvnitř banky': Transaction.KIND_TRANSFER,
    'Platba převodem uvnitř banky': Transaction.KIND_TRANSFER,
    'Vklad pokladnou': Transaction.KIND_CASH,
    'Výběr pokladnou': Transaction.KIND_CASH,
    'Vklad v hotovosti': Transaction.KIND_CASH,
    'Výběr v hotovosti': Transaction.KIND_CASH,
    'Platba': Transaction.KIND_TRANSFER,
    'Příjem': Transaction.KIND_TRANSFER,
    'Bezhotovostní platba': Transaction.KIND_TRANSFER,
    'Bezhotovostní příjem': Transaction.KIND_TRANSFER,
    'Platba kartou': Transaction.KIND_CARD,
    'Převod uvnitř konta': Transaction.KIND_TRANSFER,
    'Převod mezi bankovními konty (platba)': Transaction.KIND_TRANSFER,
    'Převod mezi bankovními konty (příjem)': Transaction.KIND_TRANSFER,
    'Neidentifikovaná platba z bankovního konta': Transaction.KIND_TRANSFER,
    'Neidentifikovaný příjem na bankovní konto': Transaction.KIND_TRANSFER,
    'Vlastní platba z bankovního konta': Transaction.KIND_TRANSFER,
    'Vlastní příjem na bankovní konto': Transaction.KIND_TRANSFER,
    'Vlastní platba pokladnou': Transaction.KIND_CASH,
    'Vlastní příjem pokladnou': Transaction.KIND_CASH,
    'Inkaso': Transaction.KIND_INSTALLMENT,
    'Inkaso ve prospěch účtu': Transaction.KIND_INSTALLMENT,
    'Inkaso z účtu': Transaction.KIND_INSTALLMENT,
    'Příjem inkasa z cizí banky': Transaction.KIND_INSTALLMENT,
}

FIO_CURRENCY_MAPPING = {
    'CZK': Transaction.CURRENCY_CZK,
    'EUR': Transaction.CURRENCY_EUR,
}

FIO_TO_PYTHON = {
    'date': lambda date_str: parser.parse(date_str[:-5]).date(),
    'amount': Decimal,
    'account_number': str,
    'bank_code': str,
    'identification': str,
    'kind': lambda kind: FIO_KIND_MAPPING.get(kind, Transaction.KIND_OTHER), # TODO,
    'account_name': str,
    'bank_name': str,
    'currency': lambda currency: FIO_CURRENCY_MAPPING.get(currency, Transaction.CURRENCY_CZK),
    'recipient_message': str,
}


def convert_transaction_to_django(transaction_dict):
    raw_dict_values = {FIO_FIELD_MAPPING[field['id']]: field['value'] for field in transaction_dict.values()
                       if field and field['id'] in FIO_FIELD_MAPPING.keys()}
    return Transaction(**{k: FIO_TO_PYTHON[k](v) for k, v in raw_dict_values.items()})

def convert_transactions_to_django(json_response):
    account_statement = json.loads(json_response)['accountStatement']
    transactions = account_statement['transactionList']['transaction']
    return [convert_transaction_to_django(t) for t in transactions]

def import_transactions(request):
    token = request.session.get('fio_token')
    if not token:
        raise KeyError(ugettext('FIO token not present in session.'))
    response = requests.get(FIO_URL_PATTERN.format(
        token=token,
        date_from=request.user.last_sync or DEFAULT_DATE_FROM,
        date_to=date.today() - relativedelta(days=1)
    ))

    if response.status_code == 200:
        transactions = convert_transactions_to_django(response.text)
        Transaction.objects.bulk_create(transactions)
        request.user.last_sync = date.today()
        request.user.save()
        return transactions
    else:
        messages.add_message(request, messages.ERROR, ugettext('Response code from FIO: {}').format(response.code))
        return []
