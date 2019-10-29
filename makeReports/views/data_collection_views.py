from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *
from makeReports.choices import *

class DataCollectionSummary(DeptReportMixin,ListView):
    """
    View to summarize data collection of in-progress form
    """
    model = AssessmentData
    template_name = 'makeReports/DataCollection/dataCollectionSummary.html'
    context_object_name = "data_collection_dict"
    def get_queryset(self):
        """
        Gets QuerySet of data objects that go with the report

        Returns:
            QuerySet : data within the report
        """
        report = self.report
        assessments = AssessmentVersion.objects.filter(report=report).order_by("slo__number","number")
        assessment_qs = AssessmentData.objects.none()
        for assessment in assessments:
            assessment_data = AssessmentData.objects.filter(assessmentVersion = assessment)
            assessment_qs.union(assessment_data)
        return assessment_qs
    def get_context_data(self, **kwargs):
        report = self.report
        context = super(DataCollectionSummary, self).get_context_data(**kwargs)
        return section3Context(self,context)


class CreateDataCollectionRow(DeptReportMixin,FormView):
    """
    View to add new data

    Keyword Args:
        assessment (str): primary key of assessment to add data for
    """
    template_name = "makeReports/DataCollection/addDataCollection.html"
    form_class = AddDataCollection
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches view and attaches assessment to instance
        """
        self.assessment = AssessmentVersion.objects.get(pk=self.kwargs['assessment'])
        return super(CreateDataCollectionRow,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        """
        Returns the context for the template, including the assessment

        Returns:
            dict : context of template
        """
        context = super(CreateDataCollectionRow,self).get_context_data(**kwargs)
        context["assess"] = self.assessment
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
    def form_valid(self, form):
        assessmentDataObj = AssessmentData.objects.create(
            assessmentVersion=self.assessment, 
            dataRange=form.cleaned_data['dataRange'], 
            numberStudents=form.cleaned_data['numberStudents'], 
            overallProficient=form.cleaned_data['overallProficient']
            )
        assessmentDataObj.save()
        return super(CreateDataCollectionRow, self).form_valid(form)
class CreateDataCollectionRowAssess(CreateDataCollectionRow):
    """
    View to create data collection row from assessment page
    """
    def get_success_url(self):
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])

class EditDataCollectionRow(DeptReportMixin,FormView):
    """
    View to edit a data point

    Keyword Args:
        dataCollection (str): primary key of data to edit
    """
    template_name = "makeReports/DataCollection/editDataCollection.html"
    form_class = EditDataCollection

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches view and attaches data to instance
        """
        self.dataCollection = AssessmentData.objects.get(pk=self.kwargs['dataCollection'])
        return super(EditDataCollectionRow,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        """
        Gets context for template, including the assessment

        Returns:
            dict : context for template
        """
        context = super(EditDataCollectionRow,self).get_context_data(**kwargs)
        context["assess"] = self.dataCollection.assessmentVersion
        return context
    def get_initial(self):
        """
        Initializes form values based upon current values

        Returns:
            dict : initial form values 
        """
        initial = super(EditDataCollectionRow, self).get_initial()
        initial['dataRange'] = self.dataCollection.dataRange
        initial['numberStudents'] = self.dataCollection.numberStudents
        initial['overallProficient'] = self.dataCollection.overallProficient
        return initial

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.dataCollection.dataRange = form.cleaned_data['dataRange']
        self.dataCollection.numberStudents = form.cleaned_data['numberStudents']
        self.dataCollection.overallProficient = form.cleaned_data['overallProficient']
        self.dataCollection.save()
        return super(EditDataCollectionRow, self).form_valid(form)

class DeleteDataCollectionRow(DeptReportMixin,DeleteView):
    """
    View to delete data point

    Keyword Args:
        pk (str): primary key of data to delete
    """
    model = AssessmentData
    template_name = "makeReports/DataCollection/deleteDataCollection.html"

    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

class CreateSubassessmentRow(DeptReportMixin,FormView):
    form_class = AddSubassessment
    template_name = "makeReports/DataCollection/createSubassessment.html"

    def dispatch(self, request, *args, **kwargs):
        self.assessment = AssessmentVersion.objects.get(pk=self.kwargs['assessment'])
        return super(CreateSubassessmentRow,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(CreateSubassessmentRow,self).get_context_data(**kwargs)
        context["assess"] = self.assessment
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        subassessmentDataObj = Subassessment.objects.create(assessmentVersion=self.assessment, title=form.cleaned_data['title'], proficient=form.cleaned_data['proficient'])
        subassessmentDataObj.save()
        return super(CreateSubassessmentRow, self).form_valid(form)

class EditSubassessmentRow(DeptReportMixin,FormView):
    template_name = "makeReports/DataCollection/editSubassessment.html"
    form_class = EditSubassessment

    def dispatch(self, request, *args, **kwargs):
        self.subassessment = Subassessment.objects.get(pk=self.kwargs['pk'])
        return super(EditSubassessmentRow,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(EditSubassessmentRow, self).get_initial()
        initial['title'] = self.subassessment.title
        initial['proficient'] = self.subassessment.proficient
        return initial
    def get_context_data(self, **kwargs):
        context = super(CreateSubassessmentRow,self).get_context_data(**kwargs)
        context["assess"] = self.subassessment.assessmentVersion
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.subassessment.title = form.cleaned_data['title']
        self.subassessment.proficient = form.cleaned_data['proficient']
        self.subassessment.save()
        return super(EditSubassessmentRow, self).form_valid(form)


class DeleteSubassessmentRow(DeptReportMixin,DeleteView):
    model = Subassessment
    template_name = "makeReports/DataCollection/deleteSubassessment.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

class NewSLOStatus(DeptReportMixin,FormView):
    template_name = "makeReports/DataCollection/SLOStatus.html"
    form_class = SLOStatusForm
    
    def dispatch(self, request, *args, **kwargs):
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        self.slo_ir = SLOInReport.objects.get(slo=self.slo, report__pk=self.kwargs['report'])
        return super(NewSLOStatus,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        slo_status_obj = SLOStatus.objects.create(report = self.report, status = form.cleaned_data['status'], SLO = self.slo)
        slo_status_obj.save()
        return super(NewSLOStatus, self).form_valid(form)


class EditSLOStatus(DeptReportMixin,FormView):
    """
    View to edit SLO status

    Keyword Args:
        slopk (str): primary key of SLO
        statuspk (str): primary key of SLO status
    """
    template_name = "makeReports/Datacollection/SLOStatus.html"
    form_class = SLOStatusForm
    
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches view and attaches SLO and Status to the instance
        """
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        self.slo_ir = SLOInReport.objects.get(slo=self.slo,report=self.report)
        self.slo_status = SLOStatus.objects.get(pk=self.kwargs['statuspk'])
        return super(EditSLOStatus,self).dispatch(request,*args,**kwargs)

    def get_initial(self):
        """
        Initializes form based upon current value

        Returns:
            dict : initial form values
        """
        initial = super(EditSLOStatus, self).get_initial()
        initial['status'] = self.slo_status.status
        return initial
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.slo_status.report = self.report
        self.slo_status.SLO = self.slo
        self.slo_status.status = form.cleaned_data['status']
        self.slo_status.save()
        return super(EditSLOStatus, self).form_valid(form)


class NewResultCommunication(DeptReportMixin,FormView):
    """
    View to create new result communication
    """
    template_name = "makeReports/DataCollection/ResultCommunication.html"
    form_class = ResultCommunicationForm
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        result_communication = ResultCommunicate.objects.create(
            report = self.report, 
            text = form.cleaned_data['text']
            )
        result_communication.save()
        return super(NewResultCommunication, self).form_valid(form)


class EditResultCommunication(DeptReportMixin,FormView):
    """
    View to edit result communication

    Keyword Args:
        resultpk (str): primary key of result to edit
    """
    template_name = "makeReports/DataCollection/ResultCommunication.html"
    form_class = ResultCommunicationForm
    
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches view and attaches result to instance
        """
        self.result_communication = ResultCommunicate.objects.get(pk=self.kwargs['resultpk'])
        return super(EditResultCommunication,self).dispatch(request,*args,**kwargs)

    def get_initial(self):
        initial = super(EditResultCommunication, self).get_initial()
        initial['text'] = self.result_communication.text
        return initial
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

    def form_valid(self, form):
        self.result_communication.report = self.report
        self.result_communication.text = form.cleaned_data['text']
        self.result_communication.save()
        return super(EditResultCommunication, self).form_valid(form)
class Section3Comment(DeptReportMixin,FormView):
    """
    View to add a comment for section 3
    """
    template_name = "makeReports/DataCollection/comment.html"
    form_class = Single2000Textbox
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.report.section3Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section3Comment,self).form_valid(form)
    def get_initial(self):
        initial = super(Section3Comment,self).get_initial()
        initial['text']="No comment."
        return initial
class DataAssessmentAddInfo(DeptReportMixin,CreateView):
    """
    View to add additional information to data section
    """
    model = DataAdditionalInformation
    fields = ['comment','supplement']
    template_name = "makeReports/DataCollection/addInfo.html"
    def form_valid(self,form):
        """
        Sets report to the current report and then creates object based upon the form
        """
        form.instance.report=self.report
        return super(DataAssessmentAddInfo,self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
class DataAssessmentDeleteInfo(DeptReportMixin,DeleteView):
    """
    View to delete additional data information

    Keyword Args:
        pk (str): primary key of data supplement to delete
    """
    model = DataAdditionalInformation
    template_name = "makeReports/DataCollection/deleteInfo.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
class DataAssessmentUpdateInfo(DeptReportMixin,UpdateView):
    """
    View to update data assessment supplement
    
    Keyword Args:
        pk (str): primary key of data info to update
    """
    model = DataAdditionalInformation
    template_name = "makeReports/DataCollection/updateInfo.html"
    fields = ['comment']
    def get_success_url(self):
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
def sloStatusUpdate(sloIR):
    """
    Updates the SLO status based upon the assessment aggregate data points

    Args:
        sloIR (int): primary key of SLO to update the status of
    """
    aggs = AssessmentAggregate.objects.filter(assessmentVersion__slo=sloIR)
    met = True
    partiallyMet = False
    for a in aggs:
        if a.met is False:
            met = False
        if a.met is True:
            partiallyMet=True
        if not met and partiallyMet:
            break
    try:
        sS = SLOStatus.objects.get(report=sloIR.report,SLO=sloIR.slo)
        if met:
            sS.status = SLO_STATUS_CHOICES[0][0]
        elif partiallyMet:
            sS.status = SLO_STATUS_CHOICES[1][0]
        else:
            sS.status = SLO_STATUS_CHOICES[2][0]
        sS.save()
    except:
        if met:
            SLOStatus.objects.create(status=SLO_STATUS_CHOICES[0][0],report=sloIR.report,SLO=sloIR.slo)
        elif partiallyMet:
            SLOStatus.objects.create(status=SLO_STATUS_CHOICES[1][0],report=sloIR.report,SLO=sloIR.slo)
        else:
            SLOStatus.objects.create(status=SLO_STATUS_CHOICES[2][0],report=sloIR.report,SLO=sloIR.slo)
    return
class AssessmentAggregateCreate(DeptReportMixin, CreateView):
    """
    View to create assessment aggregate
    """
    model = AssessmentAggregate
    fields = ['aggregate_proficiency']
    template_name = "makeReports/DataCollection/addAggregate.html"
    def form_valid(self,form):
        """
        Sets whether the target has been met and then create objects based upon the form
        """
        self.assess = AssessmentVersion.objects.get(pk=self.kwargs['assessment'])
        form.instance.assessmentVersion = assess
        if self.assess.target <= form.instance.aggregate_proficiency:
            form.instance.met = True
        else:
            form.instance.met = False
        return super(AssessmentAggregateCreate,self).form_valid(form)
    def get_success_url(self):
        """
        Gets the success url and used as hook to update the SLO status based upon target

        Returns:
            str : URL of data summary
        """
        sloStatusUpdate(self.assess.slo)
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])
class AssessmentAggregateEdit(DeptReportMixin, UpdateView):
    """
    View to edit assessment aggregate

    Keyword Args:
        pk (str): primary key of assessment aggregate to update
    """
    model = AssessmentAggregate
    fields = ['aggregate_proficiency']
    template_name = "makeReports/DataCollection/addAggregate.html"
    def form_valid(self,form):
        """
        Updates object, including whether the target has been met 
        """
        self.assess = AssessmentVersion.objects.get(pk=self.kwargs['assessment'])
        if self.assess.target <= form.instance.aggregate_proficiency:
            form.instance.met = True
        else:
            form.instance.met = False
        return super(AssessmentAggregateEdit,self).form_valid(form)
    def get_success_url(self):
        """
        Gets success url and used as hook to update the SLO status automatically

        Returns:
            str : URL of data collection summary
        """
        sloStatusUpdate(self.assess.slo)
        return reverse_lazy('makeReports:data-summary', args=[self.report.pk])

