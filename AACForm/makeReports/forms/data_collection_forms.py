from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *

class AddDataCollection(forms.Form):
    dataRange = forms.CharField(widget= forms.Textarea, max_length=500, label="Data Collection Range")
    numberStudents = forms.IntegerField(widget= forms.NumberInput, label="Number of Students Sampled")
    overallProficient = forms.IntegerField(widget= forms.NumberInput, label="Overall Number of Students Met/\nExceeded Threshold Proficiency")

class EditDataCollection(forms.Form):
    dataRange = forms.CharField(widget= forms.Textarea, max_length=500, label="Data Collection Range")
    numberStudents = forms.IntegerField(widget= forms.NumberInput, label="Number of Students Sampled")
    overallProficient = forms.IntegerField(widget= forms.NumberInput, label="Overall Percentage of Students Met/\nExceeded Threshold Proficiency")

class AddSubassessment(forms.Form):
    title = forms.CharField(widget=forms.TextInput, max_length=500, label="Subassessment Title")
    proficient = forms.IntegerField(widget= forms.NumberInput, label="Subassessment Percentage of Students Met/\nExceeded Threshold Proficiency")

class EditSubassessment(forms.Form):
    title = forms.CharField(widget=forms.TextInput, max_length=500, label="Subassessment Title")
    proficient = forms.IntegerField(widget= forms.NumberInput, label="Subassessment Percentage of Students Met/\nExceeded Threshold Proficiency")