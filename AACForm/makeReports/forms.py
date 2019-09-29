from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from .choices import *
""" class AddMovieForm(ModelForm):
    class Meta:
        model=Movie
        fields=['movietitle','movieruntime','movierating','moviereleasedate','moviegenre','moviedescription','poster']
        labels={
            'movietitle':'Title',
            'movieruntime':"Runtime (minutes)",
            'movierating':'MPAA Rating',
            'moviereleasedate':"Release date",
            'moviegenre':"Genre",
            'moviedescription':"Description"
        }
        yearNow = datetime.now().year
        yearsT = (str(yearNow), str(yearNow+1),str(yearNow+2))+(tuple(map(str, range(1900,yearNow))))
        widgets = {'moviereleasedate':forms.SelectDateWidget(years=yearsT)
 """
class CreateNewSLO(forms.Form):
    text = forms.CharField(widget= forms.Textarea, max_length=600) 
    blooms = forms.ChoiceField(choices=BLOOMS_CHOICES)
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.objects.all(), required=False)
class ImportSLO(forms.Form):
    slo = forms.ModelMultipleChoiceField(queryset=None, to_field_name='sloText__goalText')
    #of type SLOInReport
    def __init__(self, *args, **kwargs):
        super(ImportSLO, self).__init__(*args, **kwargs)
        sloChoices = kwargs.pop('sloChoices',None)
        self.fields['slo'].queryset = sloChoices
class EditNewSLO(forms.Form):
    text = forms.CharField(widget= forms.Textarea, max_length=600)
    blooms = forms.ChoiceField(choices=BLOOMS_CHOICES, required=False)
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.objects.all(), required=False)
class EditImportedSLO(forms.Form):
    text = forms.CharField(widget= forms.Textarea, max_length=600)
class SLOsToStakeholderEntry(forms.Form):
    text = forms.CharField(max_length=2000, widget=forms.Textarea)