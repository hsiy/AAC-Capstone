from django import forms
from makeReports.models import *
from makeReports.choices import *
from django_summernote.widgets import SummernoteWidget
from .cleaners import cleanText
from django.core.exceptions import ValidationError


class SectionRubricForm(forms.Form):
    def __init__(self, *args, **kwargs):
        rubricItems = kwargs.pop('rubricItems')
        super(SectionRubricForm, self).__init__(*args, **kwargs)
        for rI in rubricItems:
            self.fields['rI'+str(rI.pk)] = forms.ChoiceField(choices=RUBRIC_GRADES_CHOICES, widget=forms.RadioSelect,label=rI.text,required=False)
            #required=False so allow partial completion of the 
        self.fields['section_comment'] = forms.CharField(
            required=False, 
            widget=SummernoteWidget(
                attrs={'summernote': {'width' : '415px'}}))
    def clean_section_comment(self):
        data = self.cleaned_data['section_comment']
        max_length = 2000
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
class RubricItemForm(forms.ModelForm):
    class Meta:
        model = RubricItem
        fields = ['text','abbreviation','section','order','DMEtext','MEtext','EEtext']
        labels = {
            'text':'Category text',
            'abbreviation':'Abbreviation (optional)',
            'section':'Section number',
            'order':'Order position of item (lower numbers will be displayed first) (optional)',
            'DMEtext':'Did not meet expectations text',
            'MEtext':"Met expectations with concerns text",
            'EEtext':'Met expectations text'
        }
        widgets ={
            'text': SummernoteWidget(),
            'DMEtext':SummernoteWidget(),
            'MEtext':SummernoteWidget(),
            'EEtext':SummernoteWidget()
        }
    def clean_text(self):
        data = self.cleaned_data['text']
        max_length = 1000
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
    def clean_DMEtext(self):
        data = self.cleaned_data['DMEtext']
        max_length = 1000
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
    def clean_MEtext(self):
        data = self.cleaned_data['MEtext']
        max_length = 1000
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
    def clean_EEtext(self):
        data = self.cleaned_data['EEtext']
        max_length = 1000
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
class DuplicateRubricForm(forms.Form):
    #rubToDup = forms.ModelChoiceField(label="Rubric to duplicate",queryset=Rubric.objects,widget=forms.HiddenInput(),required=False)
    new_name = forms.CharField(max_length=1000)
class SubmitGrade(forms.Form):
    hidden = forms.CharField(max_length=5,widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        self.valid = kwargs.pop('valid')
        super(SubmitGrade, self).__init__(*args, **kwargs)
    def clean(self):
      super().clean()
      if not self.valid:
          raise forms.ValidationError("Not all rubric items have been graded.")