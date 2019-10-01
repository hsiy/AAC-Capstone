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
def generateRubricItems(rIs,form,r):
    i=0
    for ri in rIs:
        if form.cleaned_data["rI"+str(i)]:
            try:
                GRI = GradedRubricItem.objects.get(rubric=r.rubric, item=ri)
                GRI.grade=form.cleaned_data["rI"+str(i)]
            except:
                newGRI = GradedRubricItem.objects.create(rubric=r.rubric, item=ri, grade=form.cleaned_data["rI"+str(i)])
        i+=1
def getInitialRubric(rIs, r, initial):
    i=0
    for ri in rIs:
        try:
            GRI = GradedRubricItem.objects.get(rubric=r.rubric, item=ri)
            initial["rI"+str(i)]=GRI.grade
        except:
            pass
        i+=1
    return initial
class Section1Grading(LoginRequiredMixin,UserPassesTestMixin,FormView):
    form_class = SectionRubricForm
    template_name = ""
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
class AddRubric(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    template_name = ""
    success_url = ""
    model=Rubric
    fields = ['fullFile']
    def form_valid(self,form):
        form.instance.date = datetime.now()
        return super(AddRubric,self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class AddRubricItems(LoginRequiredMixin,UserPassesTestMixin, FormView):
    template_name = ""
    form_class = RubricItemFormset
    success_url = ""
    def form_valid(self,form):
        rVersion = Rubric.objects.get(pk=self.kwargs['rubric'])
        for f in form:
            ri = RubricItem.object.create(text=f.cleaned_data['text'], \
                 section=f.cleaned_data['section'], rubricVersion=rVersion, \
                      DMEtext=f.cleaned_data['DMEtext'], MEtext=f.cleaned_data['MEtext'], \
                          EEtext=f.cleaned_data['EEtext'])
            try:
                ri.order=f.cleaned_data['order']
            except:
                pass
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ViewRubric(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Rubric
    template_name = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class UpdateRubricItem(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = RubricItem
    fields = ['text','section','order','DMEtext','MEtext','EEtext']
    template_name = ""
    success_url = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class UpdateRubricFile(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Rubric
    fields = ['fullFile']
    template_name = ""
    success_url = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeleteRubricItem(LoginRequiredMixin,UserPassesTestMixin):
    #error will result if they try to delete a ri that already has a grade somewhere
    model = RubricItem
    template_name = ""
    success_url = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DuplicateRubric(LoginRequiredMixin,UserPassesTestMixin, FormView):
    #duplicate -> edit/delete/add intended workflow instead of some kind of import
    form_class = DuplicateRubric
    success_url = ""
    template_name = ""
    def form_valid(self,form):
        rubToDup = form.cleaned_data['rubToDup']
        RIs = RubricItem.objects.filter(rubricVersion=rubToDup)
        newRub = Rubric.object.create(date=datetime.now(), fullFile=rubToDup.fullFile)
        for ri in RIs:
            newRi = RubricItem.object.create(text=ri.text, section=ri.section, rubricVersion=newRub,order=ri.order,DMEtext=ri.DMEtext,MEtext=ri.MEtext,EEtext=ri.EEtext)
        return super(DuplicateRubric,)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")