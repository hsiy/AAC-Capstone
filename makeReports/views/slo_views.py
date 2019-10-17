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
from django_summernote.widgets import SummernoteWidget
from makeReports.views.helperFunctions.mixins import *

class SLOSummary(DeptReportMixin,ListView):
    model = SLOInReport
    template_name ="makeReports/SLO/sloSummary.html"
    context_object_name = "slo_list"
    def get_queryset(self):
        report = self.report
        objs = SLOInReport.objects.filter(report=report).order_by("number")
        return objs
    def get_context_data(self, **kwargs):
        context = super(SLOSummary, self).get_context_data()
        context['stk'] = SLOsToStakeholder.objects.filter(report=self.report).last()
        return context
class AddNewSLO(DeptReportMixin,FormView):
    template_name = "makeReports/SLO/addSLO.html"
    form_class = CreateNewSLO
    def get_form_kwargs(self):
        kwargs = super(AddNewSLO,self).get_form_kwargs()
        if self.report.degreeProgram.level == "GR":
            kwargs['grad'] = True
        else:
            kwargs['grad'] = False
        return kwargs
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self, form):
        try:
            gGoals = form.cleaned_data["gradGoals"]
        except:
            gGoals = []
        rpt = self.report
        sloObj = SLO.objects.create(blooms=form.cleaned_data['blooms'])
        sloObj.gradGoals.add(gGoals)
        self.report.numberOfSLOs += 1
        self.report.save()
        sloRpt = SLOInReport.objects.create(
            date=datetime.now(), 
            goalText =form.cleaned_data['text'], 
            slo=sloObj, 
            changedFromPrior=False, 
            report=rpt, 
            number=self.report.numberOfSLOs
            )
        sloObj.save()
        sloRpt.save()
        return super(AddNewSLO, self).form_valid(form)
class ImportSLO(DeptReportMixin,FormView):
    template_name = "makeReports/SLO/importSLO.html"
    form_class = ImportSLOForm
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportSLO,self).get_form_kwargs()
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         sloChoices = SLOInReport.objects.filter(
             report__year=yearIn, 
             report__degreeProgram=dPobj
             ).order_by("number")
         slosInReport = SLOInReport.objects.filter(report=self.report).order_by("number")
         for slo in slosInReport:
             sloChoices = sloChoices.exclude(slo=slo.slo)
         kwargs['sloChoices'] = sloChoices
         return kwargs
    def form_valid(self,form):
        rpt = self.report
        num = rpt.numberOfSLOs
        for sloInRpt in form.cleaned_data['slo']:
            num += 1
            newS = SLOInReport.objects.create(
                date=datetime.now(),
                number=num,
                goalText=sloInRpt.goalText,
                slo=sloInRpt.slo,
                report=rpt, 
                changedFromPrior=False)
            newS.slo.numberOfUses += 1
            newS.slo.save()
            if form.cleaned_data['importAssessments']:
                    assessSet = AssessmentVersion.objects.filter(slo=sloInRpt)
                    for assess in assessSet:
                        newA = AssessmentVersion.objects.create(
                            report=self.report,
                            slo = newS,
                            number=newS.numberOfAssess+1,
                            changedFromPrior=False,
                            assessment = assess.assessment,
                            date = datetime.now(),
                            description = assess.description,
                            finalTerm = assess.finalTerm,
                            where = assess.where,
                            allStudents = assess.allStudents,
                            sampleDescription = assess.sampleDescription,
                            frequency = assess.frequency,
                            threshold = assess.threshold,
                            target = assess.target
                            )
                        assess.assessment.numberOfUses += 1
                        assess.assessment.save()
                        for aSup in assess.supplements.all():
                            newA.supplements.add(a)
                        newA.save()
                        newS.numberOfAssess += 1
                        newS.save()
        self.report.numberOfSLOs = num
        self.report.save()
        return super(ImportSLO,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportSLO, self).get_context_data(**kwargs)
        r = self.report
        context['currentDPpk'] = Report.objects.get(pk=self.kwargs['report']).degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=r.degreeProgram.department)
        return context
class EditImportedSLO(DeptReportMixin,FormView):
    template_name = "makeReports/SLO/editImportedSLO.html"
    form_class = EditImportedSLOForm
    def dispatch(self,request,*args,**kwargs):
        self.sloInRpt = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        return super(EditImportedSLO,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(EditImportedSLO, self).get_initial()
        initial['text'] = self.sloInRpt.goalText
        return initial
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self,form):
        r = self.report
        self.sloInRpt.date=datetime.now()
        self.sloInRpt.goalText=form.cleaned_data['text']
        self.sloInRpt.changedFromPrior = True
        self.sloInRpt.save()
        return super(EditImportedSLO, self).form_valid(form)
class EditNewSLO(DeptReportMixin,FormView):
    template_name = "makeReports/SLO/editNewSLO.html"
    form_class = EditNewSLOForm
    def dispatch(self,request,*args,**kwargs):
        self.sloInRpt = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        return super(EditNewSLO,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs = super(EditNewSLO,self).get_form_kwargs()
        if self.report.degreeProgram.level == "GR":
            kwargs['grad'] = True
            self.grad = True
        else:
            kwargs['grad'] = False
            self.grad = False
        return kwargs
    def get_initial(self):
        initial = super(EditNewSLO, self).get_initial()
        initial['text'] = self.sloInRpt.goalText
        initial['blooms'] = self.sloInRpt.slo.blooms
        initial['gradGoals'] = self.sloInRpt.slo.gradGoals.all
        return initial
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.sloInRpt.goalText = form.cleaned_data['text']
        self.sloInRpt.date = datetime.now()
        self.sloInRpt.slo.blooms = form.cleaned_data['blooms']
        if self.grad:
            self.sloInRpt.slo.gradGoals.add(form.cleaned_data['gradGoals'])
        self.sloInRpt.save()
        self.sloInRpt.slo.save()
        return super(EditNewSLO,self).form_valid(form)
class StakeholderEntry(DeptReportMixin,FormView):
    template_name = "makeReports/SLO/stakeholdersSLO.html"
    form_class = Single2000Textbox
    def dispatch(self,request,*args,**kwargs):
        self.sts = SLOsToStakeholder.objects.filter(report=self.report).last()
        return super(StakeholderEntry,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def get_initial(self):
        initial = super(StakeholderEntry,self).get_initial()
        try:
            #if sts:
            initial['text']=self.sts.text
        except:
            pass
        return initial
    def form_valid(self,form):
        try:
            self.sts.text = form.cleaned_data['text']
            self.sts.save()
        except Exception as e:
            sTs = SLOsToStakeholder.objects.create(text=form.cleaned_data['text'], report=self.report)
        return super(StakeholderEntry,self).form_valid(form)
class ImportStakeholderEntry(DeptReportMixin,FormView):
    template_name = "makeReports/SLO/importStakeholderComm.html"
    form_class = ImportStakeholderForm
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-stakeholders', args=[self.report.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportStakeholderEntry,self).get_form_kwargs()
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         kwargs['stkChoices'] = SLOsToStakeholder.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        oldSTS = form.cleaned_data["stk"]
        try:
            sts = SLOsToStakeholder.objects.filter(report=self.report).first()
            if oldSTS.report == self.report:
                pass
            elif sts:
                sts.text = form.cleaned_data['stk'].text
                sts.save()
            else:
                sTsNew = SLOsToStakeholder.objects.create(text=form.cleaned_data['stk'].text, report=self.report)
        except:
            sTs = SLOsToStakeholder.objects.create(text=form.cleaned_data['stk'].text, report=self.report)
        return super(ImportStakeholderEntry,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportStakeholderEntry, self).get_context_data(**kwargs)
        context['currentDPpk'] = self.report.degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=self.report.degreeProgram.department)
        return context
class Section1Comment(DeptReportMixin,FormView):
    template_name = "makeReports/SLO/sloComment.html"
    form_class = Single2000Textbox
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.report.section1Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section1Comment,self).form_valid(form)
    def get_initial(self):
        initial = super(Section1Comment,self).get_initial()
        initial['text']="No comment."
        return initial
class DeleteImportedSLO(DeptReportMixin,DeleteView):
    model = SLOInReport
    template_name = "makeReports/SLO/deleteSLO.html"
    def dispatch(self,request,*args,**kwargs):
        SLOIR = SLOInReport.objects.get(pk=self.kwargs['pk'])
        self.oldNum = SLOIR.number
        self.slo = SLOIR.slo
        self.assess = Assessment.objects.filter(assessmentversion__slo=SLOIR).distinct()
        return super(DeleteImportedSLO,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        oldNum = self.oldNum
        num = self.report.numberOfSLOs
        if self.slo.numberOfUses <= 1:
            self.slo.delete()
        else:
            self.slo.numberOfUses -= 1
            self.slo.save()
        slos = SLOInReport.objects.filter(report=self.report).order_by("number")
        for slo in slos:
            if slo.number > oldNum:
                slo.number -= 1
                slo.save()
        self.report.numberOfSLOs -= 1
        self.report.save()
        for a in self.assess:
            if a.numberOfUses == 1:
                a.delete()
            else:
                a.numberOfUse -= 1
                a.save()
        dAs = DecisionsActions.objects.filter(report=self.report, SLO=self.slo)
        for dA in dAs:
            dA.delete()
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class DeleteNewSLO(DeptReportMixin,DeleteView):
    model = SLOInReport
    template_name = "makeReports/SLO/deleteSLO.html"
    def dispatch(self,request,*args,**kwargs):
        SLOIR = SLOInReport.objects.get(pk=self.kwargs['pk'])
        self.slo = SLOIR.slo
        self.oldNum = SLOIR.number
        self.assess = Assessment.objects.filter(assessmentversion__slo=SLOIR).distinct()
        return super(DeleteNewSLO,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        oldNum = self.oldNum
        otherSLOs = SLOInReport
        slo = self.slo
        slo.delete()
        num = self.report.numberOfSLOs
        slos = SLOInReport.objects.filter(report=self.report).order_by("number")
        for slo in slos:
            if slo.number > oldNum:
                slo.number -= 1
                slo.save()
        self.report.numberOfSLOs -= 1
        self.report.save()
        for a in self.assess:
            if a.numberOfUses == 1:
                a.delete()
            else:
                a.numberOfUse -= 1
                a.save()
        dAs = DecisionsActions.objects.filter(report=self.report, SLO=self.slo)
        for dA in dAs:
            dA.delete()
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])