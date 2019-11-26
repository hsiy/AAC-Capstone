"""
This tests views relating to the management of rubrics
"""
from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_bakery import baker
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest
class RubricMgmt(ReportAACSetupTest):
    """
    Tests relating to rubric management
    """
    def setUp(self):
        """
        Sets-up a rubric to be used for testing
        """
        super().setUp()
        self.rubric = baker.make("Rubric",name="testytesttest")
    def test_rubriclist(self):
        """
        Tests the rubric list page exists
        """
        resp = self.client.get(reverse('makeReports:rubric-list'))
        self.assertEquals(resp.status_code,200)
        self.assertContains(resp,self.rubric.name)
    def test_rubriclistsearch(self):
        """
        Tests the rubric list page returns expected results
        """
        rub2 = baker.make("Rubric",name="nonono")
        resp = self.client.get(reverse('makeReports:search-rubric-list')+"?date=&name=testytesttest")
        self.assertContains(resp,"testytesttest")
        self.assertNotContains(resp,"nonono")
    def test_rubricadd(self):
        """
        Tests adding rubric via view
        """
        resp = self.client.post(reverse('makeReports:add-rubric'),{
            'name':'test3'
        })
        num = Rubric.objects.filter(name="test3").count()
        self.assertEquals(num,1)
    def test_rubricview(self):
        """
        Tests the viewing of a rubric
        """
        rI = baker.make("RubricItem",rubricVersion=self.rubric)  
        resp = self.client.get(reverse('makeReports:view-rubric',kwargs={'pk':self.rubric.pk}))
        self.assertContains(resp,self.rubric.name)
        self.assertContains(resp,rI.text)
    def test_rubricItemAdd(self):
        """
        Tests posting to add rubric item
        """
        resp = self.client.post(reverse('makeReports:add-RI',kwargs={
            'rubric':self.rubric.pk
        }),{
            'text':'text5',
            'abbreviation':'EX',
            'section':2,
            'order':3,
            'DMEtext':'dsds',
            'MEtext':'abab',
            'EEtext':'cccs'
        })
        num = RubricItem.objects.filter(
            text='text5',
            abbreviation ='EX',
            section=2,
            order=3,
            DMEtext='dsds',
            MEtext='abab',
            EEtext='cccs'
        ).count()
        self.assertEquals(num,1)
    def test_deleteRubric(self):
        """
        Tests deleting rubrics
        """
        rub = baker.make("Rubric")
        pk = rub.pk
        rI = baker.make("RubricItem", rubricVersion = rub)
        ipk = rI.pk
        resp = self.client.post(reverse('makeReports:delete-rubric',kwargs={'pk':rub.pk}))
        num = Rubric.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
        num = RubricItem.objects.filter(pk=ipk).count()
        self.assertEquals(num,0)
    def test_updateRI(self):
        """
        Tests view to update rubric items via post
        """
        rI = baker.make("RubricItem",rubricVersion = self.rubric)
        pk = rI.pk
        resp = self.client.post(reverse('makeReports:update-RI',kwargs={'rubric':self.rubric.pk,'pk':rI.pk}),{
            'text':'text7',
            'abbreviation':'EZ',
            'section':1,
            'order':5,
            'DMEtext':'ddsds',
            'MEtext':'abaab',
            'EEtext':'cccss'
        })
        num = RubricItem.objects.filter(
            text='text7',
            abbreviation ='EZ',
            section=1,
            order=5,
            DMEtext='ddsds',
            MEtext='abaab',
            EEtext='cccss',
            pk=pk
        ).count()
        self.assertEquals(num,1)
    def test_duplicateRubric(self):
        """
        Tests duplicating a rubric
        """
        preName = self.rubric.name
        rI = baker.make("RubricItem", rubricVersion=self.rubric)
        resp = self.client.post(reverse('makeReports:dup-rub',kwargs={
            'rubric':self.rubric.pk,
        }),{
            'new_name':"newName33"
        })
        self.rubric.refresh_from_db()
        rI.refresh_from_db()
        self.assertEquals(self.rubric.name, preName)
        self.assertEquals(rI.rubricVersion,self.rubric)
        rubs = Rubric.objects.filter(name="newName33")
        self.assertEquals(rubs.count(),1)
        rub = Rubric.objects.get(name="newName33")
        num = RubricItem.objects.filter(rubricVersion=rub,text=rI.text).count()
        self.assertEquals(num, 1)
    def test_deleteRI(self):
        """
        Tests the deletion of rubric items
        """
        rI = baker.make("RubricItem", rubricVersion=self.rubric)
        pk = rI.pk
        resp = self.client.post(reverse('makeReports:delete-RI',kwargs={
            'rubric':self.rubric.pk,
            'pk':rI.pk
        }))
        num=RubricItem.objects.filter(pk=pk).count()
        self.assertEquals(num,0)



    
