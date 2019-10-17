from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import RedirectView
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
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *
from django import forms
from django_summernote.widgets import SummernoteWidget


class DecisionsActionsSummary(DeptReportMixin,ListView):
    model = DecisionsActions
    template_name = 'makeReports/DecisionsActions/decisionsActionsSummary.html'
    context_object_name = "decisions_actions_list"

    def get_context_data(self, **kwargs):
        context = super(DecisionsActionsSummary, self).get_context_data()
        return section4Context(self,context)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)

class AddDecisionAction(DeptReportMixin,CreateView):
    model = DecisionsActions
    template_name = "makeReports/DecisionsActions/changeDecisionAction.html"
    fields = ['text']
    def dispatch(self, request, *args, **kwargs):
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        return super(AddDecisionAction,self).dispatch(request,*args,**kwargs)
    def get_form(self):
        form = super(AddDecisionAction,self).get_form()
        form.fields['text'].widget=SummernoteWidget()
        form.fields['text'].label=""
        return form
    def form_valid(self,form):
        form.instance.SLO = self.slo
        form.instance.report = self.report
        return super(AddDecisionAction,self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])
class AddDecisionActionSLO(AddDecisionAction):
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class EditDecisionAction(DeptReportMixin,UpdateView):
    model = DecisionsActions
    template_name = "makeReports/DecisionsActions/changeDecisionAction.html"
    fields = ['text']
    def dispatch(self, request, *args, **kwargs):
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        return super(EditDecisionAction,self).dispatch(request,*args,**kwargs)
    def get_form(self):
        form = super(EditDecisionAction,self).get_form()
        form.fields['text'].widget=SummernoteWidget()
        form.fields['text'].label=""
        return form
    def get_success_url(self):
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])
class EditDecisionActionSLO(EditDecisionAction):
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class AddEditRedirect(DeptReportMixin,RedirectView):
    def get_redirect_url(self, *args,**kwargs):
        slo = SLO.objects.get(pk=self.kwargs['slopk'])
        rpt = self.report
        try:
            dA = DecisionsActions.objects.get(SLO=slo,report=rpt)
            return reverse_lazy('makeReports:edit-decisions-actions-slo', args=[rpt.pk,slo.pk,dA.pk])
        except:
            return reverse_lazy('makeReports:add-decisions-actions-slo', args=[rpt.pk,slo.pk])
class Section4Comment(DeptReportMixin,FormView):
    template_name = "makeReports/DecisionsActions/comment.html"
    form_class = Single2000Textbox
    def get_success_url(self):
        return reverse_lazy('makeReports:rpt-sup-list', args=[self.report.pk])
    def form_valid(self, form):
        self.report.section4Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section4Comment,self).form_valid(form)
    def get_initial(self):
        initial = super(Section4Comment,self).get_initial()
        initial['text']="No comment."
        return initial
