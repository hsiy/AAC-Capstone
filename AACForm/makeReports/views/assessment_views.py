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

class AssessmentSummary(ListView):
    model = AssessmentVersion
    template_name = "makeReports/assessmentSummary.html"
    context_object_name = "assessment_list"
    def get_queryset(self):
        report = Report.objects.get(pk=self.request.GET['report'])
        objs = AssessmentVersion.objects.filter(report=report)
        return objs
class AddNewAssessment(FormView):
    template_name = "makeReports/addAssessment.html"
    form_class = CreateNewAssessment
    success_url = ""
    def form_valid(self, form):
        rpt = Report.objects.get(pk=self.request.GET['report'])
        assessObj = Assessment.objects.create(title=form.cleaned_data['title'], domainExamination=form.cleaned_data['domainExamination'], domainProduct=form.cleaned_data['domainProduct'], domainPerformance=form.cleaned_data['domainPerformance'])
        assessRpt = AssessmentVersion.objects.create(date=datetime.now(), assessment=assessObj, description=form.cleaned_data['description'], finalTerm=form.cleaned_data['finalTerm'], where=form.cleaned_data['where'], allStudents=form.cleaned_data['allStudents'], sampleDescription=form.cleaned_data['sampleDescription'], frequency=form.cleaned_data['frequency'], threshold=form.cleaned_data['threshold'], target=form.cleaned_data['target'] ,firstInstance= True)
        assessRpt.report.add(rpt)
        assessRpt.save()
        return super(AddNewAssessment, self).form_valid(form)
class ImportAssessment(FormView):
    template_name = "makeReports/importAssessment.html"
    form_class = ImportSLOForm
    success_url = ""
    def get_form_kwargs(self, index):
         kwargs = super().get_form_kwargs(index)
         yearIn = self.request.GET['year']
         dP = self.request.GET['dp']
         rpt = Report.objects.get(year=yearIn, degreeProgram=DegreeProgram.objects.get(pk=dP))
         kwargs['assessmentChoices'] = AssessmentVersion.objects.get(report=rpt)
         return kwargs
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.request.GET['report'])
        for assessVers in form.cleaned_data['slo']:
            AssessmentVersion.objects.create(date=datetime.now(), description=assessVers.description ,assessment=assessVers.assessment, firstInstance=False, report=rpt, changedFromPrior=False, finalTerm=assessVers.finalTerm, where=assessVers.where, allStudents=assessVers.allStudents, sampleDescription=assessVers.sampleDescription, frequency=assessVers.frequency, threshold=assessVers.threshold, target=assessVers.target)
        return super(ImportAssessment,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportAssessment, self).get_context_data(**kwargs)
        context['currentDPpk'] = Report.objects.get(pk=self.request.GET['report']).degreeProgram.pk
        return context
class EditImportedAssessment(FormView):
    template_name = "makeReports/editImportedAssessment.html"
    form_class = EditImportedAssessment
    success_url = ""
    def form_valid(self,form):
        assessVers = AssessmentVersion.objects.get(pk=self.request.GET['assessIR'])
        newAssessVers = AssessmentVersion.objects.create(date=datetime.now(), description=form.cleaned_data['description'], assessment=assessVers.assessment, changedFromPrior=False, firstInstance=False, finalTerm=form.cleaned_data['finalTerm'], where=form.cleaned_data['where'], allStudents=form.cleaned_data['allStudents'], sampleDescription=form.cleaned_data['sampleDescription'], frequency=form.cleaned_data['frequency'], threshold=form.cleaned_data['threshold'], target=form.cleaned_data['target'])
        return super(EditImportedAssessment, self).form_valid(form)
class EditNewAssessment(FormView):
    template_name = "makeReports/editNewAssessment.html"
    form_class = EditNewAssessment
    success_url = ""
    def form_valid(self, form):
        assessIR = AssessmentVersion.objects.get(pk=self.request.GET['assessIR'])
        assessIR.description = form.cleaned_data['description']
        assessIR.date = datetime.now()
        assessIR.assessment.title = form.cleaned_data['title']
        assessIR.assessment.domainExamination = form.cleaned_data['domainExamination']
        assessIR.assessment.domainPerformance = form.cleaned_data['domainPerformance']
        assessIR.assessment.domainProduct = form.cleaned_data['domainProduct']
        assessIR.assessment.directMeasure = form.cleaned_data['directMeasure']
        assessIR.finalTerm = form.cleaned_data['finalTerm']
        assessIR.where = form.cleaned_data['where']
        assessIR.allStudents = form.cleaned_data['allStudents']
        assessIR.sampleDescription = form.cleaned_data['sampleDescription']
        assessIR.frequency = form.cleaned_data['frequency']
        assessIR.threshold = form.cleaned_data['threshold']
        assessIR.target = form.cleaned_data['target']
#class supplementUpload(FormView):
    
class Section2Comment(FormView):
    template_name = ""
    form_class = Single2000Textbox
    success_url = ""
    def form_valid(self, form):
        rpt = Report.objects.get(pk=self.request.GET['report'])
        rpt.section2Comment = form.cleaned_data['text']
        rpt.save()
        return super(Section2Comment,self).form_valid(form)

