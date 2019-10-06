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

class DataCollectionSummary(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = AssessmentData
    template_name = 'makeReports/DataCollection/dataCollectionSummary.html'
    context_object_name = "data_collection_dict"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DataCollectionSummary, self).dispatch(request,*args,**kwargs)

    def get_queryset(self):
        report = self.report
        assessments = AssessmentVersion.objects.filter(report=report)
        assessment_qs = AssessmentData.objects.none()
        for assessment in assessments:
            assessment_data = AssessmentData.objects.filter(assessmentVersion = assessment)
            assessment_qs.union(assessment_data)
        return assessment_qs

    def get_context_data(self, **kwargs):
        report = self.report
        context = super(DataCollectionSummary, self).get_context_data()
        context['rpt'] = report
        assessment_data_dict = {'assessments':[]}
        assessments = AssessmentVersion.objects.filter(report=report)

        for assessment in assessments:
            temp_dict = dict()
            temp_dict['assessment_id'] = assessment.pk
            try:
                assessment_obj = Assessment.objects.get(pk=assessment.assessment.pk)
                temp_dict['assessment_text'] = assessment_obj.title
            except:
                temp_dict['assessment_text'] = None

            try:
                slo_obj = SLOInReport.objects.get(pk=assessment.slo.pk)
                temp_dict['slo_text'] = slo_obj.goalText
            except:
                temp_dict['slo_text'] = None

            try:
                assessment_data_obj = AssessmentData.objects.get(assessmentVersion=assessment)
                temp_dict['num_students_assessed'] = assessment_data_obj.numberStudents
                temp_dict['overall_proficient'] = assessment_data_obj.overallProficient
                temp_dict['data_range'] = assessment_data_obj.dataRange
                temp_dict['assessment_data_id'] = assessment_data_obj.pk
            except:
                temp_dict['num_students_assessed'] = None
                temp_dict['overall_proficient'] = None
                temp_dict['data_range'] = None
                temp_dict['assessment_data_id'] = None

            try:
                subassessments = Subassessment.objects.filter(assessmentVersion=assessment)
                temp_dict['subassessments'] = []
                for subassessment in subassessments:
                    sub_dict = (subassessment.title, subassessment.proficient, subassessment.pk)
                    temp_dict['subassessments'].append(sub_dict)

                temp_dict['subassessments_len'] = len(temp_dict['subassessments'])
            except:
                temp_dict['subassessments'] = []
                temp_dict['subassessments_len'] = 0

            assessment_data_dict['assessments'].append(temp_dict)
            
        context['assessment_data_dict'] = assessment_data_dict
        return context

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


class DeleteDataCollectionRow(DeleteView):
    model = AssessmentData
    template_name = "makeReports/DataCollection/deleteDataCollection.html"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=kwargs['report'])
        return super(DeleteDataCollectionRow,self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])


class CreateSubassessmentRow(LoginRequiredMixin,UserPassesTestMixin,FormView):
    form_class = AddSubassessment
    template_name = "makeReports/DataCollection/createSubassessment.html"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.assessment = AssessmentVersion.objects.get(pk=self.kwargs['assessment'])
        return super(CreateSubassessmentRow,self).dispatch(request,*args,**kwargs)

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

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])