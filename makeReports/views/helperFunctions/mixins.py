from makeReports.models import *
from makeReports.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class AACOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    """
    Only allows AAC members to access page
    """
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeptOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    """
    Only allow people who are in the department of the report access page

    Notes:
        Assumes URL has report attribute
    """
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeptAACMixin(LoginRequiredMixin,UserPassesTestMixin):
    """
    Allows people within the department or the AAC to access page

    Notes:
        Assumes URL has report attribute
    """
    def test_func(self):
        dept = (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
class DeptReportMixin(DeptOnlyMixin):
    """
    Attaches the report matching to the instance and puts it in the context

    Keyword Args:
        report (str): primary key of report
    """
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeptReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rpt'] = self.report
        return context
class AACReportMixin(AACOnlyMixin):
    """
    Attaches report matching to the instance and puts it in the context

    Keyword Args:
        report (str): primary key of report
    """
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AACReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rpt'] = self.report
        return context