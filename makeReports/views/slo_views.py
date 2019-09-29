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
        sloRpt = SLOInReport.objects.create(date=datetime.now(), goalText =form.cleaned_data['text'], slo=sloObj, firstInstance= True)
        sloRpt.report.add(rpt)
        sloRpt.save()
        return super(AddNewSLO, self).form_valid(form)
class ImportSLO(FormView):
    template_name = "makeReports/importSLO.html"
    form_class = ImportSLO
    success_url = ""
    def get_form_kwargs(self, index):
         kwargs = super().get_form_kwargs(index)
         yearIn = self.request.GET['year']
         dP = self.request.GET['dp']
         rpt = Report.objects.get(year=yearIn, degreeProgram=DegreeProgram.objects.get(pk=dP))
         kwargs['sloChoices'] = SLOInReport.objects.get(report=rpt)
         return kwargs
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.request.GET['report'])
        for sloInRpt in form.cleaned_data['slo']:
            SLOInReport.objects.create(date=datetime.now(),goalText=sloInRpt.goalText,slo=sloInRpt.slo, firstInstance=False, report=rpt, changedFromPrior=False)
        return super(ImportSLO,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportSLO, self).get_context_data(**kwargs)
        context['currentDPpk'] = Report.objects.get(pk=self.request.GET['report']).degreeProgram.pk
        return context
class EditImportedSLO(FormView):
    template_name = "makeReports/editImportedSLO.html"
    form_class = EditImportedSLO
    success_url = ""
    def form_valid(self,form):
        sloInRpt = SLOInReport.objects.get(pk=self.request.GET['sloIR'])
        newSLOInRpt = SLOInReport.objects.create(date=datetime.now(), goalText=form.cleaned_data['text'], slo = sloInRpt.slo, changedFromPrior=False, firstInstance=False)
        return super(EditImportedSLO, self).form_valid(form)
class EditNewSLO(FormView):
    template_name = "makeReports/editNewSLO.html"
    form_class = EditNewSLO
    success_url = ""
    def form_valid(self, form):
        sloIR = SLOInReport.objects.get(pk=self.request.GET['sloIR'])
        sloIR.goalText = form.cleaned_data['text']
        sloIR.date = datetime.now()
        sloIR.slo.blooms = form.cleaned_data['blooms']
        sloIR.slo.gradGoals = form.cleaned_data['gradGoals']
class StakeholderEntry(FormView):
    template_name = "makeReports/stakeholdersSLO.html"
    form_class = SLOsToStakeholderEntry
    success_url = ""
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.request.GET['report'])
        SLOsToStakeholder.objects.create(text=form.cleaned_data['text'], report = rpt)
        return super(StakeholderEntry,self).form_valid(form)
    