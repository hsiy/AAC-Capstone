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
from makeReports.views.helperFunctions.section_context import *
from django_weasyprint import WeasyTemplateResponseMixin, WeasyTemplateView

class GradedRubricPDFGen(WeasyTemplateView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "makeReports/Grading/feedbackPDF.html"
    pdf_stylesheets =[
        # Change this to suit your css path
        #settings.STATIC_ROOT + '\\css\\bootstrap.min-color.css',
        settings.STATIC_ROOT + '\\css\\bootstrap-print-color.css',
        #settings.BASE_DIR + 'css/main.css',
    ]
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(GradedRubricPDFGen,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(GradedRubricPDFGen,self).get_context_data(**kwargs)
        context['rubric'] = self.report.rubric
        context['GRIs1'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=1)
        context['GRIs2'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=2)
        context['GRIs3'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=3)
        context['GRIs4'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=4)
        return context
    def test_func(self):
        dept= (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
class ReportPDFGen(WeasyTemplateView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "makeReports/DisplayReport/pdf.html"
    pdf_stylesheets =[
        #settings.STATIC_ROOT + '\\css\\bootstrap-print-color.css',
        #settings.BASE_DIR + 'css/main.css',
    ]
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(ReportPDFGen,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(ReportPDFGen,self).get_context_data(**kwargs)
        context['rubric'] = self.report.rubric
        context['report'] = self.report
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
    def test_func(self):
        dept= (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
