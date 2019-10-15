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

class DataCollectionSummary(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = AssessmentData
    template_name = 'makeReports/DataCollection/dataCollectionSummary.html'
    context_object_name = "data_collection_dict"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DataCollectionSummary, self).dispatch(request,*args,**kwargs)

    def get_queryset(self):
        report = self.report
        assessments = AssessmentVersion.objects.filter(report=report).order_by("slo__number","number")
        assessment_qs = AssessmentData.objects.none()
        for assessment in assessments:
            assessment_data = AssessmentData.objects.filter(assessmentVersion = assessment)
            assessment_qs.union(assessment_data)
        return assessment_qs

    def get_context_data(self, **kwargs):
        report = self.report
        context = super(DataCollectionSummary, self).get_context_data()
        context['rpt'] = report
        return section3Context(self,context)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)


class CreateDataCollectionRow(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DataCollection/addDataCollection.html"
    form_class = AddDataCollection

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessment = AssessmentVersion.objects.get(pk=self.kwargs['assessment'])
        return super(CreateDataCollectionRow,self).dispatch(request,*args,**kwargs)

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        assessmentDataObj = AssessmentData.objects.create(assessmentVersion=self.assessment, dataRange=form.cleaned_data['dataRange'], numberStudents=form.cleaned_data['numberStudents'], overallProficient=form.cleaned_data['overallProficient'])
        assessmentDataObj.save()
        return super(CreateDataCollectionRow, self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
    def get_context_data(self,**kwargs):
        context = super(CreateDataCollectionRow,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
class CreateDataCollectionRowAssess(CreateDataCollectionRow):
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])

class EditDataCollectionRow(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DataCollection/editDataCollection.html"
    form_class = EditDataCollection

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.dataCollection = AssessmentData.objects.get(pk=self.kwargs['dataCollection'])
        return super(EditDataCollectionRow,self).dispatch(request,*args,**kwargs)

    def get_initial(self):
        initial = super(EditDataCollectionRow, self).get_initial()
        initial['dataRange'] = self.dataCollection.dataRange
        initial['numberStudents'] = self.dataCollection.numberStudents
        initial['overallProficient'] = self.dataCollection.overallProficient
        return initial

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.dataCollection.dataRange = form.cleaned_data['dataRange']
        self.dataCollection.numberStudents = form.cleaned_data['numberStudents']
        self.dataCollection.overallProficient = form.cleaned_data['overallProficient']
        self.dataCollection.save()
        return super(EditDataCollectionRow, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
    def get_context_data(self,**kwargs):
        context = super(EditDataCollectionRow,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context

class DeleteDataCollectionRow(DeleteView):
    model = AssessmentData
    template_name = "makeReports/DataCollection/deleteDataCollection.html"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=kwargs['report'])
        return super(DeleteDataCollectionRow,self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
    def get_context_data(self,**kwargs):
        context = super(DeleteDataCollectionRow,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context


class CreateSubassessmentRow(LoginRequiredMixin,UserPassesTestMixin,FormView):
    form_class = AddSubassessment
    template_name = "makeReports/DataCollection/createSubassessment.html"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessment = AssessmentVersion.objects.get(pk=self.kwargs['assessment'])
        return super(CreateSubassessmentRow,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(CreateSubassessmentRow,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        subassessmentDataObj = Subassessment.objects.create(assessmentVersion=self.assessment, title=form.cleaned_data['title'], proficient=form.cleaned_data['proficient'])
        subassessmentDataObj.save()
        return super(CreateSubassessmentRow, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)

class EditSubassessmentRow(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DataCollection/editSubassessment.html"
    form_class = EditSubassessment

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.subassessment = Subassessment.objects.get(pk=self.kwargs['pk'])
        return super(EditSubassessmentRow,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(EditSubassessmentRow,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_initial(self):
        initial = super(EditSubassessmentRow, self).get_initial()
        initial['title'] = self.subassessment.title
        initial['proficient'] = self.subassessment.proficient
        return initial

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.subassessment.title = form.cleaned_data['title']
        self.subassessment.proficient = form.cleaned_data['proficient']
        self.subassessment.save()
        return super(EditSubassessmentRow, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)


class DeleteSubassessmentRow(DeleteView):
    model = Subassessment
    template_name = "makeReports/DataCollection/deleteSubassessment.html"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=kwargs['report'])
        return super(DeleteSubassessmentRow,self).dispatch(request, *args, **kwargs)
    def get_context_data(self,**kwargs):
        context = super(DeleteSubassessmentRow,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

class NewSLOStatus(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DataCollection/SLOStatus.html"
    form_class = SLOStatusForm
    
    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        self.slo_ir = SLOInReport.objects.get(slo=self.slo, report=self.report)
        return super(NewSLOStatus,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(NewSLOStatus,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        slo_status_obj = SLOStatus.objects.create(report = self.report, status = form.cleaned_data['status'], SLO = self.slo)
        slo_status_obj.save()
        return super(NewSLOStatus, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)


class EditSLOStatus(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/Datacollection/SLOStatus.html"
    form_class = SLOStatusForm
    
    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        self.slo_ir = SLOInReport.objects.get(slo=self.slo,report=self.report)
        self.slo_status = SLOStatus.objects.get(pk=self.kwargs['statuspk'])
        return super(EditSLOStatus,self).dispatch(request,*args,**kwargs)

    def get_initial(self):
        initial = super(EditSLOStatus, self).get_initial()
        initial['status'] = self.slo_status.status
        return initial
    def get_context_data(self,**kwargs):
        context = super(EditSLOStatus,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.slo_status.report = self.report
        self.slo_status.SLO = self.slo
        self.slo_status.status = form.cleaned_data['status']
        self.slo_status.save()
        return super(EditSLOStatus, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)


class NewResultCommunication(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DataCollection/ResultCommunication.html"
    form_class = ResultCommunicationForm
    
    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(NewResultCommunication,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(NewResultCommunication,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        result_communication = ResultCommunicate.objects.create(report = self.report, text = form.cleaned_data['text'])
        result_communication.save()
        return super(NewResultCommunication, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)


class EditResultCommunication(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DataCollection/ResultCommunication.html"
    form_class = ResultCommunicationForm
    
    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.result_communication = ResultCommunicate.objects.get(pk=self.kwargs['resultpk'])
        return super(EditResultCommunication,self).dispatch(request,*args,**kwargs)

    def get_initial(self):
        initial = super(EditResultCommunication, self).get_initial()
        initial['text'] = self.result_communication.text
        return initial
    def get_context_data(self,**kwargs):
        context = super(EditResultCommunication,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.result_communication.report = self.report
        self.result_communication.text = form.cleaned_data['text']
        self.result_communication.save()
        return super(EditResultCommunication, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class Section3Comment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DataCollection/comment.html"
    form_class = Single2000Textbox
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(Section3Comment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])
    def get_context_data(self,**kwargs):
        context = super(Section3Comment,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def form_valid(self, form):
        self.report.section3Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section3Comment,self).form_valid(form)
    def get_initial(self):
        initial = super(Section3Comment,self).get_initial()
        initial['text']="No comment."
        return initial
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DataAssessmentAddInfo(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = DataAdditionalInformation
    fields = ['comment','supplement']
    template_name = "makeReports/DataCollection/addInfo.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DataAssessmentAddInfo,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(DataAssessmentAddInfo,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def form_valid(self,form):
        form.instance.report=self.report
        return super(DataAssessmentAddInfo,self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DataAssessmentDeleteInfo(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = DataAdditionalInformation
    template_name = "makeReports/DataCollection/deleteInfo.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DataAssessmentDeleteInfo,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(DataAssessmentDeleteInfo,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DataAssessmentUpdateInfo(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = DataAdditionalInformation
    template_name = "makeReports/DataCollection/updateInfo.html"
    fields = ['comment']
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DataAssessmentUpdateInfo,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context = super(DataAssessmentUpdateInfo,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)