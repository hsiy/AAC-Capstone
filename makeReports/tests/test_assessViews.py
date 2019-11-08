from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
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
        print(self.assess)
        self.assess2 = mommy.make("AssessmentVersion",report=self.rpt)
        self.assessNotInRpt = mommy.make("AssessmentVersion")
    def test_view(self):
        """
        Test view exists with assessments on it
        """
        response = self.client.get('makeReports:assessment-summary',kwargs={'report':self.rpt.pk})
        self.assertEquals(response.status_code,200)
        self.assertContains(response,self.assess.name)
        self.assertContains(response,self.assess2.name)
        self.assertNotContains(response, self.assessNotInRpt.name)
