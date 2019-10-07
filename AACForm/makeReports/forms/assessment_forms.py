from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *
class CreateNewAssessment(forms.Form):
    title = forms.CharField(widget= forms.Textarea, max_length=300)
    domain = forms.MultipleChoiceField(choices = (("Pe", "Performance"), ("Pr","Product"), ("Ex","Examination") ), widget=forms.CheckboxSelectMultiple)
    directMeasure = forms.ChoiceField(choices = ((True, "Direct Measure"), (False,"Indirect Measure")))
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    finalTerm = forms.ChoiceField(choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(widget= forms.Textarea, max_length=200)
    allStudents = forms.ChoiceField(choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(widget= forms.Textarea, max_length=200)
    frequency = forms.CharField(widget=forms.Textarea, max_length=100)
    threshold = forms.IntegerField(min_value=0,label="Proficiency Threshold: % of students that meet or exceed expectations")
    target = forms.IntegerField(min_value=0, label="Program Proficiency Target: % of students that achieve the proficiency threshold")
    def __init__(self,*args,**kwargs):
            sloQS = kwargs.pop('sloQS',None)
            super(CreateNewAssessment,self).__init__(*args,**kwargs)
            self.fields['slo'] = forms.ModelChoiceField(queryset=sloQS)

class ImportAssessmentForm(forms.Form):
    assessment = forms.ModelMultipleChoiceField(queryset=None)
    slo = forms.ModelChoiceField(queryset=None)
    def __init__(self, *args, **kwargs):
        assessChoices = kwargs.pop('assessChoices',None)
        sloChoices = kwargs.pop('slos',None)
        super(ImportAssessmentForm, self).__init__(*args, **kwargs)
        self.fields['assessment'].queryset = assessChoices
        self.fields['slo'].queryset = sloChoices

class EditNewAssessmentForm(forms.Form):
    title = forms.CharField(widget= forms.Textarea, max_length=300)
    domain = forms.MultipleChoiceField(choices = (("Pe", "Performance"), ("Pr","Product"), ("Ex","Examination") ), widget=forms.CheckboxSelectMultiple)
    directMeasure = forms.ChoiceField(choices = ((True, "Direct Measure"), (False,"Indirect Measure")))
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    finalTerm = forms.ChoiceField(choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(widget= forms.Textarea, max_length=200)
    allStudents = forms.ChoiceField(choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(widget= forms.Textarea, max_length=200)
    frequency = forms.CharField(widget=forms.Textarea, max_length=100)
    threshold = forms.IntegerField(min_value=0,label="Proficiency Threshold: % of students that meet or exceed expectations")
    target = forms.IntegerField(min_value=0, label="Program Proficiency Target: % of students that achieve the proficiency threshold")
    def __init__(self,*args,**kwargs):
            sloQS = kwargs.pop('sloQS',None)
            super(EditNewAssessmentForm,self).__init__(*args,**kwargs)
            self.fields['slo'] = forms.ModelChoiceField(queryset=sloQS)

class EditImportedAssessmentForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, max_length=1000, label="Description: ")
    finalTerm = forms.ChoiceField(choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(widget= forms.Textarea, max_length=200)
    allStudents = forms.ChoiceField(choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(widget= forms.Textarea, max_length=200)
    frequency = forms.CharField(widget=forms.Textarea, max_length=100)
    threshold = forms.IntegerField(min_value=0,label="Proficiency Threshold: % of students that meet or exceed expectations")
    target = forms.IntegerField(min_value=0, label="Program Proficiency Target: % of students that achieve the proficiency threshold")
    def __init__(self,*args,**kwargs):
            sloQS = kwargs.pop('sloQS',None)
            super(EditImportedAssessmentForm,self).__init__(*args,**kwargs)
            self.fields['slo'] = forms.ModelChoiceField(queryset=sloQS)

class ImportSupplementsForm(forms.Form):
    sup = forms.ModelChoiceField(queryset=None, label="Supplement Upload")
    def __init__(self, *args, **kwargs):
        supChoices = kwargs.pop('supChoices',None)
        super(ImportSupplementsForm, self).__init__(*args, **kwargs)
        self.fields['sup'].queryset = supChoices
