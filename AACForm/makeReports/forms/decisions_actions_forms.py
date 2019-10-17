from django import forms
from makeReports.models import *
from .cleaners import CleanSummer
from django_summernote.widgets import SummernoteWidget

class DecisionsActionsForm(forms.Form):
    decisionProcess = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Process")
    decisionMakers = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Makers")
    decisionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Timeline")
    dataUsed = forms.CharField(widget= forms.Textarea, max_length=3000, label="Data Used")
    actionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Action Timeline")
class DecActForm1Box(CleanSummer,forms.ModelForm):
    text = forms.CharField(widget=SummernoteWidget,label="")
    max_summer_length = 3000
    class Meta:
        model = DecisionsActions
        fields = ['text']