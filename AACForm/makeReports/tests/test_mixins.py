"""
Tests related to testing mixins authenticate users correctly
"""
from django.test import TestCase, RequestFactory
from django.urls import reverse
from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest
from makeReports.choices import *
from makeReports.views.helperFunctions.mixins import *
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied

class AACOnlyMixin(TestCase):
    """
    Tests only AAC members can access pages with the AAC mixin
    """
    class DummyView(AACOnlyMixin, TemplateView):
        """
        Dummy view to attach mix-in to
        """
        template_name = 'makeReports/help.html'
    def setUp(self):
        """
        Sets up an instance of the dummy view and a user
        """
        super().setUp()
        self.user = User.objects.create_user( 
                username='Megan',
                email='megan@example.com',
                password = 'passywordy',
            )
        self.col = mommy.make("College")
        self.dept = Department.objects.create(name="Dept",college=self.col)
        self.user.profile.department = self.dept
        self.user.profile.save()
        self.client.login(username='Megan', password='passywordy')
        self.factory = RequestFactory()

    def test_aac(self):
        """
        Tests the AAC member can access the page
        """
        self.user.profile.aac = True
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user =self.user
        resp = self.DummyView.as_view()(request)
        self.assertEquals(resp.status_code,200)
    def test_notaac(self):
        """
        Tests non-AAC members cannot access the page
        """
        self.user.profile.aac = False
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user =self.user
        try:
            resp = self.DummyView.as_view()(request)
            self.assertTrue(False)
        except PermissionDenied:
            self.assertTrue(True)
class DeptOnlyMixin(TestCase):
    """
    Tests only department members can access pages with the DeptOnly mixin
    """
    class DummyView(DeptOnlyMixin, TemplateView):
        """
        Dummy view to attach mix-in to
        """
        template_name = 'makeReports/help.html'
        def dispatch(self,request,*args,**kwargs):
            dept = Department.objects.get(name="Dept43")
            self.report = mommy.make("Report",degreeProgram__department=dept)
            return super().dispatch(request,*args,**kwargs)

    def setUp(self):
        """
        Sets up an instance of the dummy view and a user
        """
        super().setUp()
        self.user = User.objects.create_user( 
                username='Megan',
                email='megan@example.com',
                password = 'passywordy',
            )
        self.col = mommy.make("College")
        self.dept = Department.objects.create(name="Dept43",college=self.col)
        self.client.login(username='Megan', password='passywordy')
        self.factory = RequestFactory()

    def test_aac(self):
        """
        Tests the AAC member not in department cannot access the page
        """
        self.user.profile.aac = True
        self.user.profile.department = mommy.make("Department")
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user = self.user
        try:
            resp = self.DummyView.as_view()(request)
            self.assertTrue(False)
        except PermissionDenied:
            self.assertTrue(True)
    def test_notaac_indept(self):
        """
        Tests non-AAC member in department can access page
        """
        self.user.profile.aac = False
        self.user.profile.department = self.dept
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user =self.user
        resp = self.DummyView.as_view()(request)
        self.assertEquals(resp.status_code,200)
    def test_acc_indept(self):
        """
        Tests AAC member in department can access page
        """
        self.user.profile.aac = True
        self.user.profile.department = self.dept
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user =self.user
        resp = self.DummyView.as_view()(request)
        self.assertEquals(resp.status_code,200)
class DeptAACMixinTests(TestCase):
    """
    Tests the Department or AAC mix-in works correctly
    """
    class DummyView(DeptAACMixin, TemplateView):
        """
        Dummy view to attach mix-in to
        """
        template_name = 'makeReports/help.html'
        def dispatch(self,request,*args,**kwargs):
            dept = Department.objects.get(name="Dept432")
            self.report = mommy.make("Report",degreeProgram__department=dept)
            return super().dispatch(request,*args,**kwargs)

    def setUp(self):
        """
        Sets up an instance of the dummy view and a user
        """
        super().setUp()
        self.user = User.objects.create_user( 
                username='Megan',
                email='megan@example.com',
                password = 'passywordy',
            )
        self.col = mommy.make("College")
        self.dept = Department.objects.create(name="Dept432",college=self.col)
        self.client.login(username='Megan', password='passywordy')
        self.factory = RequestFactory()
    def test_inaac(self):
        """
        Tests that AAC members can access the page
        """
        self.user.profile.aac = True
        self.user.profile.department = mommy.make("Department")
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user = self.user
        resp = self.DummyView.as_view()(request)
        self.assertEquals(resp.status_code,200)
    def test_indept(self):
        """
        Test non-AAC member in department can access page
        """
        self.user.profile.aac = False
        self.user.profile.department = self.dept
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user =self.user
        resp = self.DummyView.as_view()(request)
        self.assertEquals(resp.status_code,200)
    def test_acc_indept(self):
        """
        Tests AAC member in department can access page
        """
        self.user.profile.aac = True
        self.user.profile.department = self.dept
        self.user.profile.save()
        request = self.factory.get('/dummy')
        request.user =self.user
        resp = self.DummyView.as_view()(request)
        self.assertEquals(resp.status_code,200)
    def test_notdept(self):
        """
        Tests non-AAC person not in department cannot access the page
        """
        self.user.profile.aac = False
        self.user.profile.department = mommy.make("Department", name="NotDept")
        self.user.profile.save()
        self.user.refresh_from_db()
        request = self.factory.get('/dummy')
        request.user = self.user
        try:
            resp = self.DummyView.as_view()(request)
            self.assertTrue(False)
        except PermissionDenied:
            self.assertTrue(True)
