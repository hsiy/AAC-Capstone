"""
Tests relating to the AAC administration of the website views
"""
from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from makeReports.choices import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest, getWithReport, postWithReport
from datetime import datetime, date, timedelta
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
    def test_arc_cols(self):
        """
        Tests that the archived college page contains only archived colleges
        """
        c1 = mommy.make("College",active=True)
        c2 = mommy.make("College",active=False)
        r = self.client.get(reverse('makeReports:arc-colleges'))
        self.assertNotContains(r,c1.name)
        self.assertContains(r,c2.name)
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
    def test_arc_depts(self):
        """
        Tests that the archived department lists contains only inactive departments
        """
        d1 = mommy.make("Department",active=True)
        d2 = mommy.make("Department",active=False)
        r = self.client.get(reverse('makeReports:arc-depts'))
        self.assertContains(r,d2.name)
        self.assertNotContains(r,d1.name)
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
    def test_arc_dps(self):
        """
        Tests that the archived degree program page contains only archived programs
        """
        dept = mommy.make("Department")
        dept2 = mommy.make("Department")
        dp = mommy.make("DegreeProgram",active=True,department=dept)
        dp2 = mommy.make("DegreeProgram",active=False,department=dept)
        dp3 = mommy.make("DegreeProgram",active=False,department=dept2)
        r = self.client.get(reverse('makeReports:arc-dps',kwargs={'dept':dept.pk}))
        self.assertContains(r,dp2.name)
        self.assertNotContains(r,dp.name)
        self.assertNotContains(r,dp3.name)
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
        num = Report.objects.filter(year=2018,degreeProgram=dp).count()
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
    def test_success(self):
        """
        Ensures that the rubric success page exists
        """
        r = self.client.get(reverse('makeReports:gen-rpt-suc'))
        self.assertEquals(r.status_code,200)
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
        """
        Tests the account list
        """
        a = mommy.make("User")
        r = self.client.get(reverse('makeReports:account-list'))
        self.assertContains(r,a.first_name)
    def test_list_search(self):
        """
        Tests the acount list acts as expected
        """
        a = mommy.make("User",first_name="aboijoie")
        b = mommy.make("User",first_name="dsasdfbwerwerqrqwejlkjljkl")
        r = self.client.get(reverse('makeReports:search-account-list')+"?f="+a.first_name+"&l="+a.last_name+"&e=")
        self.assertContains(r,a.first_name)
        self.assertNotContains(r,"dsasdfbwerwerqrqwejlkjljkl")
    def test_modify(self):
        """
        Tests the AAC modifying user account page
        """
        a = mommy.make("User")
        a.profile.aac = False
        a.profile.save()
        dept = mommy.make("Department")
        fD = {
            'aac':'on',
            'department':dept.pk,
            'first_name':'changed f_name',
            'last_name':'changed l_name',
            'email':'sdlk@g.com'
        }
        r = self.client.post(reverse('makeReports:aac-modify-account',kwargs={'pk':a.pk}),fD)
        a.refresh_from_db()
        self.assertEquals(a.profile.aac,True)
        self.assertEquals(a.profile.department,dept)
        self.assertEquals(a.first_name,'changed f_name')
        self.assertEquals(a.last_name,'changed l_name')
        self.assertEquals(a.email,'sdlk@g.com')
    def test_inactivate(self):
        """
        Tests the inactivate user view
        """
        a = mommy.make("User", is_active=True)
        r = self.client.post(reverse('makeReports:inactivate-account',kwargs={'pk':a.pk}))
        a.refresh_from_db()
        self.assertEquals(a.is_active,False)
class GradGoalAdminTests(ReportAACSetupTest):
    """
    Tests views relating to graduate goal administration by the AAC
    """
    def test_list(self):
        """
        Tests the graduate goal list page contains grad goals
        """
        r1 = mommy.make("GradGoal",active=True)
        r2 = mommy.make("GradGoal",active=False)
        r = self.client.get(reverse('makeReports:gg-list'))
        self.assertContains(r,r1.text)
        self.assertNotContains(r,r2.text)
    def test_old_list(self):
        """
        Tests the archived list contains expected goals
        """
        r1 = mommy.make("GradGoal",active=True)
        r2 = mommy.make("GradGoal",active=False)
        r = self.client.get(reverse('makeReports:old-gg-list'))
        self.assertContains(r,r2.text)
        self.assertNotContains(r,r1.text)
    def test_update(self):
        """
        Tests the update function of the graduate goal
        """
        r = mommy.make("GradGoal",active=False)
        res = self.client.post(reverse('makeReports:update-gg',kwargs={'pk':r.pk}),{
            'active':'on',
            'text':'new text here'
        })
        r.refresh_from_db()
        self.assertEquals(r.active,True)
        self.assertEquals(r.text,'new text here')
    def test_add(self):
        """
        Tests that a new graduate goal can be effectively added
        """
        r = self.client.post(reverse('makeReports:add-gg'),{
            'text':'new gg text'
        })
        num = GradGoal.objects.filter(text='new gg text', active=True).count()
        self.assertEquals(num,1)
class AnnouncementsTest(ReportAACSetupTest):
    """
    Tests that announcements can be appropriately created
    """
    def test_add(self):
        """
        Tests adding an announcement
        """
        r = self.client.post(reverse('makeReports:add-announ'),{
            'text':'ann text',
            'expiration_month':2,
            'expiration_day': 17,
            'expiration_year':2020
        })
        num = Announcement.objects.filter(text='ann text',expiration=date(2020,2,17)).count()
        self.assertEquals(num,1)
    def test_list(self):
        """
        Tests the announcement listing page
        """
        an = mommy.make("Announcement", expiration=datetime.now()+timedelta(days=1))
        an2 = mommy.make("Announcement",expiration=datetime.now()-timedelta(days=2))
        r = self.client.get(reverse('makeReports:announ-list'))
        self.assertContains(r,an.text)
        self.assertContains(r,an2.text)
    def test_delete(self):
        """
        Tests that announcements can be effectively deleted
        """
        a = mommy.make("Announcement")
        pk = a.pk
        r = self.client.post(reverse('makeReports:delete-announ',kwargs={'pk':a.pk}))
        num = Announcement.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
    def test_edit(self):
        """
        Tests that the edit page effecitvely edits announcements
        """
        a = mommy.make("Announcement")
        r = self.client.post(reverse('makeReports:edit-announ',kwargs={'pk':a.pk}),{
            'text':'ann text 2',
            'expiration_month':3,
            'expiration_day': 27,
            'expiration_year':2021
        })
        a.refresh_from_db()
        self.assertEquals(a.text,'ann text 2')
        self.assertEquals(a.expiration, date(2021,3,27))
    
    

    

