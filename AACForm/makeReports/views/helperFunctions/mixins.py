from makeReports.models import *
from makeReports.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class AACOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeptOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeptAACMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        dept = (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
class DeptReportMixin(DeptOnlyMixin):
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeptReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rpt'] = self.report
        return context
class AACReportMixin(AACOnlyMixin):
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AACReportMixin,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rpt'] = self.report
        return context