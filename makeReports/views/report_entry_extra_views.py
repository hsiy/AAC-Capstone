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

class ReportFirstPage(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Report
    fields = ['author','date_range_of_reported_data']
    template_name = "makeReports/ReportEntryExtras/first_page.html"
    labels = {
        'author':'Person preparing the report'
    }
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(ReportFirstPage,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class FinalReportSupplements(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ReportSupplement
    template_name = ""
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(FinalReportSupplements,self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        return ReportSupplement.objects.filter(report=self.report)
    def get_success_url(self):
        #return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
        #to be replaced with preview&submit page
        return ""
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class AddEndSupplements(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ReportSupplement
    template_name = ""
    fields = ['supplement']
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AddEndSupplements,self).dispatch(request,*args,**kwargs)
    def form_valid(self,form):
        form.instance.report = self.report
        return super(AddEndSupplements,self).form_valid(form)
    def get_success_url(self):
        #return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
        #to be replaced with FinalReportSupplement thing
        return ""
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
