"""
This file contains tests to verify that all PDF views exist without error.
"""
from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest
from makeReports.choices import *

class TestingPDFs(ReportAACSetupTest):
    """
    Class containing tests relating to the generation of PDFs
    """
    def test_GradedRubricPDF(self):
        """
        Tests the graded rubric PDf page exists
        """
        rub = mommy.make("GradedRubric")
        rI = mommy.make("GradedRubricItem",rubric=rub)
        self.rpt.rubric = rub
        self.rpt.save()
        resp = self.client.get(reverse('makeReports:graded-rub-pdf',kwargs={
            'report': self.rpt.pk
        }))
        self.assertEquals(resp.status_code,200)
    def test_ReportPDFGen(self):
        """
        Tests that the report PDF without supplements page exists
        """
        resp = self.client.get(reverse('makeReports:report-pdf-no-sups',kwargs={
            'report':self.rpt.pk
        }))
        self.assertEquals(resp.status_code,200)
    def test_reportPDFwithSups(self):
        """
        Tests that the report PDF with supplements exists
        """
        resp = self.client.get(reverse('makeReports:report-pdf',kwargs={
            'report':self.rpt.pk
        }))
        self.assertEquals(resp.status_code,200)
    def test_ungradedRubricPDF(self):
        """
        Tests the the ungraded rubric generation page exists
        """
        rub = mommy.make("Rubric")
        rI = mommy.make("RubricItem", rubricVersion=rub)
        resp = self.client.get(reverse('makeReports:rubric-auto-pdf',kwargs={
            'rubric':rub.pk
        }))

