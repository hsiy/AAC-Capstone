from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *

class UpdateUserForm(forms.Form):
    aac = forms.BooleanField()
    department = forms.ModelChoiceField(queryset=Department.active_objects)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(max_length=30)
class UserUpdateUserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(max_length=30)