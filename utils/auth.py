class AllowStaffMixin(object):

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


class FilterOwnObjectsMixin(object):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
