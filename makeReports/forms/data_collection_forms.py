from django import forms
from makeReports.models import *
from makeReports.choices import *
from django_summernote.widgets import SummernoteWidget
from .cleaners import CleanSummer

class AddDataCollection(forms.Form):
    dataRange = forms.CharField(widget= forms.Textarea, max_length=500, label="Data Collection Range")
    numberStudents = forms.IntegerField(widget= forms.NumberInput, label="Number of Students Sampled")
    overallProficient = forms.IntegerField(widget= forms.NumberInput, label="Overall Number of Students Met/Exceeded Threshold Proficiency")

class EditDataCollection(forms.Form):
    dataRange = forms.CharField(widget= forms.Textarea, max_length=500, label="Data Collection Range")
    numberStudents = forms.IntegerField(widget= forms.NumberInput, label="Number of Students Sampled")
    overallProficient = forms.IntegerField(widget= forms.NumberInput, label="Overall Percentage of Students Met/Exceeded Threshold Proficiency")

class AddSubassessment(forms.Form):
    title = forms.CharField(widget=forms.TextInput, max_length=500, label="Subassessment Title")
    proficient = forms.IntegerField(widget= forms.NumberInput, label="Subassessment Percentage of Students Met/Exceeded Threshold Proficiency")

class EditSubassessment(forms.Form):
    title = forms.CharField(widget=forms.TextInput, max_length=500, label="Subassessment Title")
    proficient = forms.IntegerField(widget= forms.NumberInput, label="Subassessment Percentage of Students Met/Exceeded Threshold Proficiency")

class SLOStatusForm(forms.Form):
    status = forms.ChoiceField(choices=SLO_STATUS_CHOICES, label="SLO Status: ")

class ResultCommunicationForm(CleanSummer,forms.Form):
    text = forms.CharField(
        widget=SummernoteWidget(), 
        label="Describe how results are communicated within the program. Address each SLO."
        )
    summer_max_length = 3000