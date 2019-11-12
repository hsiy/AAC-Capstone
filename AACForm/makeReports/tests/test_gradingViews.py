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
from django.core.files import File
class GradingSectionsTest(ReportAACSetupTest):
    """
    Tests that grading sections works as expected
    """
    def test_sec1_get(self):
        """
        Tests that the section 1 grading page works as expected
        """
        r = mommy.make("Rubric")
        rub = mommy.make("GradedRubric",rubricVersion=r)
        rInG = mommy.make("RubricItem",rubricVersion=r)
        rI = mommy.make("GradedRubricItem", rubric=rub, item=rInG)
        self.rpt.rubric = rub
        self.rpt.save()
        resp = self.client.get(reverse('makeReports:grade-sec1',kwargs={'report':self.rpt.pk}))
        self.assertContains(resp,rI.item.text)
        self.assertContains(resp,rI.item.DMEtext)
        self.assertContains(resp,rI.item.MEtext)
        self.assertContains(resp,rI.item.EEtext)
        

