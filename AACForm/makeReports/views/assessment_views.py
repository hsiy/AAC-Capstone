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

class AssessmentSummary(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = AssessmentVersion
    template_name = "makeReports/Assessment/assessmentSummary.html"
    context_object_name = "assessment_list"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AssessmentSummary,self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        report = self.report
        objs = AssessmentVersion.objects.filter(report=report).order_by("slo__number","number")
        return objs
    def get_context_data(self, **kwargs):
        context = super(AssessmentSummary, self).get_context_data()
        context['rpt'] = self.report
        return section2Context(self,context)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class AddNewAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/addAssessment.html"
    form_class = CreateNewAssessment
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AddNewAssessment,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(AddNewAssessment,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_form_kwargs(self):
        kwargs = super(AddNewAssessment,self).get_form_kwargs()
        kwargs['sloQS'] = SLOInReport.objects.filter(report=self.report)
        return kwargs
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self, form):
        rpt = self.report
        form.cleaned_data['slo'].numberOfAssess += 1
        form.cleaned_data['slo'].save()
        assessObj = Assessment.objects.create(title=form.cleaned_data['title'], domainExamination=False, domainProduct=False, domainPerformance=False, directMeasure =form.cleaned_data['directMeasure'])
        assessRpt = AssessmentVersion.objects.create(date=datetime.now(), number=form.cleaned_data['slo'].numberOfAssess, assessment=assessObj, description=form.cleaned_data['description'], finalTerm=form.cleaned_data['finalTerm'], where=form.cleaned_data['where'], allStudents=form.cleaned_data['allStudents'], sampleDescription=form.cleaned_data['sampleDescription'], frequency=form.cleaned_data['frequency'], threshold=form.cleaned_data['threshold'], target=form.cleaned_data['target'] ,slo=form.cleaned_data['slo'] ,firstInstance= True, report=rpt, changedFromPrior=False)
        dom = form.cleaned_data['domain']
        if ("Pe" in dom):
            assessObj.domainPerformance = True
        if ("Pr" in dom):
            assessObj.domainProduct = True
        if ("Ex" in dom):
            assessObj.domainExamination = True
        assessObj.save()
        assessRpt.save()
        return super(AddNewAssessment, self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class ImportAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/importAssessment.html"
    form_class = ImportAssessmentForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(ImportAssessment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def get_form_kwargs(self):
        kwargs = super(ImportAssessment,self).get_form_kwargs()
        yearIn = self.request.GET['year']
        dP = self.request.GET['dp']
        aCs = AssessmentVersion.objects
        if yearIn!="":
            aCs=aCs.filter(report__year=yearIn)
        if dP!="" and dP!="-1":
            try:
                aCs=aCs.filter(report__degreeProgram=DegreeProgram.objects.get(pk=dP))
            except:
                pass
        if self.request.GET['slo']!="" and self.request.GET['slo']!="-1":
            aCs=aCs.filter(slo=SLOInReport.objects.get(pk=self.request.GET['slo']))
        aCsInRpt = AssessmentVersion.objects.filter(report=self.report)
        for a in aCsInRpt:
            aCs=aCs.exclude(assessment=a.assessment)
        kwargs['assessChoices'] = aCs
        kwargs['slos'] = SLOInReport.objects.filter(report=self.report)
        return kwargs
    def form_valid(self,form):
        rpt = self.report
        slo = form.cleaned_data['slo']
        num = slo.numberOfAssess
        for assessVers in form.cleaned_data['assessment']:
            num += 1
            AssessmentVersion.objects.create(slo=slo,number=num,date=datetime.now(), description=assessVers.description ,assessment=assessVers.assessment, firstInstance=False, report=rpt, changedFromPrior=False, finalTerm=assessVers.finalTerm, where=assessVers.where, allStudents=assessVers.allStudents, sampleDescription=assessVers.sampleDescription, frequency=assessVers.frequency, threshold=assessVers.threshold, target=assessVers.target)
        slo.numberOfAssess = num
        slo.save()
        return super(ImportAssessment,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportAssessment, self).get_context_data(**kwargs)
        r = self.report
        context['currentDPpk'] = r.degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=r.degreeProgram.department)
        context['slo_list'] = SLOInReport.objects.filter(report=r).union(SLOInReport.objects.filter(report__degreeProgram__department=r.degreeProgram.department).exclude(report=r),all=True)
        context['rpt']= r
        return context
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class EditImportedAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/editImportedAssessment.html"
    form_class = EditImportedAssessmentForm
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
    def get_form_kwargs(self):
        kwargs = super(EditImportedAssessment,self).get_form_kwargs()
        kwargs['sloQS'] = SLOInReport.objects.filter(report=self.report)
        return kwargs
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:assessment-summary', args=[r.pk])
    def form_valid(self,form):
        #assessVers = AssessmentVersion.objects.get(pk=self.request.GET['assessIR'])
        #newAssessVers = AssessmentVersion.objects.create(date=datetime.now(), description=form.cleaned_data['description'], assessment=assessVers.assessment, changedFromPrior=False, firstInstance=False, finalTerm=form.cleaned_data['finalTerm'], where=form.cleaned_data['where'], allStudents=form.cleaned_data['allStudents'], sampleDescription=form.cleaned_data['sampleDescription'], frequency=form.cleaned_data['frequency'], threshold=form.cleaned_data['threshold'], target=form.cleaned_data['target'])
        r = self.report
        self.assessVers.description = form.cleaned_data['description']
        self.assessVers.date = datetime.now()
        self.assessVers.finalTerm = form.cleaned_data['finalTerm']
        self.assessVers.where = form.cleaned_data['where']
        self.assessVers.allStudents = form.cleaned_data['allStudents']
        self.assessVers.sampleDescription = form.cleaned_data['sampleDescription']
        self.assessVers.frequency = form.cleaned_data['frequency']
        self.assessVers.threshold = form.cleaned_data['threshold']
        self.assessVers.target = form.cleaned_data['target']
        self.assessVers.slo = form.cleaned_data['slo']
        self.assessVers.save()
        self.assessVers.assessment.save()
        return super(EditImportedAssessment, self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class EditNewAssessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/editNewAssessment.html"
    form_class = EditNewAssessmentForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(EditNewAssessment,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(EditNewAssessment, self).get_initial()
        initial['title'] = self.assessVers.assessment.title
        initial['domainPerformance'] = self.assessVers.assessment.domainPerformance
        initial['domainProduct'] = self.assessVers.assessment.domainProduct
        initial['domainExamination'] = self.assessVers.assessment.domainExamination
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
    def get_form_kwargs(self):
        kwargs = super(EditNewAssessment,self).get_form_kwargs()
        kwargs['sloQS'] = SLOInReport.objects.filter(report=self.report)
        return kwargs
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.assessVers.description = form.cleaned_data['description']
        self.assessVers.date = datetime.now()
        self.assessVers.assessment.title = form.cleaned_data['title']
        self.assessVers.assessment.domain = form.cleaned_data['domain']
        self.assessVers.assessment.directMeasure = form.cleaned_data['directMeasure']
        self.assessVers.finalTerm = form.cleaned_data['finalTerm']
        self.assessVers.where = form.cleaned_data['where']
        self.assessVers.allStudents = form.cleaned_data['allStudents']
        self.assessVers.sampleDescription = form.cleaned_data['sampleDescription']
        self.assessVers.frequency = form.cleaned_data['frequency']
        self.assessVers.threshold = form.cleaned_data['threshold']
        self.assessVers.target = form.cleaned_data['target']
        self.assessVers.slo = form.cleaned_data['slo']
        self.assessVers.save()
        self.assessVers.assessment.save()
        return super(EditNewAssessment,self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class SupplementUpload(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    template_name = "makeReports/Assessment/supplementUpload.html"
    model = AssessmentSupplement
    fields = ['supplement']
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(SupplementUpload,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        self.assessVers.supplements.add(self.object)
        self.assessVers.save()
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self,form):
        form.instance.assessmentVersion = self.assessVers
        form.instance.uploaded_at = datetime.now()
        return super(SupplementUpload,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(SupplementUpload, self).get_context_data(**kwargs)
        context['rpt']=self.report
        return context
    def test_func(self):
        return (self.report.degreeProgram.department==self.request.user.profile.department)
class ImportSupplement(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/importSupplement.html"
    form_class = ImportSupplementsForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(ImportSupplement,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportSupplement,self).get_form_kwargs()
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         kwargs['supChoices'] = AssessmentSupplement.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        self.assessVers.supplements.add(form.cleaned_data['sup'])
        self.assessVers.save()
        return super(ImportSupplement,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportSupplement, self).get_context_data(**kwargs)
        context['currentDPpk'] = self.report.degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=self.report.degreeProgram.department)
        context['rpt'] = self.report
        return context
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeleteSupplement(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = AssessmentSupplement
    template_name = "makeReports/Assessment/deleteSupplement.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeleteSupplement,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(DeleteSupplement,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class Section2Comment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Assessment/assessmentComment.html"
    form_class = Single2000Textbox
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(Section2Comment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.report.section2Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section2Comment,self).form_valid(form)
    def get_context_data(self,**kwargs):
        context = super(Section2Comment,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_initial(self):
        initial = super(Section2Comment,self).get_initial()
        initial['text']="No comment."
        return initial
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeleteImportedAssessment(DeleteView):
    model = AssessmentVersion
    template_name = "makeReports/Assessment/deleteAssessment.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        a = AssessmentVersion.objects.get(pk=self.kwargs['pk'])
        self.oldNum = a.number
        self.slo = a.slo
        return super(DeleteImportedAssessment,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(DeleteImportedAssessment,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        oldNum = self.oldNum
        num = self.slo.numberOfAssess
        assess = AssessmentVersion.objects.filter(report=self.report)
        for a in assess:
            if a.number > oldNum:
                a.number -= 1
                a.save()
        self.slo.numberOfAssess -= 1
        self.slo.save()
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
class DeleteNewAssessment(DeleteView):
    model = AssessmentVersion
    template_name = "makeReports/Assessment/deleteAssessment.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        a = AssessmentVersion.objects.get(pk=self.kwargs['pk'])
        self.oldNum = a.number
        self.slo = a.slo
        return super(DeleteNewAssessment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        ASSESSIR = AssessmentVersion.objects.get(pk=self.kwargs['pk'])
        assessment = ASSESSIR.assessment
        assessment.delete()
        assessment.save()
        oldNum = self.oldNum
        num = self.slo.numberOfAssess
        assess = AssessmentVersion.objects.filter(report=self.report)
        for a in assess:
            if a.number > oldNum:
                a.number -= 1
                a.save()
        self.slo.numberOfAssess -= 1
        self.slo.save()        
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def get_context_data(self,**kwargs):
        context = super(DeleteNewAssessment,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
