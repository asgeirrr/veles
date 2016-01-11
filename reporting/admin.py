from django.contrib import admin

from .models import Category, Keyword, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    fields = ('name', 'monthly_limit')
    list_display = ('name', 'monthly_limit')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    list_display = ('word', 'category')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(category__user=request.user)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    readonly_fields = ('date', 'amount', 'account_number', 'bank_code', 'identification', 'recipient_message', 'kind')
    fields = readonly_fields + ('category',)
    list_display = fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False
