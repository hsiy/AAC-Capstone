from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *
class CreateNewAssessment(forms.Form):
    title = forms.CharField(widget= forms.Textarea, max_length=300)
    domain = forms.MultipleChoiceField(choices = DOMAIN_CHOICES)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    finalTerm = forms.ChoiceField(choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(widget= forms.Textarea, max_length=200)
    allStudents = forms.ChoiceField(choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(widget= forms.Textarea, max_length=200)
    frequency = forms.CharField(widget=forms.Textarea, max_length=100)
    threshold = forms.IntegerField(min_value=0,label="Proficiency Threshold: % of students that meet or exceed expectations")
    target = forms.IntegerField(min_value=0, label="Program Proficiency Target: % of students that achieve the proficiency threshold")

class ImportAssessment(forms.Form):
    asessessment = forms.ModelMultipleChoiceField(queryset=None, to_field_name='assessment__title')
    def __init__(self, *args, **kwargs):
        assessChoices = kwargs.pop('assessChoices',None)
        super(ImportAssessment, self).__init__(*args, **kwargs)
        self.fields['assessment'].queryset = assessChoices

class EditNewAssessment(forms.Form):
    title = forms.CharField(widget= forms.Textarea, max_length=300)
    domain = forms.MultipleChoiceField(choices = DOMAIN_CHOICES)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    finalTerm = forms.ChoiceField(choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(widget= forms.Textarea, max_length=200)
    allStudents = forms.ChoiceField(choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(widget= forms.Textarea, max_length=200)
    frequency = forms.CharField(widget=forms.Textarea, max_length=100)
    threshold = forms.IntegerField(min_value=0,label="Proficiency Threshold: % of students that meet or exceed expectations")
    target = forms.IntegerField(min_value=0, label="Program Proficiency Target: % of students that achieve the proficiency threshold")

class EditImportedAssessment(forms.Form):
    description = forms.CharField(widget=forms.Textarea, max_length=1000, label="Description: ")
    finalTerm = forms.ChoiceField(choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(widget= forms.Textarea, max_length=200)
    allStudents = forms.ChoiceField(choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(widget= forms.Textarea, max_length=200)
    frequency = forms.CharField(widget=forms.Textarea, max_length=100)
    threshold = forms.IntegerField(min_value=0,label="Proficiency Threshold: % of students that meet or exceed expectations")
    target = forms.IntegerField(min_value=0, label="Program Proficiency Target: % of students that achieve the proficiency threshold")

class UploadSupplement(forms.Form):
    pass

class ImportSupplements(forms.Form):
    sup = forms.ModelChoiceField(queryset=None, label="Supplement Upload")
    def __init__(self, *args, **kwargs):
        supChoices = kwargs.pop('supChoices',None)
        super(ImportSupplements, self).__init__(*args, **kwargs)
        self.fields['sup'].queryset = supChoices
