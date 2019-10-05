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
def generateRubricItems(rIs,form,r):
    for ri in rIs:
        if form.cleaned_data["rI"+str(ri.pk)]:
            try:
                GRI = GradedRubricItem.objects.get(rubric=r.rubric, item=ri)
                GRI.grade=form.cleaned_data["rI"+str(ri.pk)]
            except:
                gr = form.cleaned_data["rI"+str(ri.pk)]
                if gr and (gr is not ""):
                    newGRI = GradedRubricItem.objects.create(rubric=r.rubric, item=ri, grade=form.cleaned_data["rI"+str(ri.pk)])
def getInitialRubric(rIs, r, initial):
    for ri in rIs:
        try:
            GRI = GradedRubricItem.objects.get(rubric=r.rubric, item=ri)
            initial["rI"+str(ri.pk)]=GRI.grade
        except:
            pass
    return initial
@register.simple_tag
def get_item(dictionary, key1, key2):
    s = dictionary.get(key1)
    if s:
        return s[key2]
    else:
        return ""
class Section1Grading(LoginRequiredMixin,UserPassesTestMixin,FormView):
    form_class = SectionRubricForm
    template_name = "makeReports/Grading/grading_section.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.rubricItems = RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion,section=1).order_by("order","pk")
        return super(Section1Grading,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs= super(Section1Grading,self).get_form_kwargs()
        kwargs['rubricItems'] = self.rubricItems
        return kwargs
    def form_valid(self,form):
        generateRubricItems(self.rubricItems,form,self.report)
        self.report.rubric.section1Comment = form.cleaned_data['section_comment']
        self.report.rubric.save()
        return super(Section1Grading,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(Section1Grading,self).get_context_data(**kwargs)
        context['section'] = 1
        context['report'] = self.report
        extraHelp = dict()
        for rI in self.rubricItems:
            extraHelp["rI"+str(rI.pk)] = [rI.DMEtext, rI.MEtext, rI.EEtext]
        context['extraHelp']=extraHelp
        return context
    def get_initial(self):
        initial = super(Section1Grading,self).get_initial()
        initial = getInitialRubric(self.rubricItems,self.report,initial)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class Section2Grading(LoginRequiredMixin,UserPassesTestMixin,FormView):
    form_class = SectionRubricForm
    template_name = ""
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.rubricItems = RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion,section=2).order_by("order","pk")
        return super(Section2Grading,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs= super(Section2Grading,self).get_form_kwargs()
        kwargs['rubricItems'] = self.rubricItems
        return kwargs
    def form_valid(self,form):
        generateRubricItems(self.rubricItems,form,self.report)
        self.report.rubric.section2Comment = form.cleaned_data['section_comment']
        self.report.rubric.save()
        return super(Section2Grading,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(Section2Grading,self).get_context_data(**kwargs)
        context['section'] = 2
        context['report'] = self.report
        return context
    def get_initial(self):
        initial = super(Section2Grading,self).get_initial()
        initial = getInitialRubric(self.rubricItems,self.report,initial)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class Section3Grading(LoginRequiredMixin,UserPassesTestMixin,FormView):
    form_class = SectionRubricForm
    template_name = ""
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.rubricItems = RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion,section=3).order_by("order","pk")
        return super(Section3Grading,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs= super(Section3Grading,self).get_form_kwargs()
        kwargs['rubricItems'] = self.rubricItems
        return kwargs
    def form_valid(self,form):
        generateRubricItems(self.rubricItems,form,self.report)
        self.report.rubric.section3Comment = form.cleaned_data['section_comment']
        self.report.rubric.save()
        return super(Section3Grading,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(Section3Grading,self).get_context_data(**kwargs)
        context['section'] = 3
        context['report'] = self.report
        return context
    def get_initial(self):
        initial = super(Section3Grading,self).get_initial()
        initial = getInitialRubric(self.rubricItems,self.report,initial)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class Section4Grading(LoginRequiredMixin,UserPassesTestMixin,FormView):
    form_class = SectionRubricForm
    template_name = ""
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.rubricItems = RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion,section=4).order_by("order","pk")
        return super(Section4Grading,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs= super(Section4Grading,self).get_form_kwargs()
        kwargs['rubricItems'] = self.rubricItems
        return kwargs
    def form_valid(self,form):
        generateRubricItems(self.rubricItems,form,self.report)
        self.report.rubric.section4Comment = form.cleaned_data['section_comment']
        self.report.rubric.save()
        return super(Section1Grading,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(Section1Grading,self).get_context_data(**kwargs)
        context['section'] = 4
        context['report'] = self.report
        return context
    def get_initial(self):
        initial = super(Section4Grading,self).get_initial()
        initial = getInitialRubric(self.rubricItems,self.report,initial)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class RubricReview(LoginRequiredMixin,UserPassesTestMixin, ListView, FormMixin):
    model = GradedRubricItem
    template_name = "makeReports/Grading/rubric_review.html"
    form_class = SubmitGrade
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.GRIs = GradedRubricItem.objects.filter(report=self.report)
        return super(RubricReview,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs=super(RubricReview,self).dispatch(request,*args,**kwargs)
        #valid iff there's a graded rubric item for every rubric item
        kwargs['valid'] = (self.GRIs.count == RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion).count())
    def form_valid(self,form):
        self.report.rubric.complete = True
        self.report.rubric.save()
        return super(RubricReview,self).form_valid(form)
    def get_queryset(self):
        return self.GRIs
    def get_success_url(self):
        return reverse_lazy('makeReports:ret-rept', args=[self.report.pk])
    def get_context_data(self, **kwargs):
        context = super(Section1Grading,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['gRub'] = self.report.rubric
        return context
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ReturnReport(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Report
    fields = ['returned']
    template_name = 'makeReports/Grading/returnReport.html'
    success_url = reverse_lazy('makeReports:admin-home')
    def form_valid(self,form):
        if form.cleaned_data['returned']:
            self.object.submitted = False
            self.object.rubric.complete = False
        return super(ReturnReport,self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class Feedback(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = GradedRubricItem
    template_name = "makeReports/Grading/feedback.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.GRIs = GradedRubricItem.objects.filter(report=self.report)
        return super(RubricReview,self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        return self.GRIs
    def get_success_url(self):
        return reverse_lazy('makeReports:ret-rept', args=[self.report.pk])
    def get_context_data(self, **kwargs):
        context = super(Section1Grading,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['gRub'] = self.report.rubric
        return context
    def test_func(self):
        rightDept = (self.report.degreeProgram.department == self.request.user.profile.department)
        feedbackToGive = self.report.rubric.complete or (self.report.returned and (not self.report.submitted))
        return rightDept and feedbackToGive