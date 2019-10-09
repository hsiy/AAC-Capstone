from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *

class UpdateUserForm(forms.Form):
    aac = forms.BooleanField(label="AAC member",required=False)
    department = forms.ModelChoiceField(queryset=Department.active_objects, required=False)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(max_length=30)
class UserUpdateUserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(max_length=30)
class CreateDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'college']
    def __init__(self,*args,**kwargs):
        super(CreateDepartmentForm,self).__init__(*args,**kwargs)
        self.fields['college'].queryset=College.active_objects.all()
class GenerateReports(forms.Form):
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.order_by('-date'))
class MakeNewAccount(UserCreationForm):
    isaac = forms.BooleanField(required=False, label="Account for AAC member?")
    department = forms.ModelChoiceField(queryset=Department.active_objects, label="Department", required=False)
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