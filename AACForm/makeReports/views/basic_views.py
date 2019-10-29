from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *

class HomePage(ListView):
    """
    Home page view
    """
    template_name = "makeReports/home.html"
    model = Report
    def get_queryset(self):
        """
        When logged in, this returns unsubmitted reports within the user's department

        Returns:
            QuerySet : reports that need work
        """
        try:
            objs = Report.objects.filter(
                degreeProgram__department=self.request.user.profile.department, 
                submitted=False, 
                degreeProgram__active=True
                )
        except:
            objs = None
        return objs
    def get_context_data(self, **kwargs):
        """
        Returns context for template, including the current user, graded reports, and announcements

        Returns:
            dict : template context
        """
        context=super(HomePage,self).get_context_data(**kwargs)
        try:
            context['user']=self.request.user
            context['gReps'] = Report.objects.filter(degreeProgram__department=self.request.user.profile.department,rubric__complete=True, year=int(datetime.now().year))
            context['announ'] = Announcement.objects.filter(expiration__gte=datetime.now()).order_by("-creation")
        except:
            pass
        return context
class FacultyReportList(LoginRequiredMixin,ListView):
    """
    View to list all reports within the department
    """
    template_name = "makeReports/reportList.html"
    model = Report
    def get_queryset(self):
        objs = Report.objects.filter(
            degreeProgram__department=self.request.user.profile.department, 
            degreeProgram__active=True
            )
        return objs
class ReportListSearchedDept(LoginRequiredMixin,ListView):
    """
    View to search all reports within a department

    Notes:
        Search parameters sent through get request, with 'year', 
        'submitted', 'graded', and 'dP' for primary key of degree program
    """
    model = Report
    template_name = "makeReports/reportList.html"
    def get_queryset(self):
        """
        Gets QuerySet based upon search parameters
        
        Returns:
            QuerySet : reports within department matching search
        """
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
class DisplayReport(DeptAACMixin,TemplateView):
    """
    View to see report

    Keyword Args:
        pk (str): primary key of report to display
    """
    template_name = "makeReports/DisplayReport/report.html"
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view and attaches report to instance
        """
        self.report = Report.objects.get(pk=self.kwargs['pk'])
        return super(DisplayReport,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        """
        Gets template context, including the report, report supplements, and context needed 
        for displaying all 4 sections

        Returns:
            dict : context for template
        """
        context = super(DisplayReport,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['reportSups'] = ReportSupplement.objects.filter(report=self.report)
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
class UserModifyAccount(LoginRequiredMixin,FormView):
    """
    View to update a user's own account
    """
    form_class = UserUpdateUserForm
    success_url = reverse_lazy('makeReports:home-page')
    template_name = "makeReports/AACAdmin/modify_account.html"
    def dispatch(self, request,*args,**kwargs):
        """
        Dispatches view and attaches user to instance
        """
        self.userToChange = self.request.user
        return super(UserModifyAccount,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        """
        Initializes form based upon the current values

        Returns:
            dict : initial form values
        """
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
class HelpPage(TemplateView):
    """
    View of help page
    """
    template_name = "makeReports/help.html"
