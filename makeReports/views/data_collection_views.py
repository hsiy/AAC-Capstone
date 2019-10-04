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

            assessment_obj = Assessment.objects.get(pk=assessment.assessment)
            temp_dict['assessment_text'] = assessment_obj.title

            slo_obj = SLOInReport.objects.get(pk=assessment.slo)
            temp_dict['slo_text'] = slo_obj.goalText

            assessment_data_obj = AssessmentData.objects.get(assessmentVersion=assessment)
            temp_dict['num_students_assessed'] = assessment_data_obj.numberStudents
            temp_dict['overall_proficient'] = assessment_data_obj.overallProficient

            subassessments = Subassessment.objects.filter(assessmentVersion=assessment)
            temp_dict['subassessments'] = []

            for subassessment in subassessments:
                sub_dict = {subassessment.title : subassessment.proficient}
                temp_dict['subassessments'].append(sub_dict)

            assessment_data_dict['assessments'].append(temp_dict)
            
        context['assessment_data_dict'] = assessment_data_dict
        return context

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)


class CreateDataCollectionRow(LoginRequiredMixin,UserPassesTestMixin,FormView):
    pass


class EditDataCollectionRow(LoginRequiredMixin,UserPassesTestMixin,FormView):
    pass


class DeleteDataCollectionRow(DeleteView):
    pass


class CreateSubassessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    pass


class EditSubassessment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    pass


class DeleteSubassessment(DeleteView):
    pass
