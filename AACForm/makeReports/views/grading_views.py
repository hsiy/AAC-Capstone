from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, FormView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from django.template.defaulttags import register
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *
def generateRubricItems(rIs,form,r):
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
    for ri in rIs:
        try:
            GRI = GradedRubricItem.objects.filter(rubric=r.rubric, item=ri).last()
            initial["rI"+str(ri.pk)]=GRI.grade
        except:
            pass
    return initial
@register.simple_tag
def get_item(dictionary, key1, key2):
    s = dictionary.get(key1)
    if s:
        return mark_safe(s[key2])
    else:
        return ""
class GradingView(AACOnlyMixin,FormView):
    form_class = SectionRubricForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.rubricItems = RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion,section=self.section).order_by("order","pk")
        return super().dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy("makeReports:grade-sec"+str(self.section+1), args=[self.report.pk])
    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs['rubricItems'] = self.rubricItems
        return kwargs
    def form_valid(self,form):
        generateRubricItems(self.rubricItems,form,self.report)
        tempStr = "section"+str(self.section)+"Comment"
        setattr(self.report.rubric,tempStr, form.cleaned_data['section_comment'])
        self.report.rubric.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
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
    form_class = Single2000Textbox
    template_name = "makeReports/Grading/overall_comment.html"
    def get_success_url(self):
        return reverse_lazy("makeReports:rub-review", args=[self.report.pk])
    def get_context_data(self,**kwargs):
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
    template_name = "makeReports/Grading/rubric_review.html"
    form_class = SubmitGrade
    def dispatch(self,request,*args,**kwargs):
        self.GRIs = GradedRubricItem.objects.filter(rubric__report__pk=self.kwargs['report'])
        return super(RubricReview,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs=super(RubricReview,self).get_form_kwargs()
        #valid iff there's a graded rubric item for every rubric item
        kwargs['valid'] = (self.GRIs.count() >= RubricItem.objects.filter(rubricVersion=self.report.rubric.rubricVersion).count())
        return kwargs
    def form_valid(self,form):
        self.report.rubric.complete = True
        self.report.rubric.save()
        return super(RubricReview,self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('makeReports:ret-rept', args=[self.report.pk])
    def get_context_data(self,**kwargs):
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
    model = Report
    fields = ['returned']
    template_name = 'makeReports/Grading/returnReport.html'
    success_url = reverse_lazy('makeReports:admin-home')
    def form_valid(self,form):
        if form.cleaned_data['returned']:
            self.object.submitted = False
            self.object.rubric.complete = False
        return super(ReturnReport,self).form_valid(form)
class Feedback(DeptAACMixin, ListView):
    model = GradedRubricItem
    template_name = "makeReports/Grading/feedback.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.GRIs = GradedRubricItem.objects.filter(rubric__report=self.report)
        return super(Feedback,self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        return self.GRIs
    def get_success_url(self):
        return reverse_lazy('makeReports:ret-rept', args=[self.report.pk])
    def get_context_data(self, **kwargs):
        context = super(Feedback,self).get_context_data(**kwargs)
        context['report'] = self.report
        context['gRub'] = self.report.rubric
        context['obj_list'] = self.GRIs
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
