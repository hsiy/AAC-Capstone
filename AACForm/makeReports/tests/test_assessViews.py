from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from makeReports.forms import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest

class AssessmentSummaryPageTest(ReportSetupTest):
    """
    Tests Assessment summary page
    """
    def setUp(self):
        """
        Sets up assessments to be on the page
        """
        super(AssessmentSummaryPageTest,self).setUp()
        self.assess = mommy.make("AssessmentVersion",report=self.rpt)
        self.assess2 = mommy.make("AssessmentVersion",report=self.rpt)
        self.assessNotInRpt = mommy.make("AssessmentVersion")
    def test_view(self):
        """
        Test view exists with assessments on it
        """
        response = self.client.get(reverse('makeReports:assessment-summary',kwargs={'report':self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,self.assess.assessment.title)
        self.assertContains(response,self.assess2.assessment.title)
        self.assertNotContains(response, self.assessNotInRpt.assessment.title)
class AddNewAssessmentTest(ReportSetupTest):
    """
    Tests the Add New Assessment Page
    """
    def test_view(self):
        """
        Tests view exists
        """
        response = self.client.get(reverse('makeReports:add-assessment',kwargs={'report':self.rpt.pk}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"ssessment")
    def test_post(self):
        """
        Tests that the assessment is added
        """
        slo = mommy.make("SLOInReport", report=self.rpt)
        fD = {
            'slo': slo.pk,
            'title': 'title of assess',
            'description': 'desc things',
            'domain': "Pe",
            'domain': 'Pr',
            'directMeasure':True,
            'finalTerm':True,
            'where': 'a place',
            'allStudents': True,
            'sampleDescription':'dsd',
            'frequencyChoice': FREQUENCY_CHOICES[0][0],
            'frequency':'freq desc',
            'threshold':'thresholding',
            'target':34
        }
        response = self.client.post(reverse('makeReports:add-assessment',kwargs={'report':self.rpt.pk}),fD)
        num = AssessmentVersion.objects.filter(
            slo=slo,
            # assessment__title='title of assess',
            # description='desc things',
            # where = 'a place',
            # sampleDescription = 'dsd',
            # frequencyChoice = FREQUENCY_CHOICES[0][0],
            # frequency = 'freq desc',
            # threshold ='thresholding',
            # target = 34
            ).count()
        self.assertGreaterEqual(num,1)
class ImportAssessmentPage(ReportSetupTest):
    """
    Tests the import assessment page
    """
    def setUp(self):
        """
        Creates an assessment to import and SLO to import to
        """
        super(ImportAssessmentPage,self).setUp()
        self.slo = mommy.make("SLOInReport",report=self.rpt)
        self.rpt2 = mommy.make("Report", degreeProgram=self.rpt.degreeProgram,year=2019)
        self.slo2 = mommy.make("SLOInReport",report=self.rpt2)
        self.assess = mommy.make("AssessmentVersion",slo=self.slo2,report=self.rpt2)
    def test_view(self):
        """
        Test that the page exists
        """
        response = self.client.get(reverse('makeReports:import-assessment',kwargs={'report':self.rpt.pk})+"?year=2019&dp="+str(self.slo2.report.degreeProgram.pk)+"&slo="+str(self.slo2.pk))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"mport")
    def test_post(self):
        """
        Tests that posting data imports assessment
        """
        fD = {
            'assessment': self.assess.pk,
            'slo': self.slo.pk
        }
        response = self.client.post(reverse('makeReports:import-assessment',kwargs={'report':self.rpt.pk})+"?year=2019&dp="+str(self.slo2.report.degreeProgram.pk)+"&slo="+str(self.slo2.pk),fD)
        num = AssessmentVersion.objects.filter(report=self.rpt).count()
        self.assertGreaterEqual(num, 1)
        
