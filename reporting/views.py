from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DownloadTransactionsForm
from .fio import download_transactions


class DashboardView(LoginRequiredMixin, FormView):
    template_name = 'dashboard.html'
    form_class = DownloadTransactionsForm
    success_url = reverse_lazy('dashboard')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        download_transactions(self.request.user)
        return super(DashboardView, self).form_valid(form)
