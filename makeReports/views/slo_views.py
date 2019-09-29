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
    template_name ="makeReports/SLO/sloSummary.html"
    context_object_name = "slo_list"
    def get_queryset(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        objs = SLOInReport.objects.filter(report=report)
        return objs
    def get_context_data(self, **kwargs):
        context = super(SLOSummary, self).get_context_data()
        context['rptPK'] = self.kwargs['report']
        return context
class AddNewSLO(FormView):
    template_name = "makeReports/SLO/addSLO.html"
    form_class = CreateNewSLO
    #success_url = reverse_lazy('makeReports:slo-summary', rpt=)
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def form_valid(self, form):
        gGoals = form.cleaned_data["gradGoals"]
        rpt = Report.objects.get(pk=self.kwargs['report'])
        sloObj = SLO.objects.create(blooms=form.cleaned_data['blooms'])
        sloObj.gradGoals.set(form.cleaned_data['gradGoals'])
        sloRpt = SLOInReport.objects.create(date=datetime.now(), goalText =form.cleaned_data['text'], slo=sloObj, firstInstance= True, changedFromPrior=False, report=rpt)
        sloObj.save()
        sloRpt.save()
        return super(AddNewSLO, self).form_valid(form)
class ImportSLO(FormView):
    template_name = "makeReports/SLO/importSLO.html"
    form_class = ImportSLOForm
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportSLO,self).get_form_kwargs()
         r = Report.objects.get(pk=self.kwargs['report'])
         yearIn = r.year
         dPobj = r.degreeProgram
         kwargs['sloChoices'] = SLOInReport.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        for sloInRpt in form.cleaned_data['slo']:
            SLOInReport.objects.create(date=datetime.now(),goalText=sloInRpt.goalText,slo=sloInRpt.slo, firstInstance=False, report=rpt, changedFromPrior=False)
        return super(ImportSLO,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportSLO, self).get_context_data(**kwargs)
        context['currentDPpk'] = Report.objects.get(pk=self.kwargs['report']).degreeProgram.pk
        context['rpt']=self.kwargs['report']
        return context
class EditImportedSLO(FormView):
    template_name = "makeReports/SLO/editImportedSLO.html"
    form_class = EditImportedSLOForm
    def get_initial(self):
        initial = super(EditImportedSLO, self).get_initial()
        sloInRpt = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        initial['text'] = sloInRpt.goalText
        return initial
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def form_valid(self,form):
        r = Report.objects.get(pk=self.kwargs['report'])
        sloInRpt = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        newSLOInRpt = SLOInReport.objects.create(report=r,date=datetime.now(), goalText=form.cleaned_data['text'], slo = sloInRpt.slo, changedFromPrior=False, firstInstance=False)
        newSLOInRpt.save()
        return super(EditImportedSLO, self).form_valid(form)
class EditNewSLO(FormView):
    template_name = "makeReports/SLO/editNewSLO.html"
    form_class = EditNewSLOForm
    def get_initial(self):
        initial = super(EditNewSLO, self).get_initial()
        sloInRpt = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        initial['text'] = sloInRpt.goalText
        initial['blooms'] = sloInRpt.slo.blooms
        initial['gradGoals'] = sloInRpt.slo.gradGoals.all
        return initial
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def form_valid(self, form):
        sloIR = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        sloIR.goalText = form.cleaned_data['text']
        sloIR.date = datetime.now()
        sloIR.slo.blooms = form.cleaned_data['blooms']
        sloIR.slo.gradGoals.set(form.cleaned_data['gradGoals'])
        sloIR.save()
        sloIR.slo.save()
        return super(EditNewSLO,self).form_valid(form)
class StakeholderEntry(FormView):
    template_name = "makeReports/SLO/stakeholdersSLO.html"
    form_class = Single2000Textbox
    success_url = ""
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        SLOsToStakeholder.objects.create(text=form.cleaned_data['text'], report = rpt)
        return super(StakeholderEntry,self).form_valid(form)
class Section1Comment(FormView):
    template_name = ""
    form_class = Single2000Textbox
    success_url = ""
    def form_valid(self, form):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        rpt.section1Comment = form.cleaned_data['text']
        rpt.save()
        return super(Section1Comment,self).form_valid(form)