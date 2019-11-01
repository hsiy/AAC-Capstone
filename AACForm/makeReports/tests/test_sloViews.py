from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
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
        self.inSLO = mommy.make("SLOInReport",report__degreeProgram=self.inDp)
        self.outSLO = mommy.make("SLOInReport", report__year=self.rpt.year)
    def test_view(self):
        response = self.client.get(reverse('makeReports:import-slo',kwargs={"report":self.rpt.pk})+"?dp="+str(self.dP.pk)+"&year="+str(self.rpt.year))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"SLO")
        self.assertContains(response,self.inSLO.goalText)
        self.assertNotContains(response,self.outSLO.goalText)
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
        self.

