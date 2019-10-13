from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
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
from django.template.defaulttags import register
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from makeReports.views.helperFunctions.section_context import *
from django_weasyprint import WeasyTemplateResponseMixin, WeasyTemplateView
from PyPDF2 import PdfFileMerger, PdfFileReader
from types import SimpleNamespace
from weasyprint import HTML, CSS
from django.core.files import File
import tempfile
import os, io, requests
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.utils import six
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse
def test_func_x(self,*args,**kwargs):
    report = Report.objects.get(pk=kwargs['report'])
    dept= (report.degreeProgram.department == self.profile.department)
    aac = getattr(self.profile, "aac")
    return dept or aac
def test_func_a(self):
    aac = getattr(self.profile, "aac")
    return aac
def my_user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # the following line is the only change with respect to
            # user_passes_test:
            if test_func(request.user, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator
class GradedRubricPDFGen(WeasyTemplateView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "makeReports/Grading/feedbackPDF.html"
    pdf_stylesheets =[
        # Change this to suit your css path
        settings.STATIC_ROOT + '\\css\\report.css',
        settings.STATIC_ROOT + '\\css\\landscape.css',
        #settings.STATIC_ROOT + '\\css\\bootstrap-print-color.css',
        #settings.BASE_DIR + 'css/main.css',
    ]
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(GradedRubricPDFGen,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(GradedRubricPDFGen,self).get_context_data(**kwargs)
        context['rubric'] = self.report.rubric
        context['GRIs1'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=1)
        context['GRIs2'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=2)
        context['GRIs3'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=3)
        context['GRIs4'] = GradedRubricItem.objects.filter(rubric=self.report.rubric, item__section=4)
        return context
    def test_func(self):
        dept= (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
class ReportPDFGen(WeasyTemplateView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "makeReports/DisplayReport/pdf.html"
    pdf_stylesheets =[
        settings.STATIC_ROOT + '\\css\\report.css',
        #settings.BASE_DIR + 'css/main.css',
    ]
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(ReportPDFGen,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(ReportPDFGen,self).get_context_data(**kwargs)
        context['rubric'] = self.report.rubric
        context['report'] = self.report
        context = section1Context(self,context)
        context = section2Context(self,context)
        context = section3Context(self,context)
        context = section4Context(self,context)
        return context
    def test_func(self):
        dept= (self.report.degreeProgram.department == self.request.user.profile.department)
        aac = getattr(self.request.user.profile, "aac")
        return dept or aac
@login_required
@my_user_passes_test(test_func_x)
def reportPDF(request, report):
    report = get_object_or_404(Report, pk=report)
    sec1and2 = get_template('makeReports/DisplayReport/PDFsub/pdf1and2.html')
    sec3 = get_template('makeReports/DisplayReport/PDFsub/pdf3.html')
    sec4 = get_template('makeReports/DisplayReport/PDFsub/pdf4.html')
    context = {'report':report}
    s = SimpleNamespace(**context)
    context = section1Context(s,context)
    context = section2Context(s,context)
    p1and2 = sec1and2.render(context).encode(encoding="ISO-8859-1")
    context = {'report':report}
    context = section3Context(s,context)
    p3 = sec3.render(context).encode(encoding="ISO-8859-1")
    context = {'report':report}
    context = section4Context(s,context)
    p4 =sec4.render(context).encode(encoding="ISO-8859-1")
    assessSups = AssessmentSupplement.objects.filter(assessmentversion__report=report)
    dataSups = DataAdditionalInformation.objects.filter(report=report)
    repSups = ReportSupplement.objects.filter(report=report)
    html1and2 = HTML(string=p1and2)
    html3 = HTML(string=p3)
    html4 = HTML(string=p4)
    f1and2 = tempfile.TemporaryFile()
    f3 = tempfile.TemporaryFile()
    f4 = tempfile.TemporaryFile()
    pdf1and2 = html1and2.write_pdf(target=f1and2,stylesheets=[CSS(settings.STATIC_ROOT+'/css/report.css')])
    pdf3 = html3.write_pdf(target=f3,stylesheets=[CSS(settings.STATIC_ROOT+'/css/report.css')])
    pdf4 = html4.write_pdf(target=f4,stylesheets=[CSS(settings.STATIC_ROOT+'/css/report.css')]) 
    merged = PdfFileMerger()
    merged.append(f1and2)
    for sup in assessSups:
        rep = requests.get(sup.supplement.url)
        with io.BytesIO(rep.content) as open_pdf_file:
            read_pdf = PdfFileReader(open_pdf_file)
            merged.append(read_pdf)
    merged.append(f3)
    for sup in dataSups:
        rep = requests.get(sup.supplement.url)
        with io.BytesIO(rep.content) as open_pdf_file:
            read_pdf = PdfFileReader(open_pdf_file)
            merged.append(read_pdf)
    merged.append(f4)
    for sup in repSups:
        rep = requests.get(sup.supplement.url)
        with io.BytesIO(rep.content) as open_pdf_file:
            read_pdf = PdfFileReader(open_pdf_file)
            merged.append(read_pdf)
    http_response = HttpResponse(content_type="application/pdf")
    merged.write(http_response)
    return http_response
@login_required
@user_passes_test(test_func_a)
def UngradedRubric(request, rubric):
    rubric = get_object_or_404(Rubric, pk=rubric)
    template = get_template("makeReports/Grading/rubricPDF.html")
    context = dict()
    context['rubric'] = rubric
    context['RIs1'] = RubricItem.objects.filter(rubricVersion=rubric, section=1)
    context['RIs2'] = RubricItem.objects.filter(rubricVersion=rubric, section=2)
    context['RIs3'] = RubricItem.objects.filter(rubricVersion=rubric, section=3)
    context['RIs4'] = RubricItem.objects.filter(rubricVersion=rubric, section=4)
    rend = template.render(context).encode(encoding="ISO-8859-1")
    html = HTML(string=rend)
    f = tempfile.TemporaryFile()
    pdf = html.write_pdf(target=rubric.fullFile,stylesheets=[CSS(settings.STATIC_ROOT+'/css/report.css'),CSS(settings.STATIC_ROOT+'/css/landscape.css')])
    http_response = FileResponse(rubric.fullFile.open(),content_type="application/pdf")
    rubric.save()
    return http_response
