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

class AssessmentSummary(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = AssessmentVersion
    template_name = "makeReports/assessmentSummary.html"
    context_object_name = "assessment_list"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AssessmentSummary,self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        report = self.report
        objs = AssessmentVersion.objects.filter(report=report)
        return objs
    def get_context_data(self, **kwargs):
        context = super(AssessmentSummary, self).get_context_data()
        context['rpt'] = self.report
        return context
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class AddNewAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/addAssessment.html"
    form_class = CreateNewAssessment
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AddNewAssessment,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs = super(AddNewAssessment,self).get_form_kwargs()
        return kwargs
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self, form):
        rpt = self.report
        assessObj = Assessment.objects.create(title=form.cleaned_data['title'], domainExamination=form.cleaned_data['domainExamination'], domainProduct=form.cleaned_data['domainProduct'], domainPerformance=form.cleaned_data['domainPerformance'])
        assessRpt = AssessmentVersion.objects.create(date=datetime.now(), assessment=assessObj, description=form.cleaned_data['description'], finalTerm=form.cleaned_data['finalTerm'], where=form.cleaned_data['where'], allStudents=form.cleaned_data['allStudents'], sampleDescription=form.cleaned_data['sampleDescription'], frequency=form.cleaned_data['frequency'], threshold=form.cleaned_data['threshold'], target=form.cleaned_data['target'] ,firstInstance= True)
        assessRpt.report.add(rpt)
        assessRpt.save()
        return super(AddNewAssessment, self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class ImportAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/importAssessment.html"
    form_class = ImportAssessment
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(ImportAssessment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportAssessment,self).get_form_kwargs()
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         kwargs['assessChoices'] = AssessmentVersion.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.request.GET['report'])
        for assessVers in form.cleaned_data['assessment']:
            AssessmentVersion.objects.create(date=datetime.now(), description=assessVers.description ,assessment=assessVers.assessment, firstInstance=False, report=rpt, changedFromPrior=False, finalTerm=assessVers.finalTerm, where=assessVers.where, allStudents=assessVers.allStudents, sampleDescription=assessVers.sampleDescription, frequency=assessVers.frequency, threshold=assessVers.threshold, target=assessVers.target)
        return super(ImportAssessment,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportAssessment, self).get_context_data(**kwargs)
        r = self.report
        context['currentDPpk'] = Report.objects.get(pk=self.kwargs['report']).degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=r.degreeProgram.department)
        context['rpt']=self.kwargs['report']
        return context
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class EditImportedAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/editImportedAssessment.html"
    form_class = EditImportedAssessment
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(EditImportedAssessment,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(EditImportedAssessment, self).get_initial()
        initial['description'] = self.assessVers.description
        initial['finalTerm'] = self.assessVers.finalTerm
        initial['where'] = self.assessVers.where
        initial['allStudents'] = self.assessVers.allStudents
        initial['sampleDescription'] = self.assessVers.sampleDescription
        initial['frequency'] = self.assessVers.frequency
        initial['threshold'] = self.assessVers.threshold
        initial['target'] = self.assessVers.target
        initial['slo'] = self.assessVers.slo
        return initial
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:assessment-summary', args=[r.pk])
    def form_valid(self,form):
        #assessVers = AssessmentVersion.objects.get(pk=self.request.GET['assessIR'])
        #newAssessVers = AssessmentVersion.objects.create(date=datetime.now(), description=form.cleaned_data['description'], assessment=assessVers.assessment, changedFromPrior=False, firstInstance=False, finalTerm=form.cleaned_data['finalTerm'], where=form.cleaned_data['where'], allStudents=form.cleaned_data['allStudents'], sampleDescription=form.cleaned_data['sampleDescription'], frequency=form.cleaned_data['frequency'], threshold=form.cleaned_data['threshold'], target=form.cleaned_data['target'])
        r = self.report
        self.sloInRpt.date=datetime.now()
        self.sloInRpt.goalText=form.cleaned_data['text']
        self.sloInRpt.changedFromPrior = True
        self.sloInRpt.save()
        return super(EditImportedAssessment, self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class EditNewAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/editNewAssessment.html"
    form_class = EditNewAssessment
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(EditNewAssessment,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(EditNewAssessment, self).get_initial()
        initial['title'] = self.assessVers.assessment.title
        initial['domainExamination'] = self.assessVers.assessment.domainExamination
        initial['domainProduct'] = self.assessVers.assessment.domainProduct
        initial['domainPerformance'] = self.assessVers.assessment.domainPerformance
        initial['directMeasure'] = self.assessVers.assessment.directMeasure
        initial['description'] = self.assessVers.description
        initial['finalTerm'] = self.assessVers.finalTerm
        initial['where'] = self.assessVers.where
        initial['allStudents'] = self.assessVers.allStudents
        initial['sampleDescription'] = self.assessVers.sampleDescription
        initial['frequency'] = self.assessVers.frequency
        initial['threshold'] = self.assessVers.threshold
        initial['target'] = self.assessVers.target
        initial['slo'] = self.assessVers.slo
        return initial
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.assessVers.description = form.cleaned_data['description']
        self.assessVers.date = datetime.now()
        self.assessVers.assessment.title = form.cleaned_data['title']
        self.assessVers.assessment.domainExamination = form.cleaned_data['domainExamination']
        self.assessVers.assessment.domainPerformance = form.cleaned_data['domainPerformance']
        self.assessVers.assessment.domainProduct = form.cleaned_data['domainProduct']
        self.assessVers.assessment.directMeasure = form.cleaned_data['directMeasure']
        self.assessVers.finalTerm = form.cleaned_data['finalTerm']
        self.assessVers.where = form.cleaned_data['where']
        self.assessVers.allStudents = form.cleaned_data['allStudents']
        self.assessVers.sampleDescription = form.cleaned_data['sampleDescription']
        self.assessVers.frequency = form.cleaned_data['frequency']
        self.assessVers.threshold = form.cleaned_data['threshold']
        self.assessVers.target = form.cleaned_data['target']
        self.assessVers.save()
        self.assessVers.assessment.save()
        return super(EditNewAssessment,self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class supplementUpload(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = ""
class Section2Comment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/assessment/assessmentComment.html"
    form_class = Single2000Textbox
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(Section2Comment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        #to be changed to assessment page!
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.report.section1Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section2Comment,self).form_valid(form)
    def get_initial(self):
        initial = super(Section2Comment,self).get_initial()
        initial['text']="No comment."
        return initial
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)

