from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *
class SectionRubricForm(forms.Form):
    section_comment = forms.CharField(max_length=2000, required=False)
    def __init__(self, *args, **kwargs):
        rubricItems = kwargs.pop('rubricItems')
        super(SectionRubricForm, self).__init__(*args, **kwargs)
        i = 0
        for rI in rubricItems:
            self.fields['rI'+str(i)] = forms.ChoiceField(choices=RUBRIC_GRADES_CHOICES, widget=forms.RadioSelect,label=rI.text,required=False)
            #required=False so allow partial completion of the form
            i+=1