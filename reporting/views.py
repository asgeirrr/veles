from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView

from .fio import import_transactions
from .forms import DownloadTransactionsForm


class DashboardView(LoginRequiredMixin, FormView):
    template_name = 'dashboard.html'
    form_class = DownloadTransactionsForm
    success_url = reverse_lazy('dashboard')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        import_transactions(self.request)
        return super(DashboardView, self).form_valid(form)
