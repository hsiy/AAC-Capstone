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
from makeReports.views.helperFunctions.section_context import *
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
        try:
            context['user']=self.request.user
            context['gReps'] = Report.objects.filter(degreeProgram__department=self.request.user.profile.department,rubric__complete=True, year=int(datetime.now().year))
        except:
            pass
        return context
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
class DisplayReport(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name = "makeReports/DisplayReport/report.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['pk'])
        return super(DisplayReport,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(DisplayReport,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['reportSups'] = ReportSupplement.objects.filter(report=self.report)
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
    def test_func(self):
        return getattr(self.request.user.profile, "aac") or (self.report.degreeProgram.department == self.request.user.profile.department)
class UserModifyAccount(FormView):
    form_class = UserUpdateUserForm
    success_url = reverse_lazy('makeReports:home-page')
    template_name = "makeReports/AACAdmin/modify_account.html"
    def dispatch(self, request,*args,**kwargs):
        self.userToChange = self.request.user
        return super(UserModifyAccount,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(UserModifyAccount,self).get_initial()
        try:
            initial['first_name'] = self.userToChange.first_name
            initial['last_name'] = self.userToChange.last_name
            initial['email'] = self.userToChange.email
        except:
            pass
        return initial
    def form_valid(self,form):
        self.userToChange.first_name = form.cleaned_data['first_name']
        self.userToChange.last_name = form.cleaned_data['last_name']
        self.userToChange.email = form.cleaned_data['email']
        self.userToChange.save()
        return super(UserModifyAccount,self).form_valid(form)