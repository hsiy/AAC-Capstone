"""
This file contains views related to graphing
"""
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from makeReports.models import *
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *
from csv_export.views import CSVExportView

class GraphingHome(AACOnlyMixin,TemplateView):
    template_name = "makeReports/Graphing/graphing.html"
    def get_context_data(self, **kwargs):
        context = super(GraphingHome, self).get_context_data(**kwargs)
        context['colleges'] = College.active_objects.all
        return context
class GraphingDept(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "graphing_dept.html"
    def test_func(self):
        return self.request.user.profile.department.pk == int(self.kwargs['dept'])
class OutputCSVDepartment(LoginRequiredMixin, UserPassesTestMixin,CSVExportView):
    model = AssessmentData
    fields = [
        'assessmentVersion__report__year',
        'assessmentVersion__report__degreeProgram', 'assessmentVersion__report__degreeProgram__name',
        'assessmentVersion__report',
        'assessmentVersion__slo', 'assessmentVersion__slo__goalText',
        'assessmentVersion__slo__slo__blooms',
        'assessmentVersion__assessment', 'assessmentVersion__assessment__title',
        'assessmentVersion__assessment__domainExamination', 
        'assessmentVersion__assessment__domainProduct', 
        'assessmentVersion__assessment__domainPerformance',
        'assessmentVersion__assessment__directMeasure',
        'assessmentVersion', 'assessmentVersion__assessmentaggregate__aggregate_proficiency',
        'assessmentVersion__assessmentaggregate__met',
        'assessmentVersion__date', 'assessmentVersion__description',
        'assessmentVersion__finalTerm', 'assessmentVersion__where',
        'assessmentVersion__allStudents', 'assessmentVersion__sampleDescription',
        'assessmentVersion__frequencyChoice', 'assessmentVersion__frequency',
        'assessmentVersion__threshold', 'assessmentVersion__target',
        'dataRange','numberStudents','overallProficient',
        ]
    def get_field_value(self,obj, field_name):
        if "assessmentVersion__assessmentaggregate" in field_name:
            #following code is taken from the source code for CSVExportView
            try:
                related_field_names = field_name.split('__')
                related_obj = getattr(obj, related_field_names[0])
                related_field_name = '__'.join(related_field_names[1:])
                return self.get_field_value(related_obj, related_field_name)
            except:
                return ""
        else:
            return super(OutputCSVDepartment,self).get_field_value(obj, field_name)
    def get_queryset(self):
        return AssessmentData.objects.filter(
            assessmentVersion__report__year__gte=self.kwargs['gYear'],
            assessmentVersion__report__year__lte=self.kwargs['lYear'],
            assessmentVersion__report__degreeProgram__department__pk=self.kwargs['dept'])
    def test_func(self):
        return (self.request.user.profile.department.pk == int(self.kwargs['dept'])) or self.request.user.profile.aac
class OutputCSVDP(OutputCSVDepartment):
    def get_queryset(self):
        return AssessmentData.objects.filter(
            assessmentVersion__report__year__gte=self.kwargs['gYear'],
            assessmentVersion__report__year__lte=self.kwargs['lYear'],
            assessmentVersion__report__degreeProgram__pk=self.kwargs['dP'])
class OutputCSVCollege(OutputCSVDepartment):
    fields = [
        'assessmentVersion__report__year',
        'assessmentVersion__report__degreeProgram__department', 'assessmentVersion__report__degreeProgram__department__name',
        'assessmentVersion__report__degreeProgram', 'assessmentVersion__report__degreeProgram__name',
        'assessmentVersion__report',
        'assessmentVersion__slo', 'assessmentVersion__slo__goalText',
        'assessmentVersion__slo__slo__blooms', 'assessmentVersion__slo__slo__'
        'assessmentVersion__assessment', 'assessmentVersion__assessment__title',
        'assessmentVersion__assessment__domainExamination', 
        'assessmentVersion__assessment__domainProduct', 
        'assessmentVersion__assessment__domainPerformance',
        'assessmentVersion__assessment__directMeasure',
        'assessmentVersion', 'assessmentVersion__assessmentaggregate__aggregate_proficiency',
        'assessmentVersion__assessmentaggregate__met',
        'assessmentVersion__date', 'assessmentVersion__description',
        'assessmentVersion__finalTerm', 'assessmentVersion__where',
        'assessmentVersion__allStudents', 'assessmentVersion__sampleDescription',
        'assessmentVersion__frequencyChoice', 'assessmentVersion__frequency',
        'assessmentVersion__threshold', 'assessmentVersion__target',
        'dataRange','numberStudents','overallProficient',
        ]
    def get_queryset(self):
        return AssessmentData.objects.filter(
            assessmentVersion__report__year__gte=self.kwargs['gYear'],
            assessmentVersion__report__year__lte=self.kwargs['lYear'],
            assessmentVersion__report__degreeProgram__department__college__pk=self.kwargs['col']
            )
    def test_func(self):
        return self.request.user.profile.aac
class CSVManagement(LoginRequiredMixin, TemplateView):
    template_name = "makeReports/CSV/csvManagement.html"
    def get_context_data(self, **kwargs):
        context = super(CSVManagement, self).get_context_data(**kwargs)
        context['colleges'] = College.active_objects.all
        return context