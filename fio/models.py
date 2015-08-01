from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Fio(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(verbose_name=_('FIO token'), blank=True, max_length=255)

