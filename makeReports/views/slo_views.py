from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, DetailView, FormView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin

class SLOSummary(ListView):
    model = SLOInReport
    template_name ="makeReports/sloSummary.html"
    context_object_name = "slo_list"
    def get_queryset(self):
        report = Report.objects.get(pk=self.request.GET['report'])
        objs = SLOInReport.objects.filter(report=report)
        return objs
class AddNewSLO(FormView):
    template_name = "makeReports/addSLO.html"
    form_class = CreateNewSLO
    success_url = ""
    def form_valid(self, form):
        gGoals = form.cleaned_data["gradGoals"]
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
        slo = form.cleaned_data['slo']
        rpt = Report.objects.get(pk=self.request.GET['report'])
        SLOText = slo.sloText
        SLOInReport.objects.creat(sloText=SLOText, firstInstance=False, report=rpt)
        return super(ImportSLO,self).form_valid(form)
class EditSLO(FormView):
    template_name = "makeReports/editSLO.html"
    form_class = EditSLO
    success_url = ""
    def form_valid(self,form):
        slo = SLOInReport.objects.get(pk=self.request.GET['sloIR'])
        if slo.firstInstance:
             slo.SLOText.goalText = form.cleaned_data['text']
        else:
            newTextobj = SLOText.objects.create(date=datetime.now(), goalText=form.cleaned_data['text'], slo = slo.sloText.slo)
            slo.SLOText=newTextobj
        slo.save()
        return super(EditSLO, self).form_valid(form)
class StakeholderEntry(FormView):
    template_name = "makeReports/stakeholdersSLO.html"
    form_class = SLOsToStakeholderEntry
    success_url = ""
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.request.GET['report'])
        SLOsToStakeholder.objects.create(text=form.cleaned_data['text'], report = rpt)
        return super(StakeholderEntry,self).form_valid(form)

    