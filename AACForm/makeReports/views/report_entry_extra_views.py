from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *
"""
This file contains extra views needed during the form input process
"""
class ReportFirstPage(DeptOnlyMixin,UpdateView):
    """
    View to set report wide attributes
    """
    model = Report
    fields = ['author','date_range_of_reported_data']
    template_name = "makeReports/ReportEntryExtras/first_page.html"
    labels = {
        'author':'Person preparing the report'
    }
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatch the view and attach the report to the instance

        Args:
            request (HttpRequest): request to view page
            
        Returns:
            HttpResponse : response of page to request
        """
        self.report = Report.objects.get(pk=self.kwargs['pk'])
        return super(ReportFirstPage,self).dispatch(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        """
        Gets the context for the template, including the report

        Returns:
            dict : context for template
        """
        context = super(ReportFirstPage,self).get_context_data(**kwargs)
        context['rpt'] = self.report
        return context
    def get_success_url(self):
        """
        Gets URL to go to upon success (SLO summary)

        Returns:
            str : URL of SLO summary page (:class:`~makeReports.views.slo_views.SLOSummary`)
        """
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class FinalReportSupplements(DeptReportMixin, ListView):
    """
    View to list report supplements while entering them
    """
    model = ReportSupplement
    template_name = "makeReports/ReportEntryExtras/supplementList.html"
    def get_context_data(self, **kwargs):
        """
        Gets the context for the template, including the report

        Returns:
            dict : context for template
        """
        context = super(FinalReportSupplements,self).get_context_data(**kwargs)
        context['report'] = self.report
        return context
    def get_queryset(self):
        return ReportSupplement.objects.filter(report=self.report)
class AddEndSupplements(DeptReportMixin, CreateView):
    """
    View to add report supplement
    """
    model = ReportSupplement
    template_name = "makeReports/ReportEntryExtras/addSupplement.html"
    fields = ['supplement']
    def get_context_data(self, **kwargs):
        """
        Gets the context for the template, including the report

        Returns:
            dict : context for template
        """
        context = super(AddEndSupplements,self).get_context_data(**kwargs)
        context['report'] = self.report
        return context
    def form_valid(self,form):
        """
        Sets the report then creates the report supplement from the form

        Args:
            form (ModelForm): filled out form to process
                
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        form.instance.report = self.report
        return super(AddEndSupplements,self).form_valid(form)
    def get_success_url(self):
        """
        Gets URL to go to upon success (report supplement summary)

        Returns:
            str : URL of report supplement list page (:class:`~makeReports.views.report_entry_extra_views.FinalReportSupplements`)
        """
        return reverse_lazy('makeReports:rpt-sup-list', args=[self.report.pk])
class DeleteEndSupplements(DeptReportMixin, DeleteView):
    """
    Delete a report supplement

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report_models.ReportSupplement` to be deleted
    """
    model = ReportSupplement
    template_name = "makeReports/ReportEntryExtras/deleteSupplement.html"
    def get_context_data(self,**kwargs):
        """
        Gets the context for the template, including the report

        Returns:
            dict : context for template
        """
        context = super(DeleteEndSupplements,self).get_context_data(**kwargs)
        context['report'] = self.report
        return context
    def get_success_url(self):
        """
        Gets URL to go to upon success (report supplement summary)

        Returns:
            str : URL of report supplement list page (:class:`~makeReports.views.report_entry_extra_views.FinalReportSupplements`)
        """
        return reverse_lazy('makeReports:rpt-sup-list', args=[self.report.pk])
class SubmitReport(DeptReportMixin, FormView):
    """
    View to review and submit form
    """
    form_class = SubmitReportForm
    template_name = "makeReports/ReportEntryExtras/submit.html"
    success_url = reverse_lazy('makeReports:sub-suc')
    def get_form_kwargs(self):
        """
        Get keyword arguments for the form, including whether the report is compelete and error message

        Returns:
            dict : keyword arguments
        """
        kwargs=super(SubmitReport,self).get_form_kwargs()
        slos = SLOInReport.objects.filter(report=self.report)
        valid = True
        eMsg = "The report is not complete.\n"
        if slos.count() == 0 :
            valid = False
            eMsg = eMsg+"There are no SLOs.\n"
        for slo in slos:
            if slo.numberOfAssess==0:
                valid = False
                eMsg = eMsg+"There is not an assessment for SLO "+str(slo.number)+".\n"
            if DecisionsActions.objects.filter(report=self.report, SLO=slo.slo).count()==0:
                valid = False
                eMsg = eMsg+"There are no decisions or actions for SLO "+str(slo.number)+".\n"
        assesses = AssessmentVersion.objects.filter(report=self.report)
        for a in assesses:
            if AssessmentData.objects.filter(assessmentVersion=a).count()==0:
                valid = False
                eMsg = eMsg+"There is no data for assessment "+str(a.number)+".\n"
            if AssessmentAggregate.objects.filter(assessmentVersion=a).count()==0:
                valid = False
                eMsg = eMsg+"There is no aggregate number for assessment "+str(a.number)+".\n"
        if not self.report.author or self.report.author=="":
            valid = False
            eMsg = eMsg+"There is no report author.\n"
        if not self.report.date_range_of_reported_data or self.report.date_range_of_reported_data=="":
            valid = False
            eMsg = eMsg+"There is no reported data range.\n"
        if SLOsToStakeholder.objects.filter(report=self.report).count() == 0:
            valid == False
            eMsg = eMsg+"There is no description of sharing SLOs with stakeholders.\n"
        if ResultCommunicate.objects.filter(report=self.report).count() == 0:
            valid = False
            eMsg = eMsg+"There is no description of communicating results.\n"
        kwargs['valid'] = valid
        kwargs['eMsg'] = eMsg
        return kwargs
    def get_context_data(self, **kwargs):
        """
        Gets the context for the template, including the report, and context needed for all report sections

        Returns:
            dict : context for template
        """
        context = super(SubmitReport,self).get_context_data(**kwargs)
        context['report'] = self.report
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
    def form_valid(self,form):
        """
        After the form is validated, set the report to submitted

        Args:
            form (SubmitReportForm): filled out form to process
                
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        self.report.submitted = True
        self.report.save()
        return super(SubmitReport,self).form_valid(form)
class SuccessSubmit(TemplateView):
    """
    View to show after successfully submitting report
    """
    template_name = "makeReports/ReportEntryExtras/success.html"