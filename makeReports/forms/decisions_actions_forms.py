from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *

class DecisionsActionsForm(forms.Form):
    decisionProcess = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Process")
    decisionMakers = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Makers")
    decisionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Timeline")
    dataUsed = forms.CharField(widget= forms.Textarea, max_length=3000, label="Data Used")
    actionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Action Timeline")