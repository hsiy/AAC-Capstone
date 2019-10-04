from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, DetailView
from django.views.generic import RedirectView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin

class AdminHome(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/AACAdmin/adminHome.html"
    form_class = GenerateReports
    success_url = reverse_lazy('makeReports:gen-rpt-suc')
    def form_valid(self, form):
        #generate this years reports
        thisYear = datetime.now().year
        dPs = DegreeProgram.objects.all()
        for dP in dPs:
            if dP.cycle and dP.cycle > 0:
                if (thisYear - dP.startingYear) % (dP.cycle) == 0:
                    #if a report for the degree program/year already
                    # exists, this won't create a new one
                    try:
                        Report.objects.get(year=thisYear, degreeProgram=dP)
                    except:
                        gR = GradedRubric.objects.create(rubricVersion = form.cleaned_data['rubric'])
                        Report.objects.create(year=thisYear, degreeProgram=dP,rubric=gR, submitted = False)
        return super(AdminHome, self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class GenerateReportSuccess(TemplateView):
    template_name = "makeReports/AACAdmin/genRptSuc.html"
class CreateCollege(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = College
    template_name = "makeReports/AACAdmin/addCollege.html"
    fields = ['name']
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class UpdateCollege(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = College
    template_name = "makeReports/AACAdmin/updateCollege.html"
    fields = ['name']
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeleteCollege(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = College
    fields = ['active']
    template_name = "makeReports/AACAdmin/deleteCollege.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class RecoverCollege(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = College
    fields = ['active']
    template_name = "makeReports/AACAdmin/recoverCollege.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class CollegeList(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = College
    template_name = "makeReports/AACAdmin/collegeList.html"
    def get_queryset(self):
        objs = College.active_objects.all()
        return objs
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class CreateDepartment(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Department
    #fields = ['name', 'college']
    form_class = CreateDepartmentForm
    template_name = "makeReports/AACAdmin/addDepartment.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DepartmentList(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Department
    template_name = "makeReports/AACAdmin/deptList.html"
    def get_queryset(self):
        objs = Department.active_objects.order_by('college__name')
        return objs
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class UpdateDepartment(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Department
    fields = ['name', 'college']
    template_name = "makeReports/AACAdmin/updateDepartment.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeleteDepartment(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Department
    fields = ['active']
    template_name = "makeReports/AACAdmin/deleteDept.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class RecoverDepartment(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Department
    fields = ['active']
    template_name = "makeReports/AACAdmin/recoverDept.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class CreateDegreeProgram(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = DegreeProgram
    fields=['name','level','cycle','startingYear']
    template_name = "makeReports/AACAdmin/addDP.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def form_valid(self, form):
        form.instance.department = Department.objects.get(pk=int(self.kwargs['dept']))
        return super(CreateDegreeProgram, self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class UpdateDegreeProgram(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = DegreeProgram
    form_class = CreateDPByDept
    template_name = "makeReports/AACAdmin/updateDP.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeleteDegreeProgram(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = DegreeProgram
    fields = ['active']
    template_name = "makeReports/AACAdmin/deleteDP.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class RecoverDegreeProgram(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = DegreeProgram
    fields = ['active']
    template_name = "makeReports/AACAdmin/recoverDP.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DegreeProgramList(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = DegreeProgram
    template_name = "makeReports/AACAdmin/dpList.html"
    def dispatch(self, *args, **kwargs):
        self.dept = Department.objects.get(pk=int(self.kwargs['dept']))
        return super(DegreeProgramList, self).dispatch(args,kwargs)
    def get_queryset(self):
        objs = DegreeProgram.active_objects.filter(department=self.dept)
        return objs
    def get_context_data(self, **kwargs):
        context = super(DegreeProgramList, self).get_context_data(**kwargs)
        context['dept'] = self.dept
        return context
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class CreateReport(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Report
    form_class = CreateReportByDept
    template_name = "makeReports/AACAdmin/manualReportCreate.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def get_form_kwargs(self):
        kwargs = super(CreateReport, self).get_form_kwargs()
        kwargs['dept'] = self.kwargs['dept']
        return kwargs
    def form_valid(self, form):
        form.instance.submitted = False
        return super(CreateReport, self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeleteReport(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Report
    template_name = "makeReports/AACAdmin/deleteReport.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ReportList(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Report
    template_name = "makeReports/AACAdmin/reportList.html"
    def get_queryset(self):
        qs = Report.objects.filter(year=int(datetime.now().year), degreeProgram__active=True).order_by('submitted','-rubric__complete')
        return qs
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ReportListSearched(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Report
    template_name = "makeReports/AACAdmin/reportList.html"
    def get_queryset(self):
        year = self.request.GET['year']
        submitted = self.request.GET['submitted']
        x=self.request.GET
        graded = self.request.GET['graded']
        dP = self.request.GET['dP']
        dept = self.request.GET['dept']
        college = self.request.GET['col']
        objs = Report.objects.filter(degreeProgram__active=True).order_by('submitted','-rubric__complete')
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
        if dept!="":
            objs=objs.filter(degreeProgram__department__name__icontains=dept)
        if college!="":
            objs=objs.filter(degreeProgram__department__college__name__icontains=college)
        return objs
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ArchivedColleges(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = College
    template_name = "makeReports/AACAdmin/archivedColleges.html"
    def get_queryset(self):
        return College.objects.filter(active=False)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ArchivedDepartments(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Department
    template_name = "makeReports/AACAdmin/archivedDepartments.html"
    def get_queryset(self):
        return Department.objects.filter(active=False)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ArchivedDegreePrograms(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = DegreeProgram
    template_name = "makeReports/AACAdmin/archivedDPs.html"
    def dispatch(self, *args, **kwargs):
        self.dept = Department.objects.get(pk=int(self.kwargs['dept']))
        return super(ArchivedDegreePrograms, self).dispatch(args,kwargs)
    def get_queryset(self):
        return DegreeProgram.objects.filter(active=False, department=self.dept)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
    def get_context_data(self, **kwargs):
        context = super(ArchivedDegreePrograms, self).get_context_data(**kwargs)
        context['dept'] = self.dept
        return context
class MakeAccount(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/AACAdmin/create_account.html"
    form_class = MakeNewAccount
    success_url = reverse_lazy('makeReports:admin-home')
    def form_valid(self,form):
        form.save()
        return super(MakeAccount,self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ModifyAccount(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Profile
    success_url = reverse_lazy('makeReports:admin-home')
    template_name = "makeReports/AACAdmin/modify_account.html"
    fields = ['aac','department']
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class InactivateUser(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = User
    success_url = reverse_lazy('makeReports:admin-home')
    template_name = "makeReports/AACAdmin/inactivate_account.html"
    fields = ['is_active']
    def test_func(self):
        return getattr(self.request.user.profile, "aac")


