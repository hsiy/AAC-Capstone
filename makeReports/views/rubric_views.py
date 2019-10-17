from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin
from makeReports.views.helperFunctions.mixins import *
class RubricList(AACOnlyMixin,ListView):
    model = Rubric
    template_name = "makeReports/Rubric/rubricList.html"
    def get_queryset(self):
        return Rubric.objects.order_by("-date")
class SearchRubricList(AACOnlyMixin,ListView):
    model = Rubric
    template_name = "makeReports/Rubric/rubricList.html"
    def get_queryset(self):
        rubs = Rubric.objects
        day = self.request.GET['date']
        if self.request.GET['name']!="":
            rubs=rubs.filter(name__icontains=self.request.GET['name'])
        if day!="":
            rubs=rubs.filter(date__range=(datetime.strptime(day,"%Y-%m-%d")-timedelta(days=180),datetime.strptime(day,"%Y-%m-%d")+timedelta(days=180)))
        return rubs.order_by("-date")
class AddRubric(AACOnlyMixin,CreateView):
    template_name = "makeReports/Rubric/addRubric.html"
    success_url = reverse_lazy('makeReports:rubric-list')
    model=Rubric
    fields = ['name','fullFile']
    def form_valid(self,form):
        form.instance.date = datetime.now()
        return super(AddRubric,self).form_valid(form)
class AddRubricItems(AACOnlyMixin, FormView):
    template_name = "makeReports/Rubric/addRI.html"
    form_class = RubricItemForm
    def dispatch(self, request,*args, **kwargs):
        self.rubric = Rubric.objects.get(pk=self.kwargs['rubric'])
        return super(AddRubricItems, self).dispatch(request,*args,**kwargs)
    def form_valid(self,form):
        ri = RubricItem.objects.create(text=form.cleaned_data['text'], \
                section=form.cleaned_data['section'], rubricVersion=self.rubric, \
                    DMEtext=form.cleaned_data['DMEtext'], MEtext=form.cleaned_data['MEtext'], \
                        EEtext=form.cleaned_data['EEtext'])
        try:
            ri.order=form.cleaned_data['order']
            ri.save()
        except:
            pass
        return super(AddRubricItems,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(AddRubricItems,self).get_context_data(**kwargs)
        context['numRIs'] = RubricItem.objects.filter(rubricVersion=self.rubric).count()
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:add-RI', args=[self.kwargs['rubric']])
class ViewRubric(AACOnlyMixin,DetailView):
    model = Rubric
    template_name = "makeReports/Rubric/rubricDetail.html"
    def get_context_data(self,**kwargs):
        context = super(ViewRubric,self).get_context_data(**kwargs)
        context['rIs'] = RubricItem.objects.filter(rubricVersion=self.object).order_by("section","order","pk")
        context['obj'] = self.object
        return context
class UpdateRubricItem(AACOnlyMixin,UpdateView):
    model = RubricItem
    fields = ['text','abbreviation','section','order','DMEtext','MEtext','EEtext']
    template_name = "makeReports/Rubric/updateRubricItem.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:view-rubric',args=[self.kwargs['rubric']])
class UpdateRubricFile(AACOnlyMixin, UpdateView):
    model = Rubric
    fields = ['name','fullFile']
    template_name = "makeReports/Rubric/updateRubric.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:view-rubric',args=[self.kwargs['rubric']])
class DeleteRubricItem(AACOnlyMixin,DeleteView):
    model = RubricItem
    template_name = "makeReports/Rubric/deleteRubricItem.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:view-rubric',args=[self.kwargs['rubric']])
class DuplicateRubric(AACOnlyMixin, FormView):
    #duplicate -> edit/delete/add intended workflow instead of some kind of import
    form_class = DuplicateRubricForm
    success_url = reverse_lazy('makeReports:rubric-list')
    template_name = "makeReports/Rubric/duplicateRubric.html"
    def form_valid(self,form):
        rubToDup = Rubric.objects.get(pk=self.kwargs['rubric'])
        RIs = RubricItem.objects.filter(rubricVersion=rubToDup)
        newRub = Rubric.objects.create(date=datetime.now(), fullFile=rubToDup.fullFile, name=form.cleaned_data['new_name'])
        for ri in RIs:
            newRi = RubricItem.objects.create(text=ri.text, abbreviation=ri.abbreviation, section=ri.section, rubricVersion=newRub,order=ri.order,DMEtext=ri.DMEtext,MEtext=ri.MEtext,EEtext=ri.EEtext)
        return super(DuplicateRubric,self).form_valid(form)
class DeleteRubric(AACOnlyMixin,DeleteView):
    model = Rubric
    template_name = "makeReports/Rubric/deleteRubric.html"
    def get_success_url(self):
        return reverse_lazy('makeReports:rubric-list')