from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin
from django.template.defaulttags import register
class AACOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeptOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeptAACMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        dept = (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
class DeptReportMixin(DeptOnlyMixin):
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeptReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rpt'] = self.report
        return context
class AACReportMixin(AACOnlyMixin):
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeptReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rpt'] = self.report
        return context