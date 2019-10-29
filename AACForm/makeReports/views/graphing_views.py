from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from makeReports.models import *
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *

class GraphingHome(DeptAACMixin,TemplateView):
    template_name = "graphing.html"
    def get_context_data(self, **kwargs):
        context = super(GraphingHome, self).get_context_data(**kwargs)
        context['colleges'] = College.active_objects.all
        return context