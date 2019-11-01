from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
class NonAACTest(TestCase):
    """
    Creates Non AAC member logged in
    """
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
        self.dept = Department.objects.create(name="Dept",college=self.col)
        self.user.profile.department = self.dept
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
        self.dept = Department.objects.create(name="Dept",college=self.col)
        self.user.profile.department = self.dept
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
class ReportAACSetupTest(AACTest):
    """
    Creates a report during setup to test
    """
    def setUp(self):
        """
        Sets up user and creates report to search
        """
        super(ReportAACSetupTest,self).setUp()
        self.degProg = mommy.make('DegreeProgram')
        self.degProg.department = self.dept
        self.degProg.save()
        self.rpt = mommy.make('Report')
        self.rpt.submitted = True
        self.rpt.degreeProgram = self.degProg
        self.rpt.save()
class ReportSetupTest(NonAACTest):
    def setUp(self):
        """
        Sets up user and creates report to search
        """
        super(ReportSetupTest,self).setUp()
        self.degProg = mommy.make('DegreeProgram')
        self.degProg.department = self.dept
        self.degProg.save()
        self.rpt = mommy.make('Report')
        self.rpt.submitted = True
        self.rpt.degreeProgram = self.degProg
        self.rpt.save()

class ReportListSearchedDept(ReportAACSetupTest):
    """
    Tests the by department report list page
    """
    def test_view(self):
        """
        Test 200 response and that report is in the list
        """
        response = self.client.get(reverse('makeReports:search-reports-dept')+"?submitted=S&year=&dP=&graded=")
        self.assertEquals(response.status_code,200)
        self.assertContains(response,self.rpt.degreeProgram.name)
        response = self.client.get(reverse('makeReports:search-reports-dept')+"?submitted=nS&year=&dP=&graded=")
        self.assertNotContains(response,self.rpt.degreeProgram.name)
class DisplayReportTest(ReportSetupTest):
    """
    Tests display report page
    """
    def test_view(self):
        """
        Tests 200 response and that something from the report is displayed
        """
        response = self.client.get(reverse('makeReports:view-rpt',kwargs={'pk':self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response, self.rpt.degreeProgram.name)
        self.assertContains(response, self.rpt.degreeProgram.department.name)
        self.assertContains(response, self.rpt.author)
        self.assertContains(response, "SLO")
        self.assertContains(response, "Assessment")
        self.assertContains(response, "Data")
        self.assertContains(response, "Decision")