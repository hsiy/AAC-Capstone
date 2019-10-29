from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, FormView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from django.template.defaulttags import register
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *
def generateRubricItems(rIs,form,r):
    """
    Generates graded rubric items based on grading form

    Args:
        rIs (list) : list of :class:`~makeReports.models.report-models.RubricItem` in rubric
        form (Form) : completed form
        r (Report) : report
    """
    for ri in rIs:
        if form.cleaned_data["rI"+str(ri.pk)]:
            try:
                GRI = GradedRubricItem.objects.get(rubric=r.rubric, item=ri)
                GRI.grade=form.cleaned_data["rI"+str(ri.pk)]
            except:
                gr = form.cleaned_data["rI"+str(ri.pk)]
                if gr and (gr != ""):
                    newGRI = GradedRubricItem.objects.create(rubric=r.rubric, item=ri, grade=form.cleaned_data["rI"+str(ri.pk)])
def getInitialRubric(rIs, r, initial):
    """
    Initializes grading form based upon things already graded

    Args:
        rIs (list) : list of :class:`~makeReports.models.report-models.RubricItem` in rubric
        form (Form) : completed form
        r (Report) : report
    
    Returns:
        dict : initial rubric values
    """
    for ri in rIs:
        try:
            GRI = GradedRubricItem.objects.filter(rubric=r.rubric, item=ri).last()
            initial["rI"+str(ri.pk)]=GRI.grade
        except:
            pass
    return initial
@register.simple_tag
def get_item(dictionary, key1, key2):
    """
    Gets item from dictionary in dictionary

    Args:
        dictionary (dict) : outer dictionary
        key1 (str) : first dictionary key
        key2 (str) : second dictionary key
    
    Returns:
        obj : dictionary[key1][key2]
    """
    s = dictionary.get(key1)
    if s:
        return mark_safe(s[key2])
    else:
        return ""
class GradingView(AACOnlyMixin,FormView):
    """
    View to grade one section of a form

    Keyword Args:
        report (str): primary key of current report to grade
    """
    form_class = SectionRubricForm
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view, and attaches report and rubric items to instance
        """
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.rubricItems = RubricItem.objects.filter(
            rubricVersion=self.report.rubric.rubricVersion,
            section=self.section
            ).order_by("order","pk")
        return super().dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy("makeReports:grade-sec"+str(self.section+1), args=[self.report.pk])
    def get_form_kwargs(self):
        """
        Get form keyword arguments, including the rubric items

        Returns:
            dict : keyword arguments for the form
        """
        kwargs= super().get_form_kwargs()
        kwargs['rubricItems'] = self.rubricItems
        return kwargs
    def form_valid(self,form):
        """
        Generates all graded rubric items and sets the grading comment for the section
        """
        generateRubricItems(self.rubricItems,form,self.report)
        tempStr = "section"+str(self.section)+"Comment"
        setattr(self.report.rubric,tempStr, form.cleaned_data['section_comment'])
        self.report.rubric.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        """
        Gets template context, including the section, report, and rubric items
        """
        context = super().get_context_data(**kwargs)
        context = rubricItemsHelper(self,context)
        context['section'] = self.section
        context['report'] = self.report
        context['rpt'] = self.report
        return context
    def get_initial(self):
        initial = super().get_initial()
        initial = getInitialRubric(self.rubricItems,self.report,initial)
        return initial
class Section1Grading(GradingView):
    """
    View for grading section 1
    """
    section = 1
    template_name = "makeReports/Grading/grading_section1.html"
    #model = SLOInReport
    success_url = reverse_lazy("makeReports:admin-home")
    def get_context_data(self, **kwargs):
        context = super(Section1Grading,self).get_context_data(**kwargs)
        return section1Context(self,context)
    def get_initial(self):
        initial = super(Section1Grading,self).get_initial()
        initial['section_comment'] = self.report.rubric.section1Comment
        return initial
class Section2Grading(GradingView):
    """
    View for grading section 2
    """
    section = 2
    template_name = "makeReports/Grading/grading_section2.html"
    def get_context_data(self, **kwargs):
        context = super(Section2Grading,self).get_context_data(**kwargs)
        return section2Context(self,context)
    def get_initial(self):
        initial = super(Section2Grading,self).get_initial()
        initial['section_comment'] = self.report.rubric.section2Comment
        return initial
class Section3Grading(GradingView):
    """
    View for grading section 3
    """
    section = 3
    template_name = "makeReports/Grading/grading_section3.html"
    def get_context_data(self, **kwargs):
        context = super(Section3Grading,self).get_context_data(**kwargs)
        return section3Context(self,context)
    def get_initial(self):
        initial = super(Section3Grading,self).get_initial()
        initial['section_comment'] = self.report.rubric.section3Comment
        return initial
class Section4Grading(GradingView):
    """
    View for grading section 4
    """
    section = 4
    template_name = "makeReports/Grading/grading_section4.html"
    def get_success_url(self):
        return reverse_lazy("makeReports:grade-comment", args=[self.report.pk])
    def get_context_data(self, **kwargs):
        context = super(Section4Grading,self).get_context_data(**kwargs)
        return section4Context(self,context)
    def get_initial(self):
        initial = super(Section4Grading,self).get_initial()
        initial['section_comment'] = self.report.rubric.section4Comment
        return initial
class OverallComment(AACReportMixin,FormView):
    """
    View to add an overall comment to the report
    """
    form_class = Single2000Textbox
    template_name = "makeReports/Grading/overall_comment.html"
    def get_success_url(self):
        return reverse_lazy("makeReports:rub-review", args=[self.report.pk])
    def get_context_data(self,**kwargs):
        """
        Returns template context, including the current report

        Returns:
            dict : context of template
        """
        context = super(OverallComment,self).get_context_data(**kwargs)
        context['report'] = self.report
        return context
    def form_valid(self, form):
        self.report.rubric.generalComment = form.cleaned_data['text']
        self.report.rubric.save()
        return super(OverallComment,self).form_valid(form)
    def get_initial(self):
        initial = super(OverallComment,self).get_initial()
        try:
            initial['text'] = self.report.rubric.generalComment
        except:
            pass
        return initial
class RubricReview(AACReportMixin, FormView):
    """
    View to review graded rubric
    """
    template_name = "makeReports/Grading/rubric_review.html"
    form_class = SubmitGrade
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches the view and attaches the graded rubric items to the instance
        """
        self.GRIs = GradedRubricItem.objects.filter(rubric__report__pk=self.kwargs['report'])
        return super(RubricReview,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        """
        Gets the form keyword arguments, including whether the graded rubric is compelete

        Returns:
            dict : keyword arguments for form
        """
        kwargs=super(RubricReview,self).get_form_kwargs()
        #valid iff there's a graded rubric item for every rubric item
        kwargs['valid'] = (self.GRIs.count() >= RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion).count())
        return kwargs
    def form_valid(self,form):
        """
        Sets the rubric to complete and saves the rubric
        """
        self.report.rubric.complete = True
        self.report.rubric.save()
        return super(RubricReview,self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('makeReports:ret-rept', args=[self.report.pk])
    def get_context_data(self,**kwargs):
        """
        Gets the context data, including the report, the graded rubric and items, and the 
        context needed to display the report

        Returns:
            dict : context for template
        """
        context = super(RubricReview,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['gRub'] = self.report.rubric
        context['object_list'] = self.GRIs
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
class ReturnReport(AACOnlyMixin,UpdateView):
    """
    View to return report to department for modification

    Keyword Args:
        pk (str): primary key of report to return
    """
    model = Report
    fields = ['returned']
    template_name = 'makeReports/Grading/returnReport.html'
    success_url = reverse_lazy('makeReports:admin-home')
    def form_valid(self,form):
        """
        Sets the report to be returned, not submitted, and not complete
        """
        if form.cleaned_data['returned']:
            self.object.submitted = False
            self.object.rubric.complete = False
        return super(ReturnReport,self).form_valid(form)
class Feedback(DeptAACMixin, ListView):
    """
    View for department to view AAC feedback

    Keyword Args:
        report (str): primary key of report to view feedback for
    """
    model = GradedRubricItem
    template_name = "makeReports/Grading/feedback.html"
    def dispatch(self,request,*args,**kwargs):
        """
        Dispatches view and attaches report and graded items to the view
        """
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.GRIs = GradedRubricItem.objects.filter(rubric__report=self.report)
        return super(Feedback,self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        return self.GRIs
    def get_success_url(self):
        return reverse_lazy('makeReports:ret-rept', args=[self.report.pk])
    def get_context_data(self, **kwargs):
        """
        Gets context for the template, including the report, graded rubric items, and
        context needed to display the report

        Returns:
            dict : context for template
        """
        context = super(Feedback,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['gRub'] = self.report.rubric
        context['obj_list'] = self.GRIs
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
