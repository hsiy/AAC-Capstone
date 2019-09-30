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

class Section1Grading(FormView):
    form_class = SectionRubricForm
    template_name = ""
    def get_form_kwargs(self):
        kwargs= super(Section1Grading,self).get_form_kwargs()
        r = Report.objects.get(pk=self.kwargs['report'])
        kwargs['rubricItems'] = RubricItem.objects.filter(rubricVersion=r.rubric.rubricVersion,section=1, order_by="order")
        self.kwargs['rubricItems'] = kwargs['rubricItems']
        return kwargs
    def form_valid(self,form):
        r = Report.objects.get(pk=self.kwargs['report'])
        rIs = self.kwargs['rubricItems']
        i=0
        for ri in rIs:
            newGRI = GradedRubricItem.objects.create(rubric=r.rubric, item=ri, grade=form.cleaned_data["rI"+str(i)])
            i+=1
        r.rubric.section1Comment = form.cleaned_data['section_comment']
        r.rubric.save()
        return super(Section1Grading,self).form_valid(form)
class Section2Grading(FormView):
    form_class = SectionRubricForm
    template_name = ""
    def get_form_kwargs(self):
        kwargs= super(Section1Grading,self).get_form_kwargs()
        r = Report.objects.get(pk=self.kwargs['report'])
        kwargs['rubricItems'] = RubricItem.objects.filter(rubricVersion=r.rubric.rubricVersion,section=2)
        return kwargs
    def form_valid(self,form):
        r = Report.objects.get(pk=self.kwargs['report'])
        rIs = self.kwargs['rubricItems']
        i=0
        for ri in rIs:
            newGRI = GradedRubricItem.objects.create(rubric=r.rubric, item=ri, grade=form.cleaned_data["rI"+str(i)])
            i+=1
        r.rubric.section2Comment = form.cleaned_data['section_comment']
        r.rubric.save()
        return super(Section2Grading,self).form_valid(form)
class Section3Grading(FormView):
    form_class = SectionRubricForm
    template_name = ""
    def get_form_kwargs(self):
        kwargs= super(Section1Grading,self).get_form_kwargs()
        r = Report.objects.get(pk=self.kwargs['report'])
        kwargs['rubricItems'] = RubricItem.objects.filter(rubricVersion=r.rubric.rubricVersion,section=3)
        return kwargs
    def form_valid(self,form):
        r = Report.objects.get(pk=self.kwargs['report'])
        rIs = self.kwargs['rubricItems']
        i=0
        for ri in rIs:
            newGRI = GradedRubricItem.objects.create(rubric=r.rubric, item=ri, grade=form.cleaned_data["rI"+str(i)])
            i+=1
        r.rubric.section3Comment = form.cleaned_data['section_comment']
        r.rubric.save()
        return super(Section3Grading,self).form_valid(form)
class Section4Grading(FormView):
    form_class = SectionRubricForm
    template_name = ""
    def get_form_kwargs(self):
        kwargs= super(Section1Grading,self).get_form_kwargs()
        r = Report.objects.get(pk=self.kwargs['report'])
        kwargs['rubricItems'] = RubricItem.objects.filter(rubricVersion=r.rubric.rubricVersion,section=4)
        return kwargs
    def form_valid(self,form):
        r = Report.objects.get(pk=self.kwargs['report'])
        rIs = self.kwargs['rubricItems']
        i=0
        for ri in rIs:
            newGRI = GradedRubricItem.objects.create(rubric=r.rubric, item=ri, grade=form.cleaned_data["rI"+str(i)])
            i+=1
        r.rubric.section4Comment = form.cleaned_data['section_comment']
        r.rubric.save()
        return super(Section4Grading,self).form_valid(form)