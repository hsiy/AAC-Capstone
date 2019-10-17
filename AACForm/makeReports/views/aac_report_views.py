from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from makeReports.views.helperFunctions.mixins import *

class CreateReport(AACOnlyMixin,CreateView):
    model = Report
    form_class = CreateReportByDept
    template_name = "makeReports/AACAdmin/manualReportCreate.html"
    #success_url = reverse_lazy('makeReports:admin-home')
    def get_form_kwargs(self):
        kwargs = super(CreateReport, self).get_form_kwargs()
        kwargs['dept'] = self.kwargs['dept']
        return kwargs
    def get_success_url(self):
        self.object.rubric = self.GR
        self.object.save()
        return reverse_lazy('makeReports:admin-home')
    def form_valid(self, form):
        form.instance.submitted = False
        self.GR = GradedRubric.objects.create(rubricVersion=form.cleaned_data['rubric'])
        return super(CreateReport, self).form_valid(form)
class DeleteReport(AACOnlyMixin,DeleteView):
    model = Report
    template_name = "makeReports/AACAdmin/deleteReport.html"
    success_url = reverse_lazy('makeReports:admin-home')
class ReportList(AACOnlyMixin,ListView):
    model = Report
    template_name = "makeReports/AACAdmin/reportList.html"
    def get_queryset(self):
        qs = Report.objects.filter(year=int(datetime.now().year), degreeProgram__active=True).order_by('submitted','-rubric__complete')
        return qs
class ReportListSearched(AACOnlyMixin,ListView):
    model = Report
    template_name = "makeReports/AACAdmin/reportList.html"
    def get_queryset(self):
        year = self.request.GET['year']
        submitted = self.request.GET['submitted']
        x=self.request.GET
        graded = self.request.GET['graded']
        dP = self.request.GET['dP']
        dept = self.request.GET['dept']
        college = self.request.GET['college']
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
class ManualReportSubmit(AACOnlyMixin,UpdateView):
    model = Report
    fields = ['submitted']
    template_name = 'makeReports/AACAdmin/manualSubmit.html'
    success_url = reverse_lazy('makeReports:report-list')
class MakeGradGoal(AACOnlyMixin,CreateView):
    model = GradGoal
    fields = ['text']
    template_name = "makeReports/AACAdmin/GG/addGG.html"
    success_url = reverse_lazy('makeReports:gg-list')
    def get_form(self, form_class=None):
        form = super(MakeGradGoal,self).get_form(form_class)
        form.fields['text'].widget = SummernoteWidget()
        form.fields['text'].label = "Goal text:"
        return form
class UpdateGradGoal(AACOnlyMixin,UpdateView):
    model = GradGoal
    fields = ['text','active']
    template_name = "makeReports/AACAdmin/GG/updateGG.html"
    success_url = reverse_lazy('makeReports:gg-list')
    def get_form(self, form_class=None):
        form = super(UpdateGradGoal,self).get_form(form_class)
        form.fields['text'].widget = SummernoteWidget()
        form.fields['text'].label = "Goal text:"
        return form
class ListActiveGradGoals(AACOnlyMixin,ListView):
    model = GradGoal
    template_name = "makeReports/AACAdmin/GG/GGlist.html"
    def get_queryset(self):
        return GradGoal.active_objects.all()
class ListInactiveGradGoals(AACOnlyMixin,ListView):
    model = GradGoal
    template_name = "makeReports/AACAdmin/GG/oldGGlist.html"
    def get_queryset(self):
        return GradGoal.objects.filter(active=False)