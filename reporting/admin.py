from django.contrib import admin

from .models import Category, Keyword, Transaction

from utils.auth import AllowStaffMixin, FilterOwnObjectsMixin


@admin.register(Category)
class CategoryAdmin(FilterOwnObjectsMixin, AllowStaffMixin, admin.ModelAdmin):

    fields = ('name', 'monthly_limit')
    list_display = ('name', 'monthly_limit')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@admin.register(Keyword)
class KeywordAdmin(FilterOwnObjectsMixin, AllowStaffMixin, admin.ModelAdmin):

    list_display = ('word', 'category')


@admin.register(Transaction)
class TransactionAdmin(FilterOwnObjectsMixin, admin.ModelAdmin):

    readonly_fields = ('date', 'amount', 'account_number', 'bank_code', 'identification', 'recipient_message', 'kind')
    fields = readonly_fields + ('category',)
    list_display = fields

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True
