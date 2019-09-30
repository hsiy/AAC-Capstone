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
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.objects.all(), required=False,widget=forms.CheckboxSelectMultiple)
class ImportSLOForm(forms.Form):
    slo = forms.ModelMultipleChoiceField(queryset=None)
    #of type SLOInReport
    def __init__(self, *args, **kwargs):
        sloChoices = kwargs.pop('sloChoices',None)
        super(ImportSLOForm, self).__init__(*args, **kwargs)
        self.fields['slo'].queryset = sloChoices
class EditNewSLOForm(forms.Form):
    text = forms.CharField(widget= forms.Textarea, max_length=600)
    blooms = forms.ChoiceField(choices=BLOOMS_CHOICES, required=False)
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.objects.all(), required=False,widget=forms.CheckboxSelectMultiple)
class EditImportedSLOForm(forms.Form):
    text = forms.CharField(widget= forms.Textarea, max_length=600)
class Single2000Textbox(forms.Form):
    text = forms.CharField(max_length=2000, widget=forms.Textarea)
class CreateReportByDept(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['year', 'degreeProgram'] 
    def __init__(self,*args,**kwargs):
        dept = Department.objects.get(pk=kwargs.pop('dept'))
        super(CreateReportByDept, self).__init__(*args, **kwargs)
        self.fields['degreeProgram'].queryset = DegreeProgram.objects.filter(department=dept)
class CreateDPByDept(forms.ModelForm):   
    class Meta:
        model = DegreeProgram
        fields = ['name','level','cycle','startingYear']
class JustHitButton(forms.Form):
    nothing = forms.CharField( required=False, initial="nothing")
class CreateDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'college']
class ImportStakeholderForm(forms.Form):
    stk = forms.ModelChoiceField(queryset=None)
    def __init__(self, *args, **kwargs):
        stkChoices = kwargs.pop('stkChoices',None)
        super(ImportStakeholderForm, self).__init__(*args, **kwargs)
        self.fields['stk'].queryset = stkChoices
class MakeNewAccount(UserCreationForm):
    isaac = forms.BooleanField(required=False, label="Account for AAC member?")
    department = forms.ModelChoiceField(queryset=Department.objects, label="Department", required=False)
    class Meta:
        model = User
        fields = ['email','username','password1','password2','isaac','first_name','last_name']
    def save(self, commit=True):
        user = super(MakeNewAccount, self).save(commit=True)
        profile = user.profile
        profile.aac = self.cleaned_data['isaac']
        profile.department=self.cleaned_data['department']
        user.save()
        profile.save()
        return user, profile
