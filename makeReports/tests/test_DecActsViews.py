"""
Tests related to testing views for entering decisions and actions
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

class DecActViewsTest(ReportSetupTest):
    """
    Collects all views relating to decisions and actions
    """
    def setUp(self):
        """
        Create an SLO to input decisions/actions for
        """
        super().setUp()
        self.slo = mommy.make("SLOInReport",report=self.rpt)
    def test_summary(self):
        """
        Tests that the summary page exists
        """
        resp = self.client.get(reverse('makeReports:decisions-actions-summary',kwargs={
            'report':self.rpt.pk
        }))
        self.assertContains(resp,'SLO')
    def test_addDecAct(self):
        """
        Tests adding a decision action via posting to the view
        """
        resp = self.client.post(reverse('makeReports:add-decisions-actions',kwargs={
            'report':self.rpt.pk,
            'slopk':self.slo.pk
        }),{
            'text':'testingtestingtest'
        })
        num = DecisionsActions.objects.filter(text='testingtestingtest',SLO=self.slo.slo,sloIR=self.slo,report=self.rpt).count()
        self.assertEquals(num,1)
    def test_addDecActSLO(self):
        """
        Tests that adding a decision action from SLO page redirects to SLO page
        """
        resp = self.client.post(reverse('makeReports:add-decisions-actions-slo',kwargs={
            'report':self.rpt.pk,
            'slopk':self.slo.pk
        }),{
            'text':'testingtestingtes334t'
        })
        num = DecisionsActions.objects.filter(text='testingtestingtes334t',SLO=self.slo.slo,sloIR=self.slo,report=self.rpt).count()
        self.assertEquals(num,1)
        self.assertRedirects(resp,reverse('makeReports:slo-summary',kwargs={
            'report':self.rpt.pk
        }))
    def test_editDecAct(self):
        """
        Tests that posting to view edits the decision/action text
        """
        dA = mommy.make("DecisionsActions",SLO=self.slo.slo,sloIR=self.slo,report=self.rpt)
        resp = self.client.post(reverse('makeReports:edit-decisions-actions',kwargs={
            'report':self.rpt.pk,
            'slopk':self.slo.pk,
            'pk':dA.pk
        }),{
            'text':'testingtestingtest545'
        })
        dA.refresh_from_db()
        self.assertEquals(dA.text,'testingtestingtest545')
    def test_editDecActSLO(self):
        """
        Testing that the view edits the decision/action works and redirects as expected
        """
        dA = mommy.make("DecisionsActions",SLO=self.slo.slo,sloIR=self.slo,report=self.rpt)
        resp = self.client.post(reverse('makeReports:edit-decisions-actions-slo',kwargs={
            'report':self.rpt.pk,
            'slopk':self.slo.pk,
            'pk':dA.pk
        }),{
            'text':'testingtestingtest54576'
        })
        dA.refresh_from_db()
        self.assertEquals(dA.text,'testingtestingtest54576')
        self.assertRedirects(resp,reverse('makeReports:slo-summary',kwargs={
            'report':self.rpt.pk
        }))
    def test_addEditRedirect_add(self):
        """
        Tests the add/edit redirect redirects to add when there is not one already
        """
        slo2 = mommy.make("SLOInReport",report=self.rpt)
        resp = self.client.get(reverse('makeReports:add-edit-redirect',kwargs={
            'report':self.rpt.pk,
            'slopk':slo2.pk
        }))
        self.assertRedirects(resp,reverse('makeReports:add-decisions-actions-slo',kwargs={
            'report':self.rpt.pk,
            'slopk':slo2.pk
        }))
    def test_addEditRedirect_edit(self):
        """
        Tests the add/edit redirect redirect to edit there is already one
        """
        slo2 = mommy.make("SLOInReport",report=self.rpt)
        dA = mommy.make("DecisionsActions",SLO=slo2.slo,sloIR=slo2,report=self.rpt)
        resp = self.client.get(reverse('makeReports:add-edit-redirect',kwargs={
            'report':self.rpt.pk,
            'slopk':slo2.pk
        }))
        self.assertRedirects(resp,reverse('makeReports:edit-decisions-actions-slo',kwargs={
            'report':self.rpt.pk,
            'slopk':slo2.pk,
            'pk':dA.pk
        }))
    def test_section4comment(self):
        """
        Tests the section 4 comment works as expected when posted to
        """
        resp = self.client.post(reverse('makeReports:d-a-comment',kwargs={
            'report':self.rpt.pk
        }),{
            'text':'seccy4comment2'
        })
        self.rpt.refresh_from_db()
        self.assertEquals(self.rpt.section4Comment,'seccy4comment2')


