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
from django.template.defaulttags import register
def rubricItemsHelper(self,context):
    extraHelp = dict()
    for rI in self.rubricItems:
        extraHelp["rI"+str(rI.pk)] = [rI.DMEtext, rI.MEtext, rI.EEtext]
    context['extraHelp']=extraHelp
    return context
def section1Context(self,context):
    context['slo_list'] = SLOInReport.objects.filter(report=self.report)
    context['stk'] = SLOsToStakeholder.objects.filter(report=self.report).last()
    return context
def section2Context(self,context):
    context['assessment_list'] = AssessmentVersion.objects.filter(report=self.report)
    return context
def section3Context(self,context):
    assessment_data_dict = {'assessments':[], 'slo_statuses':[]}
    assessments = AssessmentVersion.objects.filter(report=self.report).order_by("slo__number","number")
    for assessment in assessments:
        temp_dict = dict()
        temp_dict['assessment_id'] = assessment.pk
        try:
            assessment_obj = Assessment.objects.get(pk=assessment.assessment.pk)
            temp_dict['assessment_text'] = assessment_obj.title
            temp_dict['assessment_obj'] = assessment
        except:
            temp_dict['assessment_text'] = None
            temp_dict['assessment_obj'] = None

        try:
            slo_obj = SLOInReport.objects.get(pk=assessment.slo.pk)
            temp_dict['slo_text'] = slo_obj.goalText
            temp_dict['slo_obj'] = slo_obj
        except:
            temp_dict['slo_text'] = None
            temp_dict['slo_obj'] = None

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

    SLOs = SLOInReport.objects.filter(report=self.report)
    for sloir in SLOs:
        temp_dict = dict()
        temp_dict['slo_text'] = sloir.goalText
        temp_dict['slo_pk'] = sloir.slo.pk
        try:
            slo_status_obj = SLOStatus.objects.get(SLO=sloir.slo)
            temp_dict['slo_status'] = slo_status_obj.status
            temp_dict['slo_status_pk'] = slo_status_obj.pk
        except:
            temp_dict['slo_status'] = None
            temp_dict['slo_status_pk'] = None

        assessment_data_dict['slo_statuses'].append(temp_dict)
        
    try:
        result_communicate_obj = ResultCommunicate.objects.get(report=self.report)
        assessment_data_dict['result_communication_id'] = result_communicate_obj.pk
        assessment_data_dict['result_communication_text'] = result_communicate_obj.text
    except:
        pass
    context['assessment_data_dict'] = assessment_data_dict
    context['supplement_list'] = DataAdditionalInformation.objects.filter(report=self.report)
    return context
def section4Context(self,context):
    SLOs_ir = SLOInReport.objects.filter(report=self.report)
    context_list = []
    for slo_ir in SLOs_ir:
        temp_dict = dict()
        slo_obj = slo_ir.slo
        temp_dict['slo_obj'] = slo_ir
        temp_dict['slo_pk'] = slo_obj.pk
        temp_dict['slo_text'] = slo_ir.goalText
        try:
            decisions_obj = DecisionsActions.objects.get(SLO=slo_obj, report=self.report)
            temp_dict['decisions_obj'] = decisions_obj
        except:
            temp_dict['decisions_obj'] = None

        context_list.append(temp_dict)
            
    context['decisions_actions_list'] = context_list
    return context