from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext as _, ugettext

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

from .models import User
from .token import encrypt_token


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            FormActions(
                Submit('login', _('Login'), css_class='btn-primary')
            )

        )


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            'token',
            FormActions(
                Submit('register', ugettext('Register'), css_class='btn-primary')
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['token'] = encrypt_token(cleaned_data['token'], cleaned_data['password1'])
        return cleaned_data

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'token')
