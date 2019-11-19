"""
Tests relating to the Assessment Views
"""
from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from makeReports.forms import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_mommy import mommy
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest, getWithReport, postWithReport

class AssessmentSummaryPageTest(ReportSetupTest):
    """
    Tests Assessment summary page and comment page
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
    def test_comment_page(self):
        response = getWithReport('assessment-comment',self,{},"")
        self.assertEquals(response.status_code,200)
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

class EditAssessmentTest(ReportSetupTest):
    """
    Tests the edit and delete assessment pages
    """
    def setUp(self):
        """
        Sets up assessments to edit
        """
        super(EditAssessmentTest,self).setUp()
        self.assessN = mommy.make("AssessmentVersion",report=self.rpt, assessment__numberOfUses=1)
        self.shareAssess = mommy.make("Assessment", numberOfUses = 2)
        self.assessO = mommy.make("AssessmentVersion",report=self.rpt, assessment=self.shareAssess)
        self.assessO2 = mommy.make("AssessmentVersion",report=self.rpt, assessment=self.shareAssess)
    def test_view_new(self):
        """
        Tests that the edit new assessment page exists
        """
        response = getWithReport('edit-new-assessment',self,{'assessIR':self.assessN.pk},"")
        self.assertEquals(response.status_code,200)
    def test_view_old(self):
        """
        Tests that the edit imported assessment page exists
        """
        response = getWithReport('edit-impt-assessment',self,{'assessIR':self.assessO.pk},"")
        self.assertEquals(response.status_code,200)
    def test_post_new(self):
        """
        Tests that posting information to the edit new assessment page work
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
        response = postWithReport('edit-new-assessment',self,{'assessIR':self.assessN.pk},"",fD)
        self.assessN.refresh_from_db()
        self.assertEquals(self.assessN.assessment.title, 'title of assess')
        self.assertEquals(self.assessN.target,34)
    def test_post_impt_fails(self):
        """
        Tests that posting too much information to the edit imported assessment page fails
        """
        slo = mommy.make("SLOInReport", report=self.rpt)
        fD = {
            'slo': slo.pk,
            'title': 'title of assess23',
            'description': 'desc things',
            'domain': "Pe",
            'domain': 'Pr',
            'directMeasure':True,
            'finalTerm':True,
            'where': 'a place',
            'allStudents': True,
            'sampleDescription':'dsd',
            'frequencyChoice': FREQUENCY_CHOICES[0][0],
            'frequency':'freq desc66',
            'threshold':'thresholding',
            'target':34
        }
        response = postWithReport('edit-impt-assessment',self,{'assessIR':self.assessO.pk},"",fD)
        self.assessO.refresh_from_db()
        self.assertNotEquals(self.assessO.assessment.title, 'title of assess23s')
    def test_post_impt(self):
        """
        Tests that posting the correct information to the edit imported assessment page works
        """
        slo = mommy.make("SLOInReport", report=self.rpt)
        fD = {
            'slo': slo.pk,
            'description': 'desc things',
            'finalTerm':True,
            'where': 'a place',
            'allStudents': True,
            'sampleDescription':'dsd',
            'frequencyChoice': FREQUENCY_CHOICES[0][0],
            'frequency':'freq desc',
            'threshold':'thresholding',
            'target':34
        }
        response = postWithReport('edit-impt-assessment',self,{'assessIR':self.assessO.pk},"",fD)
        self.assessO.refresh_from_db()
        self.assertEquals(self.assessO.frequency, 'freq desc')
    def test_delete_new(self):
        """
        Tests that deleting a new assessment deletes the in-report and overarching version
        """
        pk = self.assessN.pk
        aPk = self.assessN.assessment.pk
        self.assessN.slo.numberOfAssess = 1
        self.assessN.slo.save()
        response = postWithReport('delete-new-assessment',self,{'pk':self.assessN.pk},"",{})
        num = AssessmentVersion.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
        num = Assessment.objects.filter(pk=aPk).count()
        self.assertEquals(num,0)
    def test_delete_old(self):
        """
        Tests that deleting an imported assessment deletes only the in-report version
        """
        pk = self.assessO.pk
        aPk = self.assessO.assessment.pk
        self.assessO.slo.numberOfAssess = 1
        self.assessO.slo.save()
        response = postWithReport('delete-impt-assessment',self,{'pk':self.assessO.pk},"",{})
        num = AssessmentVersion.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
        num = Assessment.objects.filter(pk=aPk).count()
        self.assertEquals(num,1)
class AssessmentSupplementTest(ReportSetupTest):
    """
    Tests that supplement pages all exist
    """
    def setUp(self):
        """
        Creates an assessment and supplement
        """
        super(AssessmentSupplementTest,self).setUp()
        self.a = mommy.make("AssessmentVersion", report=self.rpt)
        self.a2 = mommy.make("AssessmentVersion",report=self.rpt)
        self.sup = mommy.make("AssessmentSupplement")
        self.a.supplements.add(self.sup)
        self.sup2 = mommy.make("AssessmentSupplement")
        self.a2.supplements.add(self.sup2)

    def test_upload(self):
        """
        Checks that the upload assessment page exists
        """
        response = getWithReport('assessment-supplement-upload',self,{'assessIR':self.a.pk},"")
        self.assertEquals(response.status_code,200)
    def test_import(self):
        """
        Checks that the import supplement page exists
        """
        response = getWithReport('assessment-supplement-import',self, {'assessIR':self.a.pk},"?year="+str(self.rpt.year)+"&dp="+str(self.rpt.degreeProgram.pk))
        self.assertEquals(response.status_code,200)
    def test_delete(self):
        """
        Checks that the delete supplement page exists
        """
        response = getWithReport('delete-supplement',self,{'assessIR':self.a.pk,'pk':self.sup.pk},"")
        self.assertEquals(response.status_code,200)
    def test_delete_post(self):
        """
        Checks that posting to delete works
        """
        pk = self.sup.pk
        response = postWithReport('delete-supplement',self,{'assessIR':self.a.pk,'pk':self.sup.pk},"", {})
        num = AssessmentSupplement.objects.filter(pk=pk).count()
        self.assertEquals(num,0)
    




        
