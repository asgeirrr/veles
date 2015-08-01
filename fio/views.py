from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from fio.forms import LoginForm, RegistrationForm


class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(generic.RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        # TODO delete FIO token from session or the whole session
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


class RegistrationView(generic.CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')
