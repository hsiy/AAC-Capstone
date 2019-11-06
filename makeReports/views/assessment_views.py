"""
This file contains all views related to inputting assessments into the form
"""
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *

class AssessmentSummary(DeptReportMixin,ListView):
    """
    View to summarize state of assessment section of form
    """
    model = AssessmentVersion
    template_name = "makeReports/Assessment/assessmentSummary.html"
    context_object_name = "assessment_list"
    def get_queryset(self):
        """
        Returns assessments in report ordered by SLO

        Returns:
            QuerySet : :class:`~makeReports.models.report_models.AssessmentVersion` objects in report
        """
        report = self.report
        objs = AssessmentVersion.objects.filter(report=report).order_by("slo__number","number")
        return objs
    def get_context_data(self, **kwargs):
        """
        Gets context for template

        Notes:
            calls section2Context to retrieve context needed
        Returns:
            dict : context for template
        """
        context = super(AssessmentSummary, self).get_context_data()
        return section2Context(self,context)
class AddNewAssessment(DeptReportMixin,FormView):
    """
    View to add a new assessment
    """
    template_name = "makeReports/Assessment/addAssessment.html"
    form_class = CreateNewAssessment
    def get_form_kwargs(self):
        """
        Gets keyword arguments for form, only allowing for SLOs in report
        
        Returns:
            dict : keyword arguments for form
        """
        kwargs = super(AddNewAssessment,self).get_form_kwargs()
        kwargs['sloQS'] = SLOInReport.objects.filter(report=self.report).order_by("number")
        return kwargs
    def get_success_url(self):
        """
        Gets assessment summary url (assessment summary)

        Returns:
            str : success url of success page (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self, form):
        """
        |  Creates :class:`~makeReports.models.report_models.Assessment` and :class:`~makeReports.models.report_models.AssessmentVersion` based upon form
        |  Updates the numberOfAssess fields for :class:`~makeReports.models.report_models.SLO`

        Args:
            form (CreateNewAssessment): completed form to be processed
            
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        rpt = self.report
        num = form.cleaned_data['slo'].numberOfAssess
        num += 1
        form.cleaned_data['slo'].numberOfAssess = num
        form.cleaned_data['slo'].save()
        assessObj = Assessment.objects.create(
            title=form.cleaned_data['title'], 
            domainExamination=False, 
            domainProduct=False, 
            domainPerformance=False, 
            directMeasure =form.cleaned_data['directMeasure'])
        assessRpt = AssessmentVersion.objects.create(
            date=datetime.now(), 
            number = num, 
            assessment=assessObj, 
            description=form.cleaned_data['description'], 
            finalTerm=form.cleaned_data['finalTerm'], 
            where=form.cleaned_data['where'], 
            allStudents=form.cleaned_data['allStudents'], 
            sampleDescription=form.cleaned_data['sampleDescription'], 
            frequency=form.cleaned_data['frequency'], 
            frequencyChoice = form.cleaned_data['frequencyChoice'],
            threshold=form.cleaned_data['threshold'], 
            target=form.cleaned_data['target'],
            slo=form.cleaned_data['slo'],
            report=rpt, 
            changedFromPrior=False)
        dom = form.cleaned_data['domain']
        if ("Pe" in dom):
            assessObj.domainPerformance = True
        if ("Pr" in dom):
            assessObj.domainProduct = True
        if ("Ex" in dom):
            assessObj.domainExamination = True
        assessObj.save()
        assessRpt.save()
        return super(AddNewAssessment, self).form_valid(form)
class AddNewAssessmentSLO(AddNewAssessment):
    """
    View to add new assessment from the SLO page
    
    Keyword Args:
        slo (str): primary key of :class:`~makeReports.models.report_models.SLO` to add assessment
    """
    def get_initial(self):
        """
        Initializes slo of form to that of the page this view was navigated from

        Returns:
            dict : initial form values
        """
        initial = super(AddNewAssessmentSLO,self).get_initial()
        initial['slo'] = SLOInReport.objects.get(pk=self.kwargs['slo'])
        return initial
    def get_success_url(self):
        """
        Gets URL to go to upon success (SLO summary)

        Returns:
            str : URL of SLO summary page (:class:`~makeReports.views.slo_views.SLOSummary`)
        """
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class ImportAssessment(DeptReportMixin,FormView):
    """
    View to import assessment from within the department

    Notes:
        Through get request URL, the following search parameters are sent:
        'yearIn','dP': primary key of degree program, 'slo': primary key of SLO (:class:`~makeReports.models.report_models.SLOInReport`)
    """
    template_name = "makeReports/Assessment/importAssessment.html"
    form_class = ImportAssessmentForm
    def get_success_url(self):
        """
        Gets URL to go to upon success (assessment summary)

        Returns:
            str : URL of assessment summary page (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def get_form_kwargs(self):
        """
        Get keyword arguments of form, by filtering the assessment choices by search parameters,
        and SLO choices by the report

        Returns:
            dict : keyword arguments of the form
        """
        kwargs = super(ImportAssessment,self).get_form_kwargs()
        yearIn = self.request.GET['year']
        dP = self.request.GET['dp']
        aCs = AssessmentVersion.objects
        if yearIn!="":
            aCs=aCs.filter(report__year=yearIn)
        if dP!="" and dP!="-1":
            try:
                aCs=aCs.filter(report__degreeProgram=DegreeProgram.objects.get(pk=dP))
            except:
                pass
        if self.request.GET['slo']!="" and self.request.GET['slo']!="-1":
            aCs=aCs.filter(slo=SLOInReport.objects.get(pk=self.request.GET['slo']))
        aCsInRpt = AssessmentVersion.objects.filter(report=self.report).order_by("slo__number","number")
        #for a in aCsInRpt:
        #    aCs=aCs.exclude(assessment=a.assessment)
        kwargs['assessChoices'] = aCs
        kwargs['slos'] = SLOInReport.objects.filter(report=self.report).order_by("number")
        return kwargs
    def form_valid(self,form):
        """
        |  Creates :class:`~makeReports.models.report_models.AssessmentVersion` from form
        |  Also updates the numberOfAssess field of corresponding :class:`~makeReports.models.report_models.SLOInReport`
        |  Updates the numberOfUses field of corresponding :class:`~makeReports.models.report_models.Assessment`
        
        Args:
            form (ImportAssessmentForm): completed form to be processed
            
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        
        """
        rpt = self.report
        slo = form.cleaned_data['slo']
        num = slo.numberOfAssess
        for assessVers in form.cleaned_data['assessment']:
            num += 1
            AssessmentVersion.objects.create(
                slo=slo,
                number=num,
                date=datetime.now(), 
                description=assessVers.description,
                assessment=assessVers.assessment, 
                report=rpt, 
                changedFromPrior=False, 
                finalTerm=assessVers.finalTerm, 
                where=assessVers.where, 
                allStudents=assessVers.allStudents, 
                sampleDescription=assessVers.sampleDescription, 
                frequencyChoice = assessVers.frequencyChoice,
                frequency=assessVers.frequency, 
                threshold=assessVers.threshold, 
                target=assessVers.target)
            assessVers.assessment.numberOfUses += 1
            assessVers.assessment.save()
        slo.numberOfAssess = num
        slo.save()
        return super(ImportAssessment,self).form_valid(form)
    def get_context_data(self, **kwargs):
        """
        Gets context for template, with the current degree program, all degree programs within the department, and SLOs within department

        Returns:
            dict : context for template

        Notes:
            Arranges SLOs by first those which appear within this report, and then all others
        """
        context = super(ImportAssessment, self).get_context_data(**kwargs)
        r = self.report
        context['currentDPpk'] = r.degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=r.degreeProgram.department)
        context['slo_list'] = SLOInReport.objects.filter(report=r).order_by("number").union(SLOInReport.objects.filter(report__degreeProgram__department=r.degreeProgram.department).exclude(report=r).order_by("number"),all=True)
        return context
class ImportAssessmentSLO(ImportAssessment):
    """
    Imports assessment for a specific SLO
    
    Keyword Args:
        slo (str) : primary key of :class:`~makeReports.models.report_models.SLOInReport`
    """
    template_name = "makeReports/Assessment/importAssessmentSLO.html"
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches the view, and attaches the specific :class:`~makeReports.models.report_models.SLOInReport` to the instance

        Args:
            request (HttpRequest): request to view page
        Keyword Args:
            slo (str) : primary key of :class:`~makeReports.models.report_models.SLOInReport`
            
        Returns:
            HttpResponse : response of page to request
        """
        self.slo = SLOInReport.objects.get(pk=self.kwargs['slo'])
        return super(ImportAssessmentSLO,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        """
        Gets URL to go to upon success (SLO summary)

        Returns:
            str : URL of SLO summary page (:class:`~makeReports.views.slo_views.SLOSummary`)
        """
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def get_initial(self):
        """
        Initializes the form, sets the SLO appropriately

        Returns:
            dict : initial form values
        """
        initial = super(ImportAssessmentSLO,self).get_initial()
        initial['slo'] = self.slo
        return initial
    def get_context_data(self, **kwargs):
        """
        Gets context for the template, and attaches the :class:`~makeReports.models.report_models.SLOInReport` to the context

        Returns:
            dict : context for template
        """
        context = super(ImportAssessmentSLO, self).get_context_data(**kwargs)
        context['slo'] = self.slo
        return context
class EditImportedAssessment(DeptReportMixin,FormView):
    """
    View to edit imported assessment (cannot change fields in :class:`~makeReports.models.report_models.Assessment`)
    
    Keyword Args:
        assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` to update
    """
    template_name = "makeReports/Assessment/editImportedAssessment.html"
    form_class = EditImportedAssessmentForm
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view, and attaches :class:`~makeReports.models.report_models.AssessmentVersion` to instance

        Args:
            request (HttpRequest): request to view page
        
        Keyword Args:
            assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` to update
        
        Returns:
            HttpResponse : response of page to request
        """
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(EditImportedAssessment,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        """
        Gets initial form values based upon the current values of the :class:`~makeReports.models.report_models.AssessmentVersion`
        
        Returns:
            dict : initial form values
        """
        initial = super(EditImportedAssessment, self).get_initial()
        initial['description'] = self.assessVers.description
        initial['finalTerm'] = self.assessVers.finalTerm
        initial['where'] = self.assessVers.where
        initial['allStudents'] = self.assessVers.allStudents
        initial['sampleDescription'] = self.assessVers.sampleDescription
        initial['frequencyChoice'] = self.assessVers.frequencyChoice
        initial['frequency'] = self.assessVers.frequency
        initial['threshold'] = self.assessVers.threshold
        initial['target'] = self.assessVers.target
        initial['slo'] = self.assessVers.slo
        return initial
    def get_form_kwargs(self):
        """
        Gets form keywords, settings SLO options to those within the report

        Returns:
            dict : form keyword arguments
        """
        kwargs = super(EditImportedAssessment,self).get_form_kwargs()
        kwargs['sloQS'] = SLOInReport.objects.filter(report=self.report).order_by("number")
        return kwargs
    def get_success_url(self):
        """
        Gets URL to go to upon success (assessment summary)

        Returns:
            str : URL of assessment summary page (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self,form):
        """
        Edits imported assessment based upon form

        Args:
            form (EditImportedAssessmentForm): completed form to be processed
            
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        self.assessVers.description = form.cleaned_data['description']
        self.assessVers.date = datetime.now()
        self.assessVers.finalTerm = form.cleaned_data['finalTerm']
        self.assessVers.where = form.cleaned_data['where']
        self.assessVers.allStudents = form.cleaned_data['allStudents']
        self.assessVers.sampleDescription = form.cleaned_data['sampleDescription']
        self.assessVers.frequencyChoice = form.clenaed_data['frequencyChoice']
        self.assessVers.frequency = form.cleaned_data['frequency']
        self.assessVers.threshold = form.cleaned_data['threshold']
        self.assessVers.target = form.cleaned_data['target']
        self.assessVers.slo = form.cleaned_data['slo']
        self.assessVers.save()
        self.assessVers.assessment.save()
        return super(EditImportedAssessment, self).form_valid(form)
class EditNewAssessment(DeptReportMixin,FormView):
    """
    View to edit new assessments (can change fields in :class:`~makeReports.models.report_models.Assessment`)
    
    Keyword Args:
        assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` to edit
    """
    template_name = "makeReports/Assessment/editNewAssessment.html"
    form_class = EditNewAssessmentForm
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatch view and attach assessment to instance

        Args:
            request (HttpRequest): request to view page
        Keyword Args:
            assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` to edit
        
        Returns:
            HttpResponse : response of page to request
        """
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(EditNewAssessment,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        """
        Get initial values of form based upon current values of the assessment

        Returns:
            dict : initial values of form
        """
        initial = super(EditNewAssessment, self).get_initial()
        initial['title'] = self.assessVers.assessment.title
        initial['domainPerformance'] = self.assessVers.assessment.domainPerformance
        initial['domainProduct'] = self.assessVers.assessment.domainProduct
        initial['domainExamination'] = self.assessVers.assessment.domainExamination
        initial['directMeasure'] = self.assessVers.assessment.directMeasure
        initial['description'] = self.assessVers.description
        initial['finalTerm'] = self.assessVers.finalTerm
        initial['where'] = self.assessVers.where
        initial['allStudents'] = self.assessVers.allStudents
        initial['sampleDescription'] = self.assessVers.sampleDescription
        initial['frequencyChoice'] = self.assessVers.frequencyChoice
        initial['frequency'] = self.assessVers.frequency
        initial['threshold'] = self.assessVers.threshold
        initial['target'] = self.assessVers.target
        initial['slo'] = self.assessVers.slo
        return initial
    def get_form_kwargs(self):
        """
        Return form keywords, setting SLO options to those within the report

        Returns:
            dict : form keyword arguments
        """
        kwargs = super(EditNewAssessment,self).get_form_kwargs()
        kwargs['sloQS'] = SLOInReport.objects.filter(report=self.report).order_by("number")
        return kwargs
    def get_success_url(self):
        """
        Gets URL to go to upon success (assessment summary)

        Returns:
            str : URL of assessment summary page (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self, form):
        """
        Edit assessment according to form

        Args:
            form (EditNewAssessmentForm) : form to be processed
                
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        self.assessVers.description = form.cleaned_data['description']
        self.assessVers.date = datetime.now()
        self.assessVers.assessment.title = form.cleaned_data['title']
        self.assessVers.assessment.domain = form.cleaned_data['domain']
        self.assessVers.assessment.directMeasure = form.cleaned_data['directMeasure']
        self.assessVers.finalTerm = form.cleaned_data['finalTerm']
        self.assessVers.where = form.cleaned_data['where']
        self.assessVers.allStudents = form.cleaned_data['allStudents']
        self.assessVers.sampleDescription = form.cleaned_data['sampleDescription']
        self.assessVers.frequencyChoice = form.cleaned_data['frequencyChoice']
        self.assessVers.frequency = form.cleaned_data['frequency']
        self.assessVers.threshold = form.cleaned_data['threshold']
        self.assessVers.target = form.cleaned_data['target']
        self.assessVers.slo = form.cleaned_data['slo']
        self.assessVers.save()
        self.assessVers.assessment.save()
        return super(EditNewAssessment,self).form_valid(form)
class SupplementUpload(DeptReportMixin,CreateView):
    """
    View to upload supplements to assessments

    Keyword Args:
        assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion`
    """
    template_name = "makeReports/Assessment/supplementUpload.html"
    model = AssessmentSupplement
    fields = ['supplement']
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatch view and attach assessment to instance

        Args:
            request (HttpRequest): request to view page
        
        Keyword Args:
            assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion`
            
        Returns:
            HttpResponse : response of page to request
        """
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(SupplementUpload,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        """
        Gets success URL and used as hook to add supplement to assessment

        Returns:
            str : URL of assessment summary (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        self.assessVers.supplements.add(self.object)
        self.assessVers.save()
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self,form):
        """
        Sets the assessment version and datetime, then 
        creates supplement to assessment based upon form

        Args:
            form (ModelForm): completed form to process
            
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        form.instance.assessmentVersion = self.assessVers
        form.instance.uploaded_at = datetime.now()
        return super(SupplementUpload,self).form_valid(form)
class ImportSupplement(DeptReportMixin,FormView):
    """
    View to import supplement to assessment
    
    Keyword Args:
        assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion`
    
    Notes:
        Year and degree program to search for assessment passed via get request under
        'year' and 'dp' respectively
    """
    template_name = "makeReports/Assessment/importSupplement.html"
    form_class = ImportSupplementsForm
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view and attaches :class:`~makeReports.models.report_models.AssessmentVersion` to instance

        Args:
            request (HttpRequest): request to view page
            
        Keyword Args:
            assessIR (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion`
        
        Returns:
            HttpResponse : response of page to request
        """
        self.assessVers = AssessmentVersion.objects.get(pk=self.kwargs['assessIR'])
        return super(ImportSupplement,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        """
        Gets URL to go to upon success (assessment summary)

        Returns:
            str : URL of assessment summary page (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def get_form_kwargs(self):
        """
        Gets form keyword arguments, set the supplement choices based upon search parameters

        Returns:
            dict : form keyword arguments
        """
        kwargs = super(ImportSupplement,self).get_form_kwargs()
        yearIn = self.request.GET['year']
        dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
        kwargs['supChoices'] = AssessmentSupplement.objects.filter(
            assessmentversion__report__year=yearIn, assessmentversion__report__degreeProgram=dPobj)
        return kwargs
    def form_valid(self,form):
        """
        Imports supplement to another assessment based upon form

        Args:
            form (ImportSupplementForm): completed form to be processed
            
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        self.assessVers.supplements.add(form.cleaned_data['sup'])
        self.assessVers.save()
        return super(ImportSupplement,self).form_valid(form)
    def get_context_data(self, **kwargs):
        """
        Gets context for template, passing the assessment, the current degree program, and degree programs within
        the department

        Returns:
            dict : context for template
        """
        context = super(ImportSupplement, self).get_context_data(**kwargs)
        context["aIR"] = self.kwargs['assessIR']
        context['currentDPpk'] = self.report.degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=self.report.degreeProgram.department)
        return context
class DeleteSupplement(DeptReportMixin,DeleteView):
    """
    View to delete supplement

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report_models.AssessmentSupplement` to delete
    """
    model = AssessmentSupplement
    template_name = "makeReports/Assessment/deleteSupplement.html"
    def get_success_url(self):
        """
        Gets URL to go to upon success (assessment summary)

        Returns:
            str : URL of assessment summary page (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
class Section2Comment(DeptReportMixin,FormView):
    """
    View to add a comment for the second section of the form
    """
    template_name = "makeReports/Assessment/assessmentComment.html"
    form_class = Single2000Textbox
    def get_success_url(self):
        """
        Gets URL to go to upon success (assessment summary)

        Returns:
            str : URL of assessment summary page (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self, form):
        """
        Sets the section 2 comment from the form

        Args:
            form (Single2000Textbox): completed form to be processed
            
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        self.report.section2Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section2Comment,self).form_valid(form)
    def get_initial(self):
        """
        Gets initial value for form based upon current comment value

        Returns:
            dict : initial form values
        """
        initial = super(Section2Comment,self).get_initial()
        initial['text']="No comment."
        if self.report.section2Comment:
            initial['text'] = self.report.section2Comment
        return initial
class DeleteImportedAssessment(DeptReportMixin,DeleteView):
    """
    View to delete imported assessments (more restricted than new assessments)

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` to "delete"
    """
    model = AssessmentVersion
    template_name = "makeReports/Assessment/deleteAssessment.html"
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches the view, and attaches the :class:`~makeReports.models.report_models.AssessmentVersion`, 
        the :class:`~makeReports.models.report_models.SLOInReport`, and the number of the assessments to the instance
        
        Args:
            request (HttpRequest): request to view page
            
        Keyword Args:
            pk (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` to "delete"
            
        Returns:
            HttpResponse : response of page to request
        """
        a = AssessmentVersion.objects.get(pk=self.kwargs['pk'])
        self.oldNum = a.number
        self.slo = a.slo
        self.assessment = a.assessment
        return super(DeleteImportedAssessment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        """
        Gets success url (assessment summary) and uses it has a hook to update the number of other assessments and 
        update corresponding :class:`~makeReports.models.report_models.Assessment` and
        :class:`~makeReports.models.report_models.SLOInReport`

        Returns:
            str : URL of assessment summary (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        oldNum = self.oldNum
        assess = AssessmentVersion.objects.filter(report=self.report).order_by("slo__number","number")
        for a in assess:
            if a.number > oldNum:
                a.number -= 1
                a.save()
        if self.assessment.numberOfUses <= 1:
            self.assessment.delete()
            self.assessment.save()
        else:
            self.assessment.numberOfUses -= 1
            self.assessment.save()
        self.slo.numberOfAssess -= 1
        self.slo.save()
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
class DeleteNewAssessment(DeptReportMixin,DeleteView):
    """
    View to delete new assessment

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` delete
    """
    model = AssessmentVersion
    template_name = "makeReports/Assessment/deleteAssessment.html"
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view, and attaches :class:`~makeReports.models.report_models.AssessmentVersion` to the instance

        Args:
            request (HttpRequest): request to view page
            
        Keyword Args:
            pk (str): primary key of :class:`~makeReports.models.report_models.AssessmentVersion` delete
            
        Returns:
            HttpResponse : response of page to request
        """
        a = AssessmentVersion.objects.get(pk=self.kwargs['pk'])
        self.oldNum = a.number
        self.slo = a.slo
        return super(DeleteNewAssessment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        """
        Gets success url (assessment summary page), and uses as hook to update corresponding
        :class:`~makeReports.models.report_models.Assessment` and 
        :class:`~makeReports.models.report_models.SLOInReport`

        Returns:
            str : assessment summary URL (:class:`~makeReports.views.assessment_views.AssessmentSummary`)
        """
        ASSESSIR = AssessmentVersion.objects.get(pk=self.kwargs['pk'])
        assessment = ASSESSIR.assessment
        if assessment.numberOfUses <= 1:
            assessment.delete()
            assessment.save()
        else:
            assessment.numberOfUses -= 1
            assessment.save()
        oldNum = self.oldNum
        assess = AssessmentVersion.objects.filter(report=self.report).order_by("slo__number","number")
        for a in assess:
            if a.number > oldNum:
                a.number -= 1
                a.save()
        self.slo.numberOfAssess -= 1
        self.slo.save()        
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])