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
class RubricList(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Rubric
    template_name = "makeReports/Rubric/rubricList.html"
    def get_queryset(self):
        return Rubric.objects.order_by("-date")
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class AddRubric(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    template_name = "makeReports/Rubric/addRubric.html"
    success_url = reverse_lazy('makeReports:rubric-list')
    model=Rubric
    fields = ['name','fullFile']
    def form_valid(self,form):
        form.instance.date = datetime.now()
        return super(AddRubric,self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class AddRubricItems(LoginRequiredMixin,UserPassesTestMixin, FormView):
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
    def get_context_data(self):
        context = super(AddRubricItems,self).get_context_data()
        context['numRIs'] = RubricItem.objects.filter(rubricVersion=self.rubric).count()
        return context
    def get_success_url(self):
        return reverse_lazy('makeReports:add-RI', args=[self.kwargs['rubric']])
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class ViewRubric(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Rubric
    template_name = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class UpdateRubricItem(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = RubricItem
    fields = ['text','section','order','DMEtext','MEtext','EEtext']
    template_name = ""
    success_url = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class UpdateRubricFile(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Rubric
    fields = ['name','fullFile']
    template_name = ""
    success_url = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DeleteRubricItem(LoginRequiredMixin,UserPassesTestMixin):
    #error will result if they try to delete a ri that already has a grade somewhere
    model = RubricItem
    template_name = ""
    success_url = ""
    def test_func(self):
        return getattr(self.request.user.profile, "aac")
class DuplicateRubric(LoginRequiredMixin,UserPassesTestMixin, FormView):
    #duplicate -> edit/delete/add intended workflow instead of some kind of import
    form_class = DuplicateRubric
    success_url = ""
    template_name = ""
    def form_valid(self,form):
        rubToDup = form.cleaned_data['rubToDup']
        RIs = RubricItem.objects.filter(rubricVersion=rubToDup)
        newRub = Rubric.object.create(date=datetime.now(), fullFile=rubToDup.fullFile)
        for ri in RIs:
            newRi = RubricItem.object.create(text=ri.text, section=ri.section, rubricVersion=newRub,order=ri.order,DMEtext=ri.DMEtext,MEtext=ri.MEtext,EEtext=ri.EEtext)
        return super(DuplicateRubric,)
    def test_func(self):
        return getattr(self.request.user.profile, "aac")