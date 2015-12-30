from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['token']

    token = models.CharField(verbose_name=_('FIO token'), null=False, blank=False, max_length=255)
    last_sync = models.DateTimeField(verbose_name=_('last sync'), null=True, blank=True)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username
