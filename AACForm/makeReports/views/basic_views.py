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
class HomePage(ListView):
    template_name = "makeReports/home.html"
    model = Report
    def get_queryset(self):
        try:
            objs = Report.objects.filter(degreeProgram__department=self.request.user.profile.department, submitted=False, degreeProgram__active=True)
        except:
            objs = None
        return objs
    def get_context_data(self, **kwargs):
        context=super(HomePage,self).get_context_data(**kwargs)
        context['user']=self.request.user
        return context
#class FacultyHome(ListView):
#    template_name = "makeReports/facultyHome.html"
#    model = Report
#    def get_queryset(self):
#        objs = Report.objects.filter(degreeProgram__department=self.request.user.profile.department, submitted=False)
#        return objs
class FacultyReportList(LoginRequiredMixin,ListView):
    template_name = "makeReports/reportList.html"
    model = Report
    def get_queryset(self):
        objs = Report.objects.filter(degreeProgram__department=self.request.user.profile.department, degreeProgram__active=True)
        return objs
class ReportListSearchedDept(LoginRequiredMixin,ListView):
    model = Report
    template_name = "makeReports/reportList.html"
    def get_queryset(self):
        year = self.request.GET['year']
        submitted = self.request.GET['submitted']
        graded = self.request.GET['graded']
        dP = self.request.GET['dP']
        objs = Report.objects.filter(degreeProgram__department=self.request.user.profile.department, degreeProgram__active=True).order_by('submitted','-rubric__complete')
        if year!="":
            objs=objs.filter(year=year)
        if submitted == "S":
            objs=objs.filter(submitted=True)
        elif submitted == "nS":
            objs=objs.filter(submitted=False)
        if graded=="S":
            objs=objs.filter(rubric__complete=True)
        elif graded=="nS":
            objs=objs.filter(rubric__complete=False)
        if dP!="":
            objs=objs.filter(degreeProgram__name__icontains=dP)
        return objs