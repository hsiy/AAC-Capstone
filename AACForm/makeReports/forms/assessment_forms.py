from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_summernote.widgets import SummernoteWidget
from .cleaners import cleanText
from django.core.exceptions import ValidationError
from makeReports.choices import FREQUENCY_CHOICES
from .widgets import SLOChoicesJSWidget

class CreateNewAssessment(forms.Form):
    slo = forms.ModelChoiceField(label="SLO",queryset=None, widget=SLOChoicesJSWidget)
    title = forms.CharField(max_length=300)
    description = forms.CharField(widget=SummernoteWidget(),label="Describe How Measure Aligns with SLO")
    domain = forms.MultipleChoiceField(choices = (("Pe", "Performance"), ("Pr","Product"), ("Ex","Examination") ), widget=forms.CheckboxSelectMultiple,required=False)
    directMeasure = forms.ChoiceField(label="Direct measure",choices = ((True, "Direct Measure"), (False,"Indirect Measure")))
    finalTerm = forms.ChoiceField(label="Point in Program Assessment is Administered",choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(label="Where does the assessment occur",widget= SummernoteWidget())
    allStudents = forms.ChoiceField(label="Population Measured",choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(label="Describe what students are sampled (if not all)",widget= SummernoteWidget(), required=False)
    frequencyChoice = forms.ChoiceField(label="Frequency of Data Collection", choices=FREQUENCY_CHOICES)
    frequency = forms.CharField(label="Describe frequency if other",widget=SummernoteWidget(),required=False)
    threshold = forms.CharField(max_length=500,label="Proficiency Threshold")
    target = forms.IntegerField(min_value=0, label="Program Proficiency Target: % of students that achieve the proficiency threshold")
    
    def __init__(self,*args,**kwargs):
        sloQS = kwargs.pop('sloQS',None)
        super(CreateNewAssessment,self).__init__(*args,**kwargs)
        self.fields['slo'].queryset = sloQS
    def clean_description(self):
        data = self.cleaned_data['description']
        max_length = 1000
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
    def clean_where(self):
        data = self.cleaned_data['where']
        max_length = 500
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned   
    def clean_sampleDescription(self):
        data = self.cleaned_data['sampleDescription']
        max_length = 500
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
    def clean_frequency(self):
        data = self.cleaned_data['frequency']
        max_length = 100
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
class ImportAssessmentForm(forms.Form):
    assessment = forms.ModelMultipleChoiceField(queryset=None)
    slo = forms.ModelChoiceField(label="SLO",queryset=None)
    def __init__(self, *args, **kwargs):
        assessChoices = kwargs.pop('assessChoices',None)
        sloChoices = kwargs.pop('slos',None)
        super(ImportAssessmentForm, self).__init__(*args, **kwargs)
        self.fields['assessment'].queryset = assessChoices
        self.fields['slo'].queryset = sloChoices

class EditNewAssessmentForm(CreateNewAssessment):
    def __init__(self,*args,**kwargs):
        sloQS = kwargs.pop('sloQS',None)
        super(EditNewAssessmentForm,self).__init__(*args,**kwargs)
        self.fields['slo'].queryset = sloQS

class EditImportedAssessmentForm(EditNewAssessmentForm):
    title = None
    domain = None
    directMeasure = None


class ImportSupplementsForm(forms.Form):
    sup = forms.ModelChoiceField(queryset=None, label="Supplement Upload")
    def __init__(self, *args, **kwargs):
        supChoices = kwargs.pop('supChoices',None)
        super(ImportSupplementsForm, self).__init__(*args, **kwargs)
        self.fields['sup'].queryset = supChoices
