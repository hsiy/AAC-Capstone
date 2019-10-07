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
from django.views.generic.base import ContextMixin

class DecisionsActionsSummary(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = DecisionsActions
    template_name = 'makeReports/DecisionsActions/decisionsActionsSummary.html'
    context_object_name = "decisions_actions_list"

    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DecisionsActionsSummary, self).dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        report = self.report
        context = super(DecisionsActionsSummary, self).get_context_data()
        
        context['rpt'] = report
        SLOs_ir = SLOInReport.objects.filter(report=report)
        context_list = []

        for slo_ir in SLOs_ir:
            temp_dict = dict()
            slo_obj = slo_ir.slo
            temp_dict['slo_pk'] = slo_obj.pk
            temp_dict['slo_text'] = slo_ir.goalText
            try:
                decisions_obj = DecisionsActions.objects.get(SLO=slo_obj, report=report)
                temp_dict['decisions_obj'] = decisions_obj
            except:
                temp_dict['decisions_obj'] = None

            context_list.append(temp_dict)
                
        context['decisions_actions_list'] = context_list
        return context

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)

class AddDecisionAction(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DecisionsActions/changeDecisionAction.html"
    form_class = DecisionsActionsForm
    
    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        return super(AddDecisionAction,self).dispatch(request,*args,**kwargs)

    def get_success_url(self):
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])

    def form_valid(self, form):
        result_communication = DecisionsActions.objects.create(
            report = self.report, 
            SLO = self.slo,
            decisionProcess = form.cleaned_data['decisionProcess'], 
            decisionMakers = form.cleaned_data['decisionMakers'], 
            decisionTimeline = form.cleaned_data['decisionTimeline'], 
            dataUsed = form.cleaned_data['dataUsed'], 
            actionTimeline = form.cleaned_data['actionTimeline'])
        result_communication.save()
        return super(AddDecisionAction, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)

class EditDecisionAction(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/DecisionsActions/changeDecisionAction.html"
    form_class = DecisionsActionsForm
    
    def dispatch(self, request, *args, **kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        self.decision_action = DecisionsActions.objects.get(pk=self.kwargs['decactpk'])
        return super(EditDecisionAction,self).dispatch(request,*args,**kwargs)

    def get_initial(self):
        initial = super(EditDecisionAction, self).get_initial()
        initial['decisionProcess'] = self.decision_action.decisionProcess
        initial['decisionMakers'] = self.decision_action.decisionMakers
        initial['decisionTimeline'] = self.decision_action.decisionTimeline
        initial['dataUsed'] = self.decision_action.dataUsed
        initial['actionTimeline'] = self.decision_action.actionTimeline
        return initial

    def get_success_url(self):
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.decision_action.report = self.report
        self.decision_action.SLO = self.slo
        self.decision_action.decisionProcess = form.cleaned_data['decisionProcess']
        self.decision_action.decisionMakers = form.cleaned_data['decisionMakers'] 
        self.decision_action.decisionTimeline = form.cleaned_data['decisionTimeline']
        self.decision_action.dataUsed = form.cleaned_data['dataUsed']
        self.decision_action.actionTimeline = form.cleaned_data['actionTimeline']
        self.decision_action.save()
        return super(EditDecisionAction, self).form_valid(form)

    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)