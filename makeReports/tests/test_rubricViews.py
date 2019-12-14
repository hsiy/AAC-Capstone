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
class RubricMgmtTest(ReportAACSetupTest):
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
        resp = self.client.get(reverse('makeReports:add-rubric'))
        resp = self.client.post(reverse('makeReports:add-rubric'),{
            'name':'test3'
        })
        self.assertEquals(resp.status_code,302)
        num = Rubric.objects.filter(name="test3").count()
        self.assertEquals(num,1)
    def test_rubricadd_name_toolong(self):
        """
        Tests adding too long of a name prevents form submission
        """
        reallyLong = "abcd"*250+"x"
        resp = self.client.post(reverse('makeReports:add-rubric'),{
            'name':reallyLong
        })
        self.assertNotEquals(resp.status_code,302)
    def test_rubricview(self):
        """
        Tests the viewing of a rubric
        """
        rI = baker.make("RubricItem",rubricVersion=self.rubric)  
        resp = self.client.get(reverse('makeReports:view-rubric',kwargs={'pk':self.rubric.pk}))
        self.assertContains(resp,self.rubric.name)
        self.assertContains(resp,rI.text)
    def test_rubricview_DNE(self):
        """
        Tests the response code from the Rubric View page when the rubric does not exist returns 404
        """
        r = self.client.get(reverse('makeReports:view-rubric',kwargs={'pk':313}))
        self.assertEquals(r.status_code,404)
    def test_rubricview_recipe(self):
        """
        Tests the viewing of rubric with item from recipe
        """
        rI = baker.make_recipe("makeReports.rubricItem",rubricVersion=self.rubric)  
        resp = self.client.get(reverse('makeReports:view-rubric',kwargs={'pk':self.rubric.pk}))
        self.assertContains(resp,self.rubric.name)
        self.assertContains(resp,rI.text) 
    def test_rubricItemAdd(self):
        """
        Tests posting to add rubric item
        """
        resp = self.client.get(reverse('makeReports:add-RI',kwargs={
            'rubric':self.rubric.pk
        }))
        self.assertEquals(resp.status_code,200)
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
        self.assertEquals(resp.status_code,302)
    def test_addRI_DNE(self):
        """
        Tests the response code from the Add Rubric Item page when the rubric does not exist returns 404
        """
        r = self.client.get(reverse('makeReports:add-RI',kwargs={
            'rubric':4191
        }))
        self.assertEquals(r.status_code,404)
    def test_rubricItemAdd_toolong(self):
        """
        Tests posting to add rubric item with too long of text fails
        """
        reallyLong = "xydksdfa I want    "*1000
        resp = self.client.post(reverse('makeReports:add-RI',kwargs={
            'rubric':self.rubric.pk
        }),{
            'text':reallyLong,
            'abbreviation':'EX',
            'section':2,
            'order':3,
            'DMEtext':'dsds',
            'MEtext':'abab',
            'EEtext':'cccs'
        })
        self.assertNotEquals(resp.status_code,302)
    def test_rubricItemAdd_missingText(self):
        """
        Tests posting to add rubric item without text fails
        """
        reallyLong = "xydksdfa I want    "*1000
        resp = self.client.post(reverse('makeReports:add-RI',kwargs={
            'rubric':self.rubric.pk
        }),{
            'abbreviation':'EX',
            'section':2,
            'order':3,
            'DMEtext':'dsds',
            'MEtext':'abab',
            'EEtext':'cccs'
        })
        self.assertNotEquals(resp.status_code,302)
    def test_deleteRubric(self):
        """
        Tests deleting rubrics
        """
        rub = baker.make("Rubric")
        pk = rub.pk
        rI = baker.make("RubricItem", rubricVersion = rub)
        ipk = rI.pk
        resp = self.client.get(reverse('makeReports:delete-rubric',kwargs={'pk':rub.pk}))
        self.assertEquals(resp.status_code,200)
        resp = self.client.post(reverse('makeReports:delete-rubric',kwargs={'pk':rub.pk}))
        num = Rubric.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
        num = RubricItem.objects.filter(pk=ipk).count()
        self.assertEquals(num,0)
    def test_addRI_DNE(self):
        """
        Tests the response code from the delete rubric page when the rubric does not exist returns 404
        """
        r = self.client.get(reverse('makeReports:delete-rubric',kwargs={
            'pk':4191
        }))
        self.assertEquals(r.status_code,404)
    def test_updateRI(self):
        """
        Tests view to update rubric items via post
        """
        rI = baker.make("RubricItem",rubricVersion = self.rubric)
        pk = rI.pk
        resp = self.client.get(reverse('makeReports:update-RI',kwargs={'rubric':self.rubric.pk,'pk':rI.pk}))
        self.assertEquals(resp.status_code,200)
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
        self.assertEquals(resp.status_code,302)
    def test_updateRI_DNE(self):
        """
        Tests the response code from the Update Rubric Item page when the rubric item does not exist returns 404
        """
        r = self.client.get(reverse('makeReports:update-RI',kwargs={
            'rubric':self.rubric.pk,
            'pk':342
        }))
        self.assertEquals(r.status_code,404)
    def test_updateRI_toolong(self):
        """
        Tests view to update rubric items via post with too long of DMEtext fails
        """
        rI = baker.make("RubricItem",rubricVersion = self.rubric)
        pk = rI.pk
        reallyLong = "text of rubric"*500
        resp = self.client.post(reverse('makeReports:update-RI',kwargs={'rubric':self.rubric.pk,'pk':rI.pk}),{
            'text':'text',
            'abbreviation':'EZ',
            'section':1,
            'order':5,
            'DMEtext': reallyLong,
            'MEtext':'abaab',
            'EEtext':'cccss'
        })
        self.assertNotEquals(resp.status_code,302)
    def test_updateRI_recipe(self):
        """
        Tests view to update rubric items via post with recipe based item
        """
        rI = baker.make_recipe("makeReports.rubricItem",rubricVersion = self.rubric)
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
        resp = self.client.get(reverse('makeReports:dup-rub',kwargs={
            'rubric':self.rubric.pk,
        }))
        self.assertEquals(resp.status_code,200)
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
        self.assertEquals(resp.status_code,302)
    def test_duplicateRub_DNE(self):
        """
        Tests the response code from the Duplicate Rubric page when the rubric does not exist returns 404
        """
        r = self.client.post(reverse('makeReports:dup-rub',kwargs={
            'rubric':433,
        }),{
            'new_name':"newName33"
        })
        self.assertEquals(r.status_code,404)
    def test_duplicateRubric_missingName(self):
        """
        Tests duplicating a rubric without a name fails
        """
        preName = self.rubric.name
        rI = baker.make("RubricItem", rubricVersion=self.rubric)
        resp = self.client.post(reverse('makeReports:dup-rub',kwargs={
            'rubric':self.rubric.pk,
        }),{
        })
        self.assertNotEquals(resp.status_code,302)
    def test_deleteRI(self):
        """
        Tests the deletion of rubric items
        """
        rI = baker.make("RubricItem", rubricVersion=self.rubric)
        pk = rI.pk
        resp = self.client.get(reverse('makeReports:delete-RI',kwargs={
            'rubric':self.rubric.pk,
            'pk':rI.pk
        }))
        self.assertEquals(resp.status_code,200)
        resp = self.client.post(reverse('makeReports:delete-RI',kwargs={
            'rubric':self.rubric.pk,
            'pk':rI.pk
        }))
        num=RubricItem.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
    def test_deleteRI_DNE(self):
        """
        Tests the response code from the Delete Rubric Item page when the rubric item does not exist returns 404
        """
        r = self.client.get(reverse('makeReports:delete-RI',kwargs={
            'rubric':self.rubric.pk,
            'pk':2553
        }))
        self.assertEquals(r.status_code,404)
    def test_deleteRI_recipe(self):
        """
        Tests the deletion of rubric items with recipe based item
        """
        rI = baker.make_recipe("makeReports.rubricItem", rubricVersion=self.rubric)
        pk = rI.pk
        resp = self.client.post(reverse('makeReports:delete-RI',kwargs={
            'rubric':self.rubric.pk,
            'pk':rI.pk
        }))
        num=RubricItem.objects.filter(pk=pk).count()
        self.assertEquals(num,0)


    
