from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
class NonAACTest(TestCase):
    def setUp(self):
        """
        Setups a user
        """
        #Book.objects.create(title='Work Week', author="Gary S.")
        self.user = User.objects.create_user( 
                username='Megan',
                email='megan@example.com',
                password = 'passywordy',
            )
        self.col = mommy.make("College")
        self.dept = Department.objects.create(name="Dept",college=col)
        self.user.profile.department = dept
        self.user.profile.save()
        self.client.login(username='Megan', password='passywordy')

class AACTest(TestCase):
        def setUp(self):
        """
        Setups a user
        """
        #Book.objects.create(title='Work Week', author="Gary S.")
        self.user = User.objects.create_user( 
                username='Megan',
                email='megan@example.com',
                password = 'passywordy',
            )
        self.col = mommy.make("College")
        self.dept = Department.objects.create(name="Dept",college=col)
        self.user.profile.department = dept
        self.user.profile.aac = True
        self.user.profile.save()
        self.client.login(username='Megan', password='passywordy')

class UserModifyUserTest(NonAACTest):
    """
    Tests UserModifyAccount Page returns 200 response
    """
    def test_view(self):
        """
        Tests the 200 reponse and then 302 reponse after logout
        """
        response = self.client.get(reverse('makeReports:modify-acct'))
        self.assertEquals(response.status_code,200)
        self.client.logout()
        response = self.client.get(reverse('makeReports:modify-acct'))
        self.assertEquals(response.status_code,302)
        #self.assertContains(response, "Work Week by Gary S.")
        #self.assertContains(response, "Cat Fact")
        #self.assertTemplateUsed(response,"books.html")
class FacultyReportList(NonAACTest):
    """
    Tests Faculty Report List page
    """
    def test_view(self):
        """
        Checks response code before and after logging out
        """
        response = self.client.get(reverse('makeReports:rpt-list-dept'))
        self.assertEquals(response.status_code,200)
        self.client.logout()
        response = self.client.get(reverse('makeReports:rpt-list-dept'))
        self.assertEquals(response.status_code,302)
class ReportListSearchedDept(AACTest):
    """
    Tests the by department report list page
    """
    def setUp(self):
        """
        Sets up user and creates report to search
        """
        super(ReportListSearchedDept,self).setUp()
        degProg = mommy.make('DegreeProgram')
        degProg.department = self.dept
        self.rpt = mommy.make('Report')
        self.rpt.submitted = True
        self.rpt.returned = False
        self.rpt.degreeProgram = degProg
        self.rpt.save()
    def test_view(self):
        response = self.client.get(reverse('makeReports:search-reports-dept',args={}))
