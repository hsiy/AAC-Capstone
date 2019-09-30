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

class SLOSummary(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = SLOInReport
    template_name ="makeReports/SLO/sloSummary.html"
    context_object_name = "slo_list"
    def get_queryset(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        objs = SLOInReport.objects.filter(report=report)
        return objs
    def get_context_data(self, **kwargs):
        context = super(SLOSummary, self).get_context_data()
        context['rpt'] = Report.objects.get(pk=self.kwargs['report'])
        return context
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.department == self.request.user.profile.department)
class AddNewSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/addSLO.html"
    form_class = CreateNewSLO
    def get_form_kwargs(self):
        kwargs = super(AddNewSLO,self).get_form_kwargs()
        r = Report.objects.get(pk=self.kwargs['report'])
        if r.degreeProgram.level == "GR":
            kwargs['grad'] = True
        else:
            kwargs['grad'] = False
        return kwargs
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def form_valid(self, form):
        try:
            gGoals = form.cleaned_data["gradGoals"]
        except:
            gGoals = []
        rpt = Report.objects.get(pk=self.kwargs['report'])
        sloObj = SLO.objects.create(blooms=form.cleaned_data['blooms'])
        sloObj.gradGoals.set(gGoals)
        sloRpt = SLOInReport.objects.create(date=datetime.now(), goalText =form.cleaned_data['text'], slo=sloObj, firstInstance= True, changedFromPrior=False, report=rpt)
        sloObj.save()
        sloRpt.save()
        return super(AddNewSLO, self).form_valid(form)
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.department == self.request.user.profile.department)
class ImportSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/importSLO.html"
    form_class = ImportSLOForm
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportSLO,self).get_form_kwargs()
         #r = Report.objects.get(pk=self.kwargs['report'])
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         kwargs['sloChoices'] = SLOInReport.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        for sloInRpt in form.cleaned_data['slo']:
            SLOInReport.objects.create(date=datetime.now(),goalText=sloInRpt.goalText,slo=sloInRpt.slo, firstInstance=False, report=rpt, changedFromPrior=False)
        return super(ImportSLO,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportSLO, self).get_context_data(**kwargs)
        r = Report.objects.get(pk=self.kwargs['report'])
        context['currentDPpk'] = Report.objects.get(pk=self.kwargs['report']).degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=r.degreeProgram.department)
        context['rpt']=self.kwargs['report']
        return context
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.department == self.request.user.profile.department)
class EditImportedSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
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
        sloInRpt.date=datetime.now()
        sloInRpt.goalText=form.cleaned_data['text']
        sloInRpt.changedFromPrior = True
        sloInRpt.save()
        #newSLOInRpt = SLOInReport.objects.create(report=r,date=datetime.now(), goalText=form.cleaned_data['text'], slo = sloInRpt.slo, changedFromPrior=False, firstInstance=False)
        #newSLOInRpt.save()
        return super(EditImportedSLO, self).form_valid(form)
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.department == self.request.user.profile.department)
class EditNewSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
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
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.department == self.request.user.profile.department)
class StakeholderEntry(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/stakeholdersSLO.html"
    form_class = Single2000Textbox
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-comment', args=[r.pk])
    def get_initial(self):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        initial = super(StakeholderEntry,self).get_initial()
        sts = SLOsToStakeholder.objects.filter(report=rpt).first()
        try:
            sts = SLOsToStakeholder.objects.filter(report=rpt).first()
            #if sts:
            initial['text']=sts.text
        except:
            pass
        return initial
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        try:
            sts = SLOsToStakeholder.objects.get(report=rpt)
            sts.text = form.cleaned_data['text']
            sts.save()
        except:
            sTs = SLOsToStakeholder.objects.create(text=form.cleaned_data['text'], report=rpt)
        return super(StakeholderEntry,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(StakeholderEntry, self).get_context_data(**kwargs)
        r = Report.objects.get(pk=self.kwargs['report'])
        context['rpt']=r
        return context
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.departmentself.request.user.profile.department)
class ImportStakeholderEntry(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/importStakeholderComm.html"
    form_class = ImportStakeholderForm
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-stakeholders', args=[r.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportStakeholderEntry,self).get_form_kwargs()
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         kwargs['stkChoices'] = SLOsToStakeholder.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        oldSTS = form.cleaned_data["stk"]
        try:
            sts = SLOsToStakeholder.objects.filter(report=rpt).first()
            if oldSTS.report == rpt:
                pass
            elif sts:
                sts.text = form.cleaned_data['stk'].text
                sts.save()
            else:
                sTsNew = SLOsToStakeholder.objects.create(text=form.cleaned_data['stk'].text, report=rpt)
        except:
            sTs = SLOsToStakeholder.objects.create(text=form.cleaned_data['stk'].text, report=rpt)
        return super(ImportStakeholderEntry,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportStakeholderEntry, self).get_context_data(**kwargs)
        r = Report.objects.get(pk=self.kwargs['report'])
        context['currentDPpk'] = Report.objects.get(pk=self.kwargs['report']).degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=r.degreeProgram.department)
        context['rpt']=self.kwargs['report']
        return context
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.department == self.request.user.profile.department)
class Section1Comment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/sloComment.html"
    form_class = Single2000Textbox
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        #to be changed to assessment page!
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def form_valid(self, form):
        rpt = Report.objects.get(pk=self.kwargs['report'])
        rpt.section1Comment = form.cleaned_data['text']
        rpt.save()
        return super(Section1Comment,self).form_valid(form)
    def get_initial(self):
        initial = super(Section1Comment,self).get_initial()
        initial['text']="No comment."
        return initial
    def test_func(self):
        report = Report.objects.get(pk=self.kwargs['report'])
        return (report.degreeProgram.department == self.request.user.profile.department)
class DeleteImportedSLO(DeleteView):
    model = SLOInReport
    template_name = "makeReports/SLO/deleteSLO.html"
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        #to be changed to assessment page!
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
class DeleteNewSLO(DeleteView):
    model = SLOInReport
    template_name = "makeReports/SLO/deleteSLO.html"
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        #to be changed to assessment page!
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def form_valid(self,form):
        SLOIR = SLOInReport.objects.get(pk=self.kwargs['pk'])
        slo = SLOIR.slo
        slo.delete()
        slo.save()
        return super(DeleteNewSLO,self).form_valid(form)