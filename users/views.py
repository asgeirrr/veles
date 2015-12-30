from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .forms import LoginForm, RegistrationForm
from .models import User
from .token import decrypt_token


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
            self.request.session['fio_token'] = decrypt_token(user.token, password).decode('utf-8')
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(generic.RedirectView):

    def get(self, request, *args, **kwargs):
        del self.request.session['fio_token']
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


class RegistrationView(generic.CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')
