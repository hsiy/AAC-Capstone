"""
File contains forms related to inputting decisions/actions
"""
from django import forms
from makeReports.models import *
from .cleaners import CleanSummer
from django_summernote.widgets import SummernoteWidget

class DecActForm1Box(CleanSummer,forms.ModelForm):
    """
    Form to add/edit decision/actions without sub-boxes
    """
    text = forms.CharField(widget=SummernoteWidget(attrs={'style':'width:750px'}),label="")
    summer_max_length = 3000
    class Meta:
        """
        Defines the model type and fields for the ModelForm superclass
        to use to build the form
        """
        model = DecisionsActions
        fields = ['text']