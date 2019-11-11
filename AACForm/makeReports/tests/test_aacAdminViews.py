from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from makeReports.choices import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest, getWithReport, postWithReport
from datetime import datetime
class AACBasicViewsTest(ReportAACSetupTest):
    """
    Tests the basic AAC admin views, such as home
    """
    def test_home(self):
        """
        Tests the home page exists
        """
        response = self.client.get(reverse('makeReports:admin-home'))
        self.assertEquals(response.status_code,200)
class AACCollegeViewsTest(ReportAACSetupTest):
    """
    Tests the AAC admin views related to the colleges
    """
    def test_create(self):
        """
        Tests that the create college page exists and works
        """
        data = {
            'name': 'col name'
        }
        response = self.client.post(reverse('makeReports:add-college'),data)
        num = College.active_objects.filter(name='col name').count()
        self.assertGreaterEqual(num,1)
    def test_list(self):
        """
        Tests the list page contains a college made and not an inactive college
        """
        col = mommy.make("College", active=True)
        colI = mommy.make("College",active=False)
        response = self.client.get(reverse('makeReports:college-list'))
        self.assertContains(response,col.name)
        self.assertNotContains(response,colI.name)
    def test_delete(self):
        """
        Tests the delete page deletes the college
        """
        col = mommy.make("College")
        pk = col.pk
        response = self.client.post(reverse('makeReports:delete-college',kwargs={'pk':col.pk}))
        num = College.active_objects.filter(pk=pk).count()
        self.assertEquals(num,0)
    def test_recover(self):
        """
        Tests the recover page in fact re-marks the college as active
        """
        col = mommy.make("College",active=False)
        response = self.client.post(reverse('makeReports:recover-college',kwargs={'pk':col.pk}),{'active':'on'})
        col.refresh_from_db()
        self.assertTrue(col.active)
class DepartmentViewsTest(ReportAACSetupTest):
    """
    Tests the views relating to department administration
    """
    def test_create(self):
        """
        Tests that posting to the create department page works as expected
        """
        col = mommy.make("College")
        data = {
            'name':'dept name',
            'college': col.pk
        }
        r = self.client.post(reverse('makeReports:add-dept'),data)
        num = Department.objects.filter(name='dept name',college=col).count()
        self.assertGreaterEqual(num,1)
    def test_list(self):
        """
        Tests that list of department contains active departments
        """
        dept = mommy.make("Department")
        dep2 = mommy.make("Department",active=False)
        response = self.client.get(reverse('makeReports:dept-list')+"?college=&name=")
        self.assertContains(response,dept.name)
        self.assertNotContains(response,dep2.name)
    def test_update(self):
        """
        Tests that updating department works as expected
        """
        dept = mommy.make("Department")
        r = self.client.post(reverse('makeReports:update-dept',kwargs={'pk':dept.pk}),{'name':"d name 2","college":dept.college.pk})
        dept.refresh_from_db()
        self.assertEquals(dept.name,"d name 2")
    def test_delete(self):
        """
        Tests that the delete view marks the department inactive
        """
        dept = mommy.make("Department",active=True)
        r = self.client.post(reverse('makeReports:delete-dept',kwargs={'pk':dept.pk}))
        dept.refresh_from_db()
        self.assertFalse(dept.active)
    def test_recover(self):
        """
        Tests that recovering a department works as expected
        """
        dept = mommy.make("Department",active=False)
        r = self.client.post(reverse('makeReports:recover-dept',kwargs={'pk':dept.pk}),{'active':'on'})
        dept.refresh_from_db()
        self.assertTrue(dept.active)
class DegreeProgramAdminTest(ReportAACSetupTest):
    """
    Tests that views relating degree program administration
    """
    def setUp(self):
        super(DegreeProgramAdminTest,self).setUp()
        self.dept = mommy.make("Department")
    def test_create(self):
        """
        Tests that a degree program is created
        """
        r = self.client.post(reverse('makeReports:add-dp',kwargs={'dept':self.dept.pk}),{
            'name':'dp name',
            'level':"UG",
            'cycle': 5,
            'startingYear': 7
        })
        num = DegreeProgram.objects.filter(department=self.dept,name='dp name',cycle=5, startingYear=7, level="UG").count()
        self.assertGreaterEqual(num, 1)
    def test_create_emptyslots(self):
        """
        Tests that a degree program is created when cycle and starting year are left blank
        """
        r = self.client.post(reverse('makeReports:add-dp',kwargs={'dept':self.dept.pk}),{
            'name':'dp name 2',
            'level':'GR',
            'cycle': 0
        })
        num = DegreeProgram.objects.filter(department=self.dept,name='dp name 2', level="GR").count()
        self.assertGreaterEqual(num, 1)
    def test_update(self):
        """
        Tests that a degree program is effectively updated
        """
        dp = mommy.make("DegreeProgram",department=self.dept)
        r = self.client.post(reverse('makeReports:update-dp',kwargs={'dept':self.dept.pk,'pk':dp.pk}),{
            'name':'up dp',
            'level':'GR',
        })
        dp.refresh_from_db()
        self.assertEquals(dp.name,'up dp')
        self.assertEquals(dp.level,'GR')
    def test_recover(self):
        """
        Tests that recovering a DP works and sets it to active
        """
        dp = mommy.make("DegreeProgram",active=False,department=self.dept)
        self.client.post(reverse('makeReports:recover-dp',kwargs={'dept':self.dept.pk,'pk':dp.pk}),{'active':'on'})
        dp.refresh_from_db()
        self.assertTrue(dp.active)
    def test_delete(self):
        """
        Tests that deleting a DP sets it to inactive
        """
        dp = mommy.make("DegreeProgram",active=True,department=self.dept)
        self.client.post(reverse('makeReports:delete-dp',kwargs={'dept':self.dept.pk,'pk':dp.pk}))
        dp.refresh_from_db()
        self.assertFalse(dp.active)
class ReportAdminViewTests(ReportAACSetupTest):
    """
    Tests views relating to administrating reports
    """
    def test_create_by_dp(self):
        """
        Tests that creating a report by DP works
        """
        dp = mommy.make("DegreeProgram")
        rub = mommy.make("Rubric")
        self.client.post(reverse('makeReports:add-rpt-dp',kwargs={'dP':dp.pk}),{'year':2018,'rubric':rub.pk})
        num = Report.objects.filter(year=2018,degreeProgram=dp,rubric=rub.pk).count()
        self.assertEquals(num, 1)
    def test_delete(self):
        """
        Tests that reports get deleted
        """
        pk = self.rpt.pk
        self.client.post(reverse('makeReports:delete-rpt',kwargs={'pk':self.rpt.pk}))
        num = Report.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
    def test_submit(self):
        """
        Tests that the AAC can manually submit reports
        """
        rep = mommy.make("Report",submitted=False)
        self.client.post(reverse('makeReports:manual-submit-rpt',kwargs={'pk':rep.pk}),{'submitted':'on'})
        rep.refresh_from_db()
        self.assertTrue(rep.submitted)
    def test_list(self):
        """
        Tests that the report lists reports
        """
        r = mommy.make("Report",rubric__complete=False, year=int(datetime.now().year),degreeProgram__active=True)
        response= self.client.get(reverse('makeReports:report-list'))
        self.assertContains(response,r.degreeProgram.name)
        self.assertContains(response,r.year)
    def test_search(self):
        """
        Tests the search functionality
        """
        r = mommy.make("Report",submitted=False, year=2118)
        r2 = mommy.make("Report",submitted = True, year=2120)
        response = self.client.get(reverse('makeReports:search-reports')+"?year=2120&submitted=1&dP=&dept=&college=&graded=")
        self.assertContains(response,r2.degreeProgram.name)
        self.assertNotContains(response,2118)
        self.assertContains(response,2120)
class AccountAdminTests(ReportAACSetupTest):
    """
    Tests views relating to account administration
    """
    def test_create(self):
        """
        Tests the creation of new accounts
        """
        dept = mommy.make("Department")
        r = self.client.post(reverse('makeReports:make-account'),{
            'isaac':'on',
            'department':dept.pk,
            'college':dept.college.pk,
            'email':'sdkl@ksld.com',
            'username':'sldkjslkfdj',
            'password1':'slsdfdsfsdfdk',
            'password2':'slsdfdsfsdfdk',
            'first_name':'sdklfj',
            'last_name':'sdlkfjsadlkfj'
            })
        num = Profile.objects.filter(aac=True,department=dept,user__first_name='sdklfj').count()
        self.assertEquals(num,1)
    def test_list(self):
        a = mommy.make("User")
        r = self.client.get(reverse('makeReports:account-list'))
        self.assertContains(r,a.first_name)
    def test_list_search(self):
        a = mommy.make("User",first_name="aboijoie")
        b = mommy.make("User",first_name="dsasdfbwerwerqrqwejlkjljkl")
        r = self.client.get(reverse('makeReports:search-account-list')+"?f="+a.first_name+"&l="+a.last_name+"&e=")
        self.assertContains(r,a.first_name)
        self.assertNotContains(r,"dsasdfbwerwerqrqwejlkjljkl")
    def test_modify(self):
        pass
    
