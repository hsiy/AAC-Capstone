from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_summernote.widgets import SummernoteWidget
from .cleaners import cleanText
from django.core.exceptions import ValidationError
from makeReports.choices import FREQUENCY_CHOICES
from .widgets import SLOChoicesJSWidget
"""
Contains forms related to inputting assessments
"""
class CreateNewAssessment(forms.Form):
    """
    Form to create new assessment
    """
    slo = forms.ModelChoiceField(label="SLO",queryset=None, widget=SLOChoicesJSWidget)
    title = forms.CharField(max_length=300)
    description = forms.CharField(widget=SummernoteWidget(attrs={'style':'width:750px'}),label="Describe How Measure Aligns with SLO")
    domain = forms.MultipleChoiceField(choices = (("Pe", "Performance"), ("Pr","Product"), ("Ex","Examination") ), widget=forms.CheckboxSelectMultiple,required=False)
    directMeasure = forms.ChoiceField(label="Direct measure",choices = ((True, "Direct Measure"), (False,"Indirect Measure")))
    finalTerm = forms.ChoiceField(label="Point in Program Assessment is Administered",choices = ((True, "In final term"), (False, "In final year")))
    where = forms.CharField(label="Where does the assessment occur",widget= SummernoteWidget(attrs={'style':'width:750px'}))
    allStudents = forms.ChoiceField(label="Population Measured",choices = ((True, "All Students"), (False,"Sample of Students")))
    sampleDescription = forms.CharField(label="Describe what students are sampled (if not all)",widget= SummernoteWidget(attrs={'style':'width:750px'}), required=False)
    frequencyChoice = forms.ChoiceField(label="Frequency of Data Collection", choices=FREQUENCY_CHOICES)
    frequency = forms.CharField(label="Describe frequency if other",widget=SummernoteWidget(attrs={'style':'width:750px'}),required=False)
    threshold = forms.CharField(max_length=500,label="Proficiency Threshold")
    target = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'addon_after':'%'}), label="Program Proficiency Target: Percentage of students that achieve the proficiency threshold")
    
    def __init__(self,*args,**kwargs):
        """
        Initializes form, including setting SLO options to passed QuerySet

        Keyword Args:
            sloQS (QuerySet): SLOs to be picked from (generally those within report)
        """
        sloQS = kwargs.pop('sloQS',None)
        super(CreateNewAssessment,self).__init__(*args,**kwargs)
        self.fields['slo'].queryset = sloQS
    def clean_description(self):
        """
        Cleans out malicious or excess (from copying/pasting from Word) meta-data from rich text of the description

        Returns:
            str : cleaned rich text
        """
        data = self.cleaned_data['description']
        max_length = 1000
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
    def clean_where(self):
        """
        Cleans out malicious or excess (from copying/pasting from Word) meta-data from rich text of the where field

        Returns:
            str : cleaned rich text
        """
        data = self.cleaned_data['where']
        max_length = 500
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned   
    def clean_sampleDescription(self):
        """
        Cleans out malicious or excess (from copying/pasting from Word) meta-data from rich text of the sample description

        Returns:
            str : cleaned rich text
        """
        data = self.cleaned_data['sampleDescription']
        max_length = 500
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
    def clean_frequency(self):
        """
        Cleans out malicious or excess (from copying/pasting from Word) meta-data from rich text of the frequency

        Returns:
            str : cleaned rich text
        """
        data = self.cleaned_data['frequency']
        max_length = 100
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
class ImportAssessmentForm(forms.Form):
    """
    Form to import pre-existing assessment
    """
    assessment = forms.ModelMultipleChoiceField(queryset=None)
    slo = forms.ModelChoiceField(label="SLO",queryset=None)
    def __init__(self, *args, **kwargs):
        """
        Initializes form, sets assessment and SLO choices to passed sets

        Keyword Args:
            assessChoices (QuerySet): assessment choices
            sloChoices (QuerySet): SLO choices
        """
        assessChoices = kwargs.pop('assessChoices',None)
        sloChoices = kwargs.pop('slos',None)
        super(ImportAssessmentForm, self).__init__(*args, **kwargs)
        self.fields['assessment'].queryset = assessChoices
        self.fields['slo'].queryset = sloChoices

class EditNewAssessmentForm(CreateNewAssessment):
    """
    Form to edit new assessment (no restrictions)
    """
    def __init__(self,*args,**kwargs):
        """
        Sets SLOs choices to passed set
        
        Keyword Args:
            sloQS (QuerySet): set of SLOs to choose from
        """
        sloQS = kwargs.pop('sloQS',None)
        super(EditNewAssessmentForm,self).__init__(*args,**kwargs)
        self.fields['slo'].queryset = sloQS

class EditImportedAssessmentForm(EditNewAssessmentForm):
    """
    Edit imported assessment form (cannot change title, domain, or direct measure)
    """
    title = None
    domain = None
    directMeasure = None


class ImportSupplementsForm(forms.Form):
    """
    Import supplement for assessment form
    """
    sup = forms.ModelChoiceField(queryset=None, label="Supplement Upload")
    def __init__(self, *args, **kwargs):
        """
        Initialize form, with setting the supplement choices

        Keyword Args:
            supChoices (QuerySet): supplements to choose from
        """
        supChoices = kwargs.pop('supChoices',None)
        super(ImportSupplementsForm, self).__init__(*args, **kwargs)
        self.fields['sup'].queryset = supChoices
