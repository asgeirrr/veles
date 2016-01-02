from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):

    name = models.CharField(verbose_name=_('name'), null=False, blank=False, max_length=255)
    monthly_limit = models.PositiveIntegerField(verbose_name=_('monthly limit'), null=True, blank=True)


class Keyword(models.Model):

    category = models.ForeignKey(Category, verbose_name=_('category'), null=False, blank=False, related_name='keywords')
    word = models.CharField(verbose_name=_('word'), null=False, blank=False, max_length=255)


class Transaction(models.Model):

    CURRENCY_CZK = 1
    CURRENCY_EUR = 2

    CURRENCIES = (
        (CURRENCY_CZK, _('CZK')),
        (CURRENCY_EUR, _('EUR')),
    )

    KIND_TRANSFER = 1
    KIND_CARD = 2
    KIND_INSTALLMENT = 3
    KIND_CASH = 4
    KIND_OTHER = 5

    KINDS = (
        (KIND_TRANSFER, _('bank transfer')),
        (KIND_CARD, _('card')),
        (KIND_INSTALLMENT, _('installment')),
        (KIND_CASH, _('cash')),
        (KIND_OTHER, _('other')),
    )

    date = models.DateField(verbose_name=_('date'), null=False, blank=False)
    amount = models.DecimalField(verbose_name=_('amount'), decimal_places=2, max_digits=12, null=False, blank=False)
    account_number = models.CharField(verbose_name=_('account number'), max_length=18, null=True, blank=True)
    bank_code = models.CharField(verbose_name=_('bank code'), max_length=6, null=True, blank=True)
    identification = models.CharField(verbose_name=_('identification'), max_length=255, null=True, blank=True)
    kind = models.PositiveSmallIntegerField(verbose_name=_('kind'), choices=KINDS, default=KIND_OTHER,
                                            null=False, blank=False)
    account_name = models.CharField(verbose_name=_('account name'), max_length=255, null=True, blank=True)
    bank_name = models.CharField(verbose_name=_('bank name'), max_length=255, null=True, blank=True)
    currency = models.PositiveSmallIntegerField(verbose_name=_('currency'), choices=CURRENCIES, null=False, blank=False)
    recipient_message = models.CharField(verbose_name=_('recipient message'), max_length=255, null=True, blank=True)

    category = models.ForeignKey(Category, verbose_name=_('category'), null=True, blank=True,
                                 related_name='transactions')
