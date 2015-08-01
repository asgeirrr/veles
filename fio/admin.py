from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from fio.models import Fio


class FioDetailsInline(admin.StackedInline):
    model = Fio
    can_delete = False
    verbose_name_plural = _('fio details')


class UserAdmin(UserAdmin):
    inlines = (FioDetailsInline, )


# Re-register UserAdmin with FIO details inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
