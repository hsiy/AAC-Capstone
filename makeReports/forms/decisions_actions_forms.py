from django import forms
from makeReports.models import *
from .cleaners import CleanSummer
from django_summernote.widgets import SummernoteWidget
"""
File contains forms related to inputting decisions/actions
"""
class DecisionsActionsForm(forms.Form):
    """
    Form to add or edit decisions/actions with 5 sub text boxes
    """
    decisionProcess = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Process")
    decisionMakers = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Makers")
    decisionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Timeline")
    dataUsed = forms.CharField(widget= forms.Textarea, max_length=3000, label="Data Used")
    actionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Action Timeline")
class DecActForm1Box(CleanSummer,forms.ModelForm):
    """
    Form to add/edit decision/actions without sub-boxes
    """
    text = forms.CharField(widget=SummernoteWidget(attrs={'style':'width:750px'}),label="")
    summer_max_length = 3000
    class Meta:
        model = DecisionsActions
        fields = ['text']