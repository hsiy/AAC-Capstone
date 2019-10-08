from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *

class SubmitReportForm(forms.Form):
    hidden = forms.CharField(max_length=5,widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        self.valid = kwargs.pop('valid')
        super(SubmitReportForm, self).__init__(*args, **kwargs)
    def clean(self):
      cleaned_data = super().clean()
      if not self.valid:
          raise forms.ValidationError("The minimum requirements for the report have not been fulfilled.")