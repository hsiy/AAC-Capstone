from django import forms
from makeReports.models import *
from makeReports.choices import *
from django_summernote.widgets import SummernoteWidget
from .cleaners import CleanSummer
from django.core.exceptions import ValidationError
class CreateNewSLO(CleanSummer,forms.Form):
    text = forms.CharField(widget= forms.Textarea, label="SLO: ") 
    blooms = forms.ChoiceField(choices=BLOOMS_CHOICES, label="Highest Bloom's Taxonomy Level: ")
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.active_objects.all(), required=False,widget=forms.CheckboxSelectMultiple, label="Graduate-level Goals: ")
    summer_max_length = 600
    def __init__(self,*args,**kwargs):
        grad = kwargs.pop('grad',None)
        super(CreateNewSLO,self).__init__(*args,**kwargs)
        if not grad:
            del self.fields['gradGoals']
class ImportSLOForm(forms.Form):
    slo = forms.ModelMultipleChoiceField(queryset=None, label="SLOs to Import: ")
    importAssessments = forms.BooleanField(required=False,label="Also import assessments?")
    #of type SLOInReport
    def __init__(self, *args, **kwargs):
        sloChoices = kwargs.pop('sloChoices',None)
        super(ImportSLOForm, self).__init__(*args, **kwargs)
        self.fields['slo'].queryset = sloChoices
class EditNewSLOForm(CleanSummer,forms.Form):
    text = forms.CharField(widget= forms.Textarea, label="SLO: ")
    blooms = forms.ChoiceField(choices=BLOOMS_CHOICES, required=False, label="Highest Bloom's Taxonomy Level: ")
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.active_objects.all(), required=False,widget=forms.CheckboxSelectMultiple, label="Graduate-level Goals: ")
    
    summer_max_length = 600
    def __init__(self,*args,**kwargs):
        grad = kwargs.pop('grad',None)
        super(EditNewSLOForm,self).__init__(*args,**kwargs)
        if not grad:
            del self.fields['gradGoals']
class EditImportedSLOForm(CleanSummer,forms.Form):
    text = forms.CharField(widget= forms.Textarea, label="SLO: ")
    summer_max_length = 600
class Single2000Textbox(CleanSummer,forms.Form):
    text = forms.CharField(widget=SummernoteWidget(),label="")
    summer_max_length = 2000

class ImportStakeholderForm(forms.Form):
    stk = forms.ModelChoiceField(queryset=None, label="Stakeholder Communication Methods")
    def __init__(self, *args, **kwargs):
        stkChoices = kwargs.pop('stkChoices',None)
        super(ImportStakeholderForm, self).__init__(*args, **kwargs)
        self.fields['stk'].queryset = stkChoices
