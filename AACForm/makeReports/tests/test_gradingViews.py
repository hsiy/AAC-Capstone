"""
Tests relating to the grading views
"""
from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from makeReports.choices import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_bakery import baker
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest, getWithReport, postWithReport
from datetime import datetime, date, timedelta
from django.core.files import File
class GradingSectionsTest(ReportAACSetupTest):
    """
    Tests that grading sections works as expected
    """
    def setUp(self):
        """
        Sets-up a rubric and rubric item in each section
        """
        super().setUp()
        self.r = baker.make("Rubric")
        self.rub = baker.make("GradedRubric",rubricVersion=self.r)
        self.rInG = baker.make("RubricItem",rubricVersion=self.r,section=1)
        self.rInG2 = baker.make("RubricItem",rubricVersion=self.r,section=2)
        self.rInG3 = baker.make("RubricItem",rubricVersion=self.r,section=3)
        self.rInG4 = baker.make("RubricItem",rubricVersion=self.r,section=4)
        self.rI = baker.make("GradedRubricItem", rubric=self.rub, item=self.rInG)
        self.rI2 = baker.make("GradedRubricItem", rubric=self.rub, item=self.rInG2)
        self.rI3 = baker.make("GradedRubricItem", rubric=self.rub, item=self.rInG3)
        self.rI4 = baker.make("GradedRubricItem", rubric=self.rub, item=self.rInG4)
        self.rpt.rubric = self.rub
        self.rpt.save()
    def test_entry(self):
        """
        Tests the grading entry page exists
        """
        resp = self.client.get(reverse('makeReports:grade-entry',kwargs={
            'report':self.rpt.pk
        }))
        self.assertEquals(resp.status_code,200)
    def test_sec1_get(self):
        """
        Tests that the section 1 grading page works as expected
        """
        resp = self.client.get(reverse('makeReports:grade-sec1',kwargs={'report':self.rpt.pk}))
        self.assertContains(resp,self.rI.item.text)
        self.assertContains(resp,self.rI.item.DMEtext)
        self.assertContains(resp,self.rI.item.MEtext)
        self.assertContains(resp,self.rI.item.EEtext)
    def test_sec1_post(self):
        """
        Tests that the section 1 grading page works as expected when posting grade
        """
        fieldName = 'rI'+str(self.rInG.pk)
        resp = self.client.post(reverse('makeReports:grade-sec1',kwargs={'report':self.rpt.pk}),{
            fieldName:"ME",
            'section_comment':'fsfkjllaskdfls'
        })
        self.rI.refresh_from_db()
        self.rub.refresh_from_db()
        self.assertEquals(self.rI.grade,"ME")
        self.assertEquals(self.rub.section1Comment,'fsfkjllaskdfls')
        
    def test_sec2_get(self):
        """
        Tests that the section 2 grading page works as expected
        """
        resp = self.client.get(reverse('makeReports:grade-sec2',kwargs={'report':self.rpt.pk}))
        self.assertContains(resp,self.rI2.item.text)
        self.assertContains(resp,self.rI2.item.DMEtext)
        self.assertContains(resp,self.rI2.item.MEtext)
        self.assertContains(resp,self.rI2.item.EEtext)
    def test_sec2_post(self):
        """
        Tests that the section 2 grading page works as expected when posting grade
        """
        fieldName = 'rI'+str(self.rInG2.pk)
        resp = self.client.post(reverse('makeReports:grade-sec2',kwargs={'report':self.rpt.pk}),{
            fieldName:"DNM",
            'section_comment':'fsfkjllaskdfls2'
        })
        self.rI2.refresh_from_db()
        self.rub.refresh_from_db()
        self.assertEquals(self.rI2.grade,"DNM")
        self.assertEquals(self.rub.section2Comment,'fsfkjllaskdfls2')
    def test_sec3_get(self):
        """
        Tests that the section 1 grading page works as expected
        """
        resp = self.client.get(reverse('makeReports:grade-sec3',kwargs={'report':self.rpt.pk}))
        self.assertContains(resp,self.rI3.item.text)
        self.assertContains(resp,self.rI3.item.DMEtext)
        self.assertContains(resp,self.rI3.item.MEtext)
        self.assertContains(resp,self.rI3.item.EEtext)
    def test_sec3_post(self):
        """
        Tests that the section 3 grading page works as expected when posting grade
        """
        fieldName = 'rI'+str(self.rInG3.pk)
        resp = self.client.post(reverse('makeReports:grade-sec3',kwargs={'report':self.rpt.pk}),{
            fieldName: "MC",
            'section_comment':'fsfkjllaskdfls3'
        })
        self.rI3.refresh_from_db()
        self.rub.refresh_from_db()
        self.assertEquals(self.rI3.grade,"MC")
        self.assertEquals(self.rub.section3Comment,'fsfkjllaskdfls3')
    def test_sec4_get(self):
        """
        Tests that the section 1 grading page works as expected
        """
        resp = self.client.get(reverse('makeReports:grade-sec4',kwargs={'report':self.rpt.pk}))
        self.assertContains(resp,self.rI4.item.text)
        self.assertContains(resp,self.rI4.item.DMEtext)
        self.assertContains(resp,self.rI4.item.MEtext)
        self.assertContains(resp,self.rI4.item.EEtext)
    def test_sec4_post(self):
        """
        Tests that the section 4 grading page works as expected when posting grade
        """
        fieldName = 'rI'+str(self.rInG4.pk)
        resp = self.client.post(reverse('makeReports:grade-sec4',kwargs={'report':self.rpt.pk}),{
            fieldName:"ME",
            'section_comment':'fsfkjllaskdfls4'
        })
        self.rI4.refresh_from_db()
        self.rub.refresh_from_db()
        self.assertEquals(self.rI4.grade,"ME")
        self.assertEquals(self.rub.section4Comment,'fsfkjllaskdfls4')
    def test_comment(self):
        """
        Tests that the overall comment posts to the database as expected
        """
        rub = baker.make("GradedRubric")
        self.rpt.rubric = rub
        self.rpt.save()
        self.rpt.refresh_from_db()
        r = self.client.post(reverse('makeReports:grade-comment',kwargs={'report':self.rpt.pk}),{
            'text':'comm test'
        })
        self.assertEquals(self.rpt.rubric.generalComment,'comm test')
    def test_review_get(self):
        """
        Ensures that the the grading preview page exists
        """
        r = self.client.get(reverse('makeReports:rub-review',kwargs={
            'report':self.rpt.pk
        }))
        self.assertEquals(r.status_code,200)

