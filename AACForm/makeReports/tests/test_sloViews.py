from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from makeReports.choices import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest

class SLOSummaryGRTest(ReportSetupTest):
    """
    Tests the SLO summary page for graduate programs
    """
    def setUp(self):
        """
        Setups an SLO in the current report
        """
        super(SLOSummaryGRTest,self).setUp()
        self.rpt.degreeProgram.level = "GR"
        self.rpt.degreeProgram.save()
        self.slo = mommy.make('SLOInReport', make_m2m=True, report=self.rpt)
        self.slo2 = mommy.make('SLOInReport',make_m2m=True, report=self.rpt)
    def test_view(self):
        """
        Tests response code and existence of SLO
        """
        response = self.client.get(reverse('makeReports:slo-summary',kwargs={'report':self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertContains(response, self.slo.goalText)
        self.assertContains(response, self.slo2.goalText)
        for gg in self.slo.slo.gradGoals.all():
            self.assertContains(response, gg.text)
        for gg in self.slo2.slo.gradGoals.all():
            self.assertContains(response, gg.text)
class SLOSummaryUGTest(ReportSetupTest):
    """
    Tests SLO summary page for undergraduate programs
    """
    def setUp(self):
        """
        Setups an SLO in the current report
        """
        super(SLOSummaryUGTest,self).setUp()
        self.rpt.degreeProgram.level = "UG"
        self.rpt.degreeProgram.save()
        self.slo = mommy.make('SLOInReport', make_m2m=False, report=self.rpt)
        self.slo2 = mommy.make('SLOInReport',make_m2m=False, report=self.rpt)
    def test_view(self):
        """
        Tests response code and existence of SLO
        """
        response = self.client.get(reverse('makeReports:slo-summary',kwargs={'report':self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertContains(response, self.slo.goalText)
        self.assertContains(response, self.slo2.goalText)
        self.assertNotContains(response,"Grad")
class AddSLOGRTestPage(ReportSetupTest):
    """
    Tests add SLO page exists for graduate programs
    """
    def setUp(self):
        """
        Sets level of program of report
        """
        super(AddSLOGRTestPage,self).setUp()
        self.rpt.degreeProgram.level="GR"
        self.rpt.degreeProgram.save()
    def test_view(self):
        """
        Tests response and basic expected text
        """
        response = self.client.get(reverse('makeReports:add-slo',kwargs={'report':self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertContains(response,"Bloom")
        self.assertContains(response,"Graduate")
    def test_post(self):
        """
        Tests post creates SLO
        """
        form_data = {
            'goaltext':'text of slo',
            'blooms': BLOOMS_CHOICES[1]
        }
        response = self.client.post(reverse('makeReports:add-slo',kwargs={'report':self.rpt.pk}),form_data)
        s = SLOInReport.objects.filter(goalText='text of slo').count()
        self.assertTrue(s)
class AddSLOUGTestPage(ReportSetupTest):
    """
    Test add SLO page exists for undergraduate programs
    """
    def setUp(self):
        """
        Sets level of program of report
        """
        super(AddSLOUGTestPage,self).setUp()
        self.rpt.degreeProgram.level ="UG"
        self.rpt.degreeProgram.save()
    def test_view(self):
        """
        Tests response and basic expected text
        """
        response = self.client.get(reverse('makeReports:add-slo',kwargs={'report':self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertContains(response,"Bloom")
        self.assertNotContains(response,"Graduate")
    def test_post(self):
        """
        Tests post creates SLO
        """
        form_data = {
            'goaltext':'text of slo2',
            'blooms': BLOOMS_CHOICES[1]
        }
        response = self.client.post(reverse('makeReports:add-slo',kwargs={'report':self.rpt.pk}),form_data)
        s = SLOInReport.objects.filter(goalText='text of slo2').count()
        self.assertTrue(s)
class ImportSLOTestPage(ReportSetupTest):
    """
    Test import SLO page exists
    """
    def setUp(self):
        """
        Creates SLO within and out of the department
        """
        super(ImportSLOTestPage,self).setUp()
        self.inDp = mommy.make('DegreeProgram',department=self.dept)
        self.inSLO = mommy.make("SLOInReport",report__degreeProgram=self.inDp, report__year=self.rpt.year)
        self.outSLO = mommy.make("SLOInReport", report__year=self.rpt.year)
    def test_view(self):
        """
        Tests response and that expected SLO shows up from search
        """
        response = self.client.get(reverse('makeReports:import-slo',kwargs={"report":self.rpt.pk})+"?dp="+str(self.inDp.pk)+"&year="+str(self.rpt.year))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertContains(response,self.inSLO.goalText)
        self.assertNotContains(response,self.outSLO.goalText)
    def test_post(self):
        """
        Tests that the import posts
        """
        num = self.rpt.numberOfSLOs
        response = self.client.post(reverse('makeReports:import-slo',kwargs={"report":self.rpt.pk})+"?dp="+str(self.inDp.pk)+"&year="+str(self.rpt.year))
        self.assertEquals(num+1,self.rpt.numberOfSLOs)
class EditNewSLOPageTest(ReportSetupTest):
    """
    Tests edit new SLO page
    """
    def setUp(self):
        """
        Creates new SLO
        """
        super(EditNewSLOPageTest,self).setUp()
        self.slo = mommy.make("SLOInReport",slo__numberOfUses=1)
    def test_view(self):
        """
        Tests response and basic expected text
        """
        response = self.client.get(reverse('makeReports:edit-new-slo',kwargs={'report':self.rpt.pk,'sloIR':self.slo.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertContains(response,"Bloom")
class EditImptedSLOPageTest(ReportSetupTest):
    """
    Tests edit imported SLO page
    """
    def setUp(self):
        """
        Creates new SLO
        """
        super(EditImptedSLOPageTest,self).setUp()
        self.slo = mommy.make("SLOInReport",slo__numberOfUses=3)
    def test_view(self):
        """
        Tests response and basic expected text
        """
        response = self.client.get(reverse('makeReports:edit-impt-slo',kwargs={'report':self.rpt.pk,'sloIR':self.slo.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertNotContains(response,"Bloom")
        self.assertNotContains(response,"Graduate Goal")
class SLOStakeholderTest(ReportSetupTest):
    """
    Tests SLO stakeholder page
    """
    def test_view(self):
        """
        Tests response and basic expected text
        """
        response = self.client.get(reverse('makeReports:slo-stakeholders',kwargs={"report":self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"Stakeholder")
class SLOStakeImportTest(ReportSetupTest):
    """
    Tests SLO stakeholder communication import page
    """
    def setUp(self):
        """
        Create stakeholder to check importing
        """
        super(SLOStakeImportTest,self).setUp()
        self.dPI = mommy.make('DegreeProgram',department=self.dept)
        self.stkToImpt = mommy.make('SLOsToStakeholder',report__degreeProgram=self.dPI, report__year=self.rpt.year)
        self.stkNotImpt = mommy.make("SLOsToStakeholder",report__degreeProgram=self.dPI,report__year=self.rpt.year-1)
        dept2 = mommy.make("Department")
        self.stkNotImpt2 = mommy.make("SLOsToStakeholder",report__degreeProgram__department=dept2,report__year=self.rpt.year)
    def test_view(self):
        """
        Tests response code and that the stakeholder to import was found
        """
        response = self.client.get(str(reverse('makeReports:slo-stk-import',kwargs={"report":self.rpt.pk}))+"?dp="+str(self.dPI.pk)+"&year="+str(self.rpt.year))
        self.assertEquals(response.status_code,200)
        self.assertContains(response, "takeholder")
        self.assertContains(response, self.stkToImpt.text)
        self.assertNotContains(response, self.stkNotImpt.text)
        self.assertNotContains(response, self.stkNotImpt2.text)    
class SLOCommentTest(ReportSetupTest):
    """
    Test SLO section comment page
    """
    def test_view(self):
        """
        Tests response code
        """
        response = self.client.get(reverse('makeReports:slo-comment',kwargs={"report":self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"omment")
class DeleteNewSLOPageTest(ReportSetupTest):
    """
    Tests the delete SLO page
    """
    def setUp(self):
        """
        Creates an SLO to delete
        """
        super(DeleteNewSLOPageTest,self).setUp()
        self.sSLO = mommy.make("SLO",numberOfUses=1)
        self.slo = mommy.make("SLOInReport",report=self.rpt, slo=self.sSLO)
    def test_view(self):
        """
        Checks the page exists
        """
        pk = self.slo.pk
        SLOpk = self.slo.slo.pk
        response = self.client.get(reverse('makeReports:delete-new-slo',kwargs={'report':self.rpt.pk,'pk':self.slo.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
class DeleteImportedSLOPageTest(ReportSetupTest):
    """
    Tests the delete imported SLO page
    """
    def setUp(self):
        """
        Creates pyan SLO to delete
        """
        super(DeleteImportedSLOPageTest,self).setUp()
        self.rpt.numberOfSLOs = 3
        self.rpt.save()
        self.sSLO = mommy.make("SLO",numberOfUses=3)
        self.slo = mommy.make("SLOInReport",report=self.rpt, slo=self.sSLO)
    def test_view(self):
        """
        Checks page exists
        """
        response = self.client.get(reverse('makeReports:delete-impt-slo',kwargs={'report':self.rpt.pk,'pk':self.slo.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
    def test_post(self):
        """
        Tests delete posts
        """
        pk = self.slo.pk
        response = self.client.post(reverse('makeReports:delete-impt-slo',kwargs={'report':self.rpt.pk,'pk':pk}),follow=True)
        self.assertRaises(SLOInReport.DoesNotExist, SLOInReport.objects.get,pk=pk)
