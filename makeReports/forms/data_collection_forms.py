from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *

class AddDataCollection(forms.Form):
    dataRange = forms.CharField(widget= forms.Textarea, max_length=500)
    numberStudents = forms.IntegerField(widget= forms.NumberInput)
    overallProficient = forms.IntegerField(widget= forms.NumberInput)

class EditDataCollection(forms.Form):
    dataRange = forms.CharField(widget= forms.Textarea, max_length=500)
    numberStudents = forms.IntegerField(widget= forms.NumberInput)
    overallProficient = forms.IntegerField(widget= forms.NumberInput)