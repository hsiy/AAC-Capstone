from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

class SLOSummary(ListView, FormMixin):
    model = SLOInReport
    template_name =""
    form_class = SLOsToStakeholderEntry
    success_url = ""
    def get_queryset(self):
        report = Report.objects.get(pk=self.request.GET['report'])
        objs = SLOInReport.objects.filter(report=report)
        return objs
    def form_valid(self,form):
        report = Report.objects.get(pk=self.request.GET['report'])
        SLOsToStakeholder(text=form.cleaned_data['text'], report=report)
class AddNewSLO(FormView):
    template_name = ""
    form_class = CreateNewSLO
    success_url = ""
    def form_valid(self, form):
        gGoals = forms.cleaned_data["gradGoals"]
        rpt = Report.objects.get(pk=self.request.GET['report'])
        sloObj = SLO.objects.create(blooms=form.cleaned_data['blooms'], gradGoals=form.cleaned_data['gradGoals'])
        sloTxt = SLOText.objects.create(date=datetime.now(), goalText =form.cleaned_data['text'], slo=sloObj)
        sloRpt = SLOInReport.objects.create(sloText=sloTxt, firstInstance= True)
        sloRpt.report.add(rpt)
        sloRpt.save()
        return super(AddNewSLO, self).form_valid(form)
class ImportSLO(FormView):
    template_name = ""
    form_class = ImportSLO
    success_url = ""
    def form_valid(self,form):
        

