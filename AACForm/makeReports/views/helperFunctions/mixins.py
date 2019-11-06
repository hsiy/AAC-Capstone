from makeReports.models import *
from makeReports.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class AACOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    """
    Only allows AAC members to access page
    """
    def test_func(self):
        """
        Tests is user is part of the AAC

        Returns:
            bool : if is member of AAC
        """
        return getattr(self.request.user.profile, "aac")
class DeptOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    """
    Only allow people who are in the department of the report access page

    Notes:
        Assumes URL has report attribute
    """
    def test_func(self):
        """
        Tests if user is in the department

        Returns:
            bool : if is in department
        """
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeptAACMixin(LoginRequiredMixin,UserPassesTestMixin):
    """
    Allows people within the department or the AAC to access page

    Notes:
        Assumes URL has report attribute
    """
    def test_func(self):
        """
        Tests if the user is in the AAC or is in the department

        Returns:
            bool : if is in AAC or in department
        """
        dept = (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
class DeptReportMixin(DeptOnlyMixin):
    """
    Attaches the :class:`~makeReports.models.report_models.Report` matching to the instance and puts it in the context

    Keyword Args:
        report (str): primary key of :class:`~makeReports.models.report_models.Report`
    """
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view and attaches :class:`~makeReports.models.report_models.Report` to the instance

        Args:
            request (HttpRequest): request for the page
        Keyword Args:
            report (str): primary key of :class:`~makeReports.models.report_models.Report`
        Returns:
            HttpResponse : response with page to request
        """
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeptReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        """
        Gets context needed for template, including the report

        Returns:
            dict : context for template
        """
        context = super().get_context_data()
        context['rpt'] = self.report
        return context
class AACReportMixin(AACOnlyMixin):
    """
    Attaches :class:`~makeReports.models.report_models.Report` matching to the instance and puts it in the context

    Keyword Args:
        report (str): primary key of :class:`~makeReports.models.report_models.Report`
    """
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view and attaches :class:`~makeReports.models.report_models.Report` to the instance

        Args:
            request (HttpRequest): request for the page
        Keyword Args:
            report (str): primary key of :class:`~makeReports.models.report_models.Report`
        Returns:
            HttpResponse : response with page to request
        """
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AACReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        """
        Gets context needed for template, including the report

        Returns:
            dict : context for template
        """
        context = super().get_context_data()
        context['rpt'] = self.report
        return context