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
from makeReports.views.helperFunctions.section_context import *

class ReportFirstPage(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Report
    fields = ['author','date_range_of_reported_data']
    template_name = "makeReports/ReportEntryExtras/first_page.html"
    labels = {
        'author':'Person preparing the report'
    }
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['pk'])
        return super(ReportFirstPage,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(ReportFirstPage,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class FinalReportSupplements(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ReportSupplement
    template_name = "makeReports/ReportEntryExtras/supplementList.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(FinalReportSupplements,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(FinalReportSupplements,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        context['report'] = self.report
        return context
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
    template_name = "makeReports/ReportEntryExtras/addSupplement.html"
    fields = ['supplement']
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AddEndSupplements,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(AddEndSupplements,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        context['report'] = self.report
        return context
    def form_valid(self,form):
        form.instance.report = self.report
        return super(AddEndSupplements,self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('makeReports:rpt-sup-list', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeleteEndSupplements(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReportSupplement
    template_name = "makeReports/ReportEntryExtras/deleteSupplement.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeleteEndSupplements,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(DeleteEndSupplements,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        context['report'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:rpt-sup-list', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class SubmitReport(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = SubmitReportForm
    template_name = "makeReports/ReportEntryExtras/submit.html"
    success_url = reverse_lazy('makeReports:sub-suc')
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(SubmitReport,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs=super(SubmitReport,self).get_form_kwargs()
        slos = SLOInReport.objects.filter(report=self.report)
        valid = True
        eMsg = "The report is not complete.\n"
        if slos.count() == 0 :
            valid = False
            eMsg = eMsg+"There are no SLOs.\n"
        for slo in slos:
            if AssessmentVersion.objects.filter(slo=slo).count()==0:
                valid = False
                eMsg = eMsg+"There is no an assessment for SLO "+str(slo.number)+".\n"
            if DecisionsActions.objects.filter(report=self.report, SLO=slo.slo).count()==0:
                valid = False
                eMsg = eMsg+"There are no decisions or actions for SLO "+str(slo.number)+".\n"
        assesses = AssessmentVersion.objects.filter(report=self.report)
        for a in assesses:
            if AssessmentData.objects.filter(assessmentVersion=a).count()==0:
                valid = False
                eMsg = eMsg+"There is no data for assessment "+str(a.number)+".\n"
        if not self.report.author or self.report.author=="":
            valid = False
            eMsg = eMsg+"There is no report author.\n"
        if not self.report.date_range_of_reported_data or self.report.date_range_of_reported_data=="":
            valid = False
            eMsg = eMsg+"There is no reported data range.\n"
        if SLOsToStakeholder.objects.filter(report=self.report).count() == 0:
            valid == False
            eMsg = eMsg+"There is no description of sharing SLOs with stakeholders.\n"
        if ResultCommunicate.objects.filter(report=self.report).count() == 0:
            valid = False
            eMsg = eMsg+"There is no description of communicating results.\n"
        kwargs['valid'] = valid
        kwargs['eMsg'] = eMsg
        return kwargs
    def get_context_data(self, **kwargs):
        context = super(SubmitReport,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['rpt'] = self.report
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
    def form_valid(self,form):
        self.report.submitted = True
        self.report.save()
        return super(SubmitReport,self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class SuccessSubmit(TemplateView):
    template_name = "makeReports/ReportEntryExtras/success.html"