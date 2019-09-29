from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, DetailView
from django.views.generic import RedirectView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin

class AdminHome(TemplateView, FormMixin):
    template_name = ""
    form_class = JustHitButton
    success_url = ""
    def form_valid(self, form):
        #generate this years reports
        return super(AdminHome, self).form_valid(form)
class CreateCollege(CreateView):
    model = College
    template_name = ""
    fields = ('name')
    success_url = ""
class DeleteCollege(DeleteView):
    model = College
    template_name = ""
    success_url = ""
class UpdateCollege(UpdateView):
    model = College
    template_name = ""
    fields = ('name')
    success_url = ""
class CreateDepartment(CreateView):
    model = Department
    fields = ('name', 'college')
    template_name = ""
    success_url = ""
class DeleteDepartment(DeleteView):
    model = Department
    template_name = ""
    success_url = ""
class UpdateDepartment(UpdateView):
    model = Department
    fields = ('name', 'college')
    template_name = ""
    success_url = ""
class CreateDegreeProgram(CreateView):
    model = DegreeProgram
    fields = ('name','level','department','cycle','startingYear')
    template_name = ""
    success_url = ""
class DeleteDegreeProgram(DeleteView):
    model = DegreeProgram
    template_name = ""
    success_url = ""
class UpdateDegreeProgram(UpdateView):
    model = DegreeProgram
    fields = ('name','level','department','cycle','startingYear')
    template_name = ""
    success_url = ""
class CreateReport(CreateView):
    model = Report
    form_class = CreateReportByDept
    template_name = ""
    success_url = ""
    def get_form_kwargs(self):
        kwargs = super(CreateReport, self).get_form_kwargs()
        kwargs.update({'dept': self.request.GET['dept']})
        return kwargs
class DeleteReport(DeleteView):
    model = Report
    template_name = ""
    success_url = ""




