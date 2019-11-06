"""
File contains forms related to inputting data points
"""
from django import forms
from makeReports.models import *
from makeReports.choices import *
from django_summernote.widgets import SummernoteWidget
from .cleaners import CleanSummer


class AddDataCollection(forms.Form):
    """
    Form to add data
    """
    dataRange = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class':'form-control col-6'}), label="Data Collection Range")
    numberStudents = forms.IntegerField(widget= forms.NumberInput(attrs={'class':'form-control col-6'}), label="Number of Students Sampled")
    overallProficient = forms.IntegerField(widget= forms.NumberInput(attrs={'class':'form-control col-3','addon_after':'%'}), label="Percentage of Students Met/Exceeded Threshold Proficiency")

class AddSubassessment(forms.Form):
    """
    Form to add sub-assessment
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-6'}), max_length=500, label="Subassessment Title")
    proficient = forms.IntegerField(widget= forms.NumberInput(attrs={'class':'form-control col-6'}), label="Subassessment Percentage of Students Met/Exceeded Threshold Proficiency")

class EditSubassessment(forms.Form):
    """
    Form to edit sub-assessment
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-6'}), max_length=500, label="Subassessment Title")
    proficient = forms.IntegerField(widget= forms.NumberInput(attrs={'class':'form-control col-6'}), label="Subassessment Percentage of Students Met/Exceeded Threshold Proficiency")

class SLOStatusForm(forms.Form):
    """
    Form to update SLO status
    """
    status = forms.ChoiceField(choices=SLO_STATUS_CHOICES, label="SLO Status: ", widget=forms.Select(attrs={'class':'form-control col-4'}))

class ResultCommunicationForm(CleanSummer,forms.Form):
    """
    Form to add how results are communicated
    """
    text = forms.CharField(
        widget=SummernoteWidget(attrs={'style':'width:750px'}), 
        label="Describe how results are communicated within the program. Address each SLO."
        )
    summer_max_length = 3000
class AssessmentAggregateForm(forms.ModelForm):
    class Meta:
        model = AssessmentAggregate
        fields = ['aggregate_proficiency']
        widgets = {
            'aggregate_proficiency': forms.NumberInput(attrs={'class':'form-control col-3','addon_after':"%"})
        }
