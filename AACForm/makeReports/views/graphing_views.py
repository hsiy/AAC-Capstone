from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *

class getDataSet(LoginRequiredMixin,ListView):
    model = Report
    template_name = "graphing/graph_search.html"
    def get_queryset(self):
        dP = self.request.GET['dP']
        objs = Report.objects.filter(degreeProgram__department=self.request.user.profile.department, degreeProgram__active=True).order_by('submitted','-rubric__complete')
        if dP!="":
            objs=objs.filter(degreeProgram__name__icontains=dP)
        return objs