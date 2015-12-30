from django import forms
from django.utils.translation import ugettext

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions


class DownloadTransactionsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DownloadTransactionsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FormActions(
                Submit('download', ugettext('Download transactions'), css_class='btn-primary')
            )
        )
