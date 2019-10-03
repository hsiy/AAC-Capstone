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
    template_name = None
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
        context = super(DataCollectionSummary, self).get_context_data()
        context['rpt'] = self.report

        # TODO: generate dictionary such that subassessments are associated with assessmentdata
        

        return context

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