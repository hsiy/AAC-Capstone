from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from makeReports.views.helperFunctions.mixins import *

class AdminHome(AACOnlyMixin,FormView):
    """
    Home page for AAC administration: mostly buttons to other page
    Does contain the form to generate all the reports for the year
    """
    template_name = "makeReports/AACAdmin/adminHome.html"
    form_class = GenerateReports
    success_url = reverse_lazy('makeReports:gen-rpt-suc')
    def form_valid(self, form):
        """
        Generates all reports in cycle for this year with given rubric (in form)
        """
        #generate this years reports
        thisYear = datetime.now().year
        dPs = DegreeProgram.objects.all()
        for dP in dPs:
            if dP.cycle and dP.cycle > 0:
                #checking cycles
                if (thisYear - dP.startingYear) % (dP.cycle) == 0:
                    #if a report for the degree program/year already
                    # exists, this won't create a new one
                    if Report.objects.filter(year=thisYear, degreeProgram=dP).count() == 0:
                        gR = GradedRubric.objects.create(rubricVersion = form.cleaned_data['rubric'])
                        Report.objects.create(year=thisYear, degreeProgram=dP,rubric=gR, submitted = False)
        return super(AdminHome, self).form_valid(form)

class GenerateReportSuccess(AACOnlyMixin,TemplateView):
    """
    Simple, static page to show success of generating report
    """
    template_name = "makeReports/AACAdmin/genRptSuc.html"

class CreateCollege(AACOnlyMixin,CreateView):
    """
    Creates a new college
    Upon success, goes to college-list page
    """
    model = College
    template_name = "makeReports/AACAdmin/CollegeDeptDP/addCollege.html"
    fields = ['name']
    success_url = reverse_lazy('makeReports:college-list')

class UpdateCollege(AACOnlyMixin,UpdateView):
    """
    Update college, no restrictions compared to new college

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report-models.College` to update
    """
    model = College
    template_name = "makeReports/AACAdmin/CollegeDeptDP/updateCollege.html"
    fields = ['name']
    success_url = reverse_lazy('makeReports:college-list')

class DeleteCollege(AACOnlyMixin,UpdateView):
    """
    |  Delete college: marks the :class:`~makeReports.models.report-models.College` as archived
    |  Actual deletion is not allowed due to data-loss issues

    Keyword Args:
        pk (str): primary key of college to delete
    """
    model = College
    fields = ['active']
    template_name = "makeReports/AACAdmin/CollegeDeptDP/deleteCollege.html"
    success_url = reverse_lazy('makeReports:college-list')
    def form_valid(self,form):
        """
        Processes form after submission and validation
        """
        depts = Department.objects.filter(college=self.object)
        for dept in depts:
            dept.active = False
            dept.save()
        return super(DeleteCollege,self).form_valid(form)

class RecoverCollege(AACOnlyMixin,UpdateView):
    """
    View to unarchive college
    
    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report-models.College` to recover    
    """
    model = College
    fields = ['active']
    template_name = "makeReports/AACAdmin/CollegeDeptDP/recoverCollege.html"
    success_url = reverse_lazy('makeReports:college-list')
class CollegeList(AACOnlyMixin,ListView):
    """
    To list all active :class:`~makeReports.models.report-models.College` objects
    """
    model = College
    template_name = "makeReports/AACAdmin/CollegeDeptDP/collegeList.html"
    def get_queryset(self):
        """
        Returns active colleges in a QuerySet
        """
        objs = College.active_objects.all()
        return objs
class CreateDepartment(AACOnlyMixin,CreateView):
    """
    View to create a new :class:`~makeReports.models.report-models.Department`
    """
    model = Department
    #fields = ['name', 'college']
    form_class = CreateDepartmentForm
    template_name = "makeReports/AACAdmin/CollegeDeptDP/addDepartment.html"
    success_url = "/aac/department/list/?college=&name="
class DepartmentList(AACOnlyMixin,ListView):
    """
    View that lists all active :class:`~makeReports.models.report-models.Department` objects
    """
    model = Department
    template_name = "makeReports/AACAdmin/CollegeDeptDP/deptList.html"
    def get_context_data(self, **kwargs):
        """
        Returns context to pass to template with list of :class:`~makeReports.models.report-models.College` objects

        Args:
            **kwargs (list): list of keyword arguments
        Returns:
            dict : dictionary of context
        """
        context = super(DepartmentList,self).get_context_data(**kwargs)
        context['college_list'] = College.active_objects.all()
        return context
    def get_queryset(self):
        """
        Returns QuerySet of :class:`~makeReports.models.report-models.Department` objects meeting search parameters
        """

        objs = Department.active_objects
        get = self.request.GET
        if(get["college"]!=""):
            objs=objs.filter(college__name__icontains=get["college"])
        if(get["name"]!=""):
            objs=objs.filter(name__icontains=get["name"])
        return objs.order_by('college__name')
class UpdateDepartment(AACOnlyMixin,UpdateView):
    """
    View to update the name or college of a department

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report-models.Department` to update
    """
    model = Department
    fields = ['name', 'college']
    template_name = "makeReports/AACAdmin/CollegeDeptDP/updateDepartment.html"
    success_url = "/aac/department/list/?college=&name="
class DeleteDepartment(AACOnlyMixin,UpdateView):
    """
    View to "delete" a department by marking it inactive

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report-models.Department` to delete
    """
    model = Department
    fields = ['active']
    template_name = "makeReports/AACAdmin/CollegeDeptDP/deleteDept.html"
    success_url = "/aac/department/list/?college=&name="
class RecoverDepartment(AACOnlyMixin,UpdateView):
    """
    View to recover a department by marking it active

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report-models.Department` to recover
    """
    model = Department
    fields = ['active']
    template_name = "makeReports/AACAdmin/CollegeDeptDP/recoverDept.html"
    success_url = "/aac/department/list/?college=&name="
class CreateDegreeProgram(AACOnlyMixin,CreateView):
    """
    View to create a new degree program

    Keyword Args:
        dept (str): primary key of :class:`~makeReports.models.report-models.Department` to create degree program in
    """
    model = DegreeProgram
    fields=['name','level','cycle','startingYear']
    template_name = "makeReports/AACAdmin/CollegeDeptDP/addDP.html"
    def get_form(self, form_class=None):
        """
        Returns the form to be used

        Notes:
            To the default form it changes the label of the cycle and startingYear field
        """
        form = super(CreateDegreeProgram,self).get_form()
        form.fields['cycle'].label="Number of years between automatically assigned reports (put 0 or leave blank if there is no regular cycle)"
        form.fields['startingYear'].label="The first year report is assigned for cycle (leave blank if no cycle)"
        return form
    def get_success_url(self):
        return reverse_lazy('makeReports:dp-list',args=[self.kwargs['dept']])
    def form_valid(self, form):
        """
        First sets the department passed upon pk in the kwargs, then creates the DegreeProgram model based upon the form
        """
        form.instance.department = Department.objects.get(pk=int(self.kwargs['dept']))
        return super(CreateDegreeProgram, self).form_valid(form)
class UpdateDegreeProgram(AACOnlyMixin,UpdateView):
    """
    View to update a degree program

    Keyword Args:
        dept (str): primary key of :class:`~makeReports.models.report-models.Department` of degree program
        pk (str): primary key of :class:`~makeReports.models.report-models.DegreeProgram` to update
    """
    model = DegreeProgram
    form_class = CreateDPByDept
    template_name = "makeReports/AACAdmin/CollegeDeptDP/updateDP.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:dp-list',args=[self.kwargs['dept']])
class DeleteDegreeProgram(AACOnlyMixin,UpdateView):
    """
    View to "delete" degree program by marking it inactive

    Keyword Args:
        dept (str): primary key of :class:`~makeReports.models.report-models.Department` of degree program
        pk (str): primary key of :class:`~makeReports.models.report-models.DegreeProgram` to delete
    """
    model = DegreeProgram
    fields = ['active']
    template_name = "makeReports/AACAdmin/CollegeDeptDP/deleteDP.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:dp-list',args=[self.kwargs['dept']])
class RecoverDegreeProgram(AACOnlyMixin,UpdateView):
    """
    View to recover degree program and mark it active

    Keyword Args:
        dept (str): primary key of :class:`~makeReports.models.report-models.Department` of degree program
        pk (str): primary key of :class:`~makeReports.models.report-models.DegreeProgram` to recover
    """
    model = DegreeProgram
    fields = ['active']
    template_name = "makeReports/AACAdminCollegeDeptDP//recoverDP.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:dp-list',args=[self.kwargs['dept']])
class DegreeProgramList(AACOnlyMixin,ListView):
    """
    View to list active degree programs within a department

    Keyword Args:
        dept (str): primary key of :class:`~makeReports.models.report-models.Department`
    """
    model = DegreeProgram
    template_name = "makeReports/AACAdmin/CollegeDeptDP/dpList.html"
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches the view
        Notes:
            attaches the department associated with the primary key to the instance
        """
        self.dept = Department.objects.get(pk=int(self.kwargs['dept']))
        return super(DegreeProgramList, self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        """
        Returns:
            QuerySet : contains only active :class:`~makeReports.models.report-models.DegreeProgram` objects within the department
        """
        objs = DegreeProgram.active_objects.filter(department=self.dept)
        return objs
    def get_context_data(self, **kwargs):
        """
        Returns context to be passed to template

        Returns:
            dict : context for template

        Notes:
            Adds department to context
        """
        context = super(DegreeProgramList, self).get_context_data(**kwargs)
        context['dept'] = self.dept
        return context
class ArchivedColleges(AACOnlyMixin, ListView):
    """
    View to list archived/inactive colleges
    """
    model = College
    template_name = "makeReports/AACAdmin/CollegeDeptDP/archivedColleges.html"
    def get_queryset(self):
        """
        Returns:
            QuerySet : only inactive colleges
        """
        return College.objects.filter(active=False)
class ArchivedDepartments(AACOnlyMixin, ListView):
    """
    View to list archived/inactive departments
    """
    model = Department
    template_name = "makeReports/AACAdmin/CollegeDeptDP/archivedDepartments.html"
    def get_queryset(self):
        """
        Returns:
            QuerySet : only inactive departments
        """
        return Department.objects.filter(active=False)
class ArchivedDegreePrograms(AACOnlyMixin, ListView):
    """
    View to list archived/inactive degree programs within department
    
    Keyword Args:
        dept (str): primary key of department
    """
    model = DegreeProgram
    template_name = "makeReports/AACAdmin/CollegeDeptDP/archivedDPs.html"
    def dispatch(self, request,*args, **kwargs):
        """
        Dispatches the view
        Notes:
            attaches the department to the instance
        """
        self.dept = Department.objects.get(pk=int(self.kwargs['dept']))
        return super(ArchivedDegreePrograms, self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        """
        Returns:
            QuerySet : degree programs which are inactive and in the department
        """
        return DegreeProgram.objects.filter(active=False, department=self.dept)
    def get_context_data(self, **kwargs):
        """
        Calls super and adds department to context to pass to template
        Returns:
            dict : context to pass to template
        """
        context = super(ArchivedDegreePrograms, self).get_context_data(**kwargs)
        context['dept'] = self.dept
        return context
class MakeAccount(AACOnlyMixin,FormView):
    """
    View to create an account
    """
    template_name = "makeReports/AACAdmin/create_account.html"
    form_class = MakeNewAccount
    success_url = reverse_lazy('makeReports:admin-home')
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)
class ModifyAccount(AACOnlyMixin,FormView):
    """
    View to modify an account
    
    Keyword Args:
        pk (str): primary key of user to change
    """
    form_class = UpdateUserForm
    success_url = reverse_lazy('makeReports:account-list')
    template_name = "makeReports/AACAdmin/modify_account.html"
    def dispatch(self,request, *args,**kwargs):
        """
        Dispatches view

        Notes:
            attaches user to instance
        """
        self.userToChange = Profile.objects.get(pk=self.kwargs['pk'])
        return super(ModifyAccount,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        """
        Initialize form to valus of user to update

        Returns:
            dict : initial values of fields
        """
        initial = super(ModifyAccount,self).get_initial()
        initial['aac'] = self.userToChange.aac
        initial['department'] = self.userToChange.department
        initial['first_name'] = self.userToChange.user.first_name
        initial['last_name'] = self.userToChange.user.last_name
        initial['email'] = self.userToChange.user.email
        return initial
    def form_valid(self,form):
        self.userToChange.aac = form.cleaned_data['aac']
        self.userToChange.department = form.cleaned_data['department']
        self.userToChange.user.first_name = form.cleaned_data['first_name']
        self.userToChange.user.last_name = form.cleaned_data['last_name']
        self.userToChange.user.email = form.cleaned_data['email']
        self.userToChange.save()
        self.userToChange.user.save()
        return super(ModifyAccount,self).form_valid(form)
class InactivateUser(AACOnlyMixin,UpdateView):
    """
    View to inactivate user

    Keyword Args:
        pk (str): primary key of user to inactivate
    """
    model = User
    success_url = reverse_lazy('makeReports:account-list')
    template_name = "makeReports/AACAdmin/inactivate_account.html"
    fields = ['is_active']
class AccountList(AACOnlyMixin,ListView):
    """
    View to list accounts
    """
    model = Profile
    template_name = 'makeReports/AACAdmin/account_list.html'
    def get_queryset(self):
        return Profile.objects.filter(user__is_active=True)
class SearchAccountList(AACOnlyMixin,ListView):
    """
    View to search list of accounts

    Notes:
        Through request url, search parameters are passed through f for the
        first name, l for the last name, and e for email
    """
    model = Profile
    template_name = 'makeReports/AACAdmin/account_list.html'
    def get_queryset(self):
        """
        Filters the queryset based upon the search parameters

        Returns:
        QuerySet : queryset matching search with only active users
        """
        profs = Profile.objects.filter(user__is_active=True)
        if self.request.GET['f']!="":
            profs = profs.filter(user__first_name__icontains=self.request.GET['f'])
        if self.request.GET['l']!="":
            profs = profs.filter(user__last_name__icontains=self.request.GET['l'])
        if self.request.GET['e']!="":
            profs = profs.filter(user__email__icontains=self.request.GET['e'])
        return profs
class MakeAnnouncement(AACOnlyMixin,CreateView):
    """
    View to make announcement
    """
    template_name = "makeReports/AACAdmin/Announcements/addAnnoun.html"
    success_url = reverse_lazy('makeReports:announ-list')
    form_class = AnnouncementForm
class ModifyAnnouncement(AACOnlyMixin,UpdateView):
    """
    View to modify announcement

    Keyword Args:
        pk (str): primary key of annoucement to update
    """
    model = Announcement
    template_name = "makeReports/AACAdmin/Announcements/editAnnoun.html"
    success_url = reverse_lazy('makeReports:announ-list')
    form_class = AnnouncementForm
class ListAnnouncements(AACOnlyMixin,ListView):
    """
    View to list not-expired announcements
    """
    model = Announcement
    template_name = "makeReports/AACAdmin/Announcements/annList.html"
    def get_queryset(self):
        """
        Get not-expired announcements

        Returns:
            QuerySet : announcments that are not expired
        """
        return Announcement.objects.filter(expiration__gte=datetime.now()).order_by("-creation")
class DeleteAnnouncement(AACOnlyMixin,DeleteView):
    """
    View to delete announcement

    Keyword Args:
        pk (str): primary key of announcement to delete
    """
    model = Announcement
    template_name = "makeReports/AACAdmin/Announcements/deleteAnn.html"
    success_url = reverse_lazy('makeReports:announ-list')

