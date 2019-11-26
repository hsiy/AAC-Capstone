"""
Tests the APIs work as expected
"""
from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_bakery import baker
from .test_basicViews import ReportAACSetupTest, NonAACTest, ReportSetupTest
from makeReports.choices import *

class APITesting(NonAACTest):
    """
    Contains tests that are APIs for the Javascript
    """
    def test_dept_by_col(self):
        """
        Tests that the API returns all departments within a college
        """
        col = baker.make("College")
        col2 = baker.make("College")
        dep1 = baker.make("Department",college=col)
        dep2 = baker.make("Department",college=col)
        depNo = baker.make("Department",college=col2)
        resp = self.client.get(reverse('makeReports:api-dept-by-col')+"?college="+str(col.pk))
        self.assertContains(resp,dep1.pk)
        self.assertContains(resp,dep1.name)
        self.assertContains(resp,dep2.pk)
        self.assertContains(resp,dep2.name)
        self.assertNotContains(resp,depNo.name)
    def test_SLOSuggestions(self):
        """
        Tests the SLO suggestions work as expected
        """
        resp = self.client.post(reverse('makeReports:api-slo-suggestions'),{
            'slo_text':'analyze analyze analyzing understand synthesize'
        })
        self.assertContains(resp,'Analysis')
    def test_prog_by_dept(self):
        """
        Tests the API returns programs within the department
        """
        dep = baker.make("Department")
        dep2 = baker.make("Department")
        prog = baker.make("DegreeProgram",department=dep)
        prog2 = baker.make("DegreeProgram",department=dep)
        progNo = baker.make("DegreeProgram",department=dep2)
        resp = self.client.get(reverse('makeReports:api-prog-by-dept')+"?department="+str(dep.pk))
        self.assertContains(resp,prog.name)
        self.assertContains(resp,prog.pk)
        self.assertContains(resp,prog2.name)
        self.assertContains(resp,prog2.pk)
        self.assertNotContains(resp,progNo.pk)
    def test_slo_by_dp(self):
        """
        Tests that the API returns SLOs within the degree program
        """
        dp = baker.make("DegreeProgram")
        dp2 = baker.make("DegreeProgram")
        slo = baker.make("SLOInReport",report__degreeProgram=dp, report__year=2018)
        slo2 = baker.make("SLOInReport",report__degreeProgram=dp2,report__year=2018)
        resp = self.client.get(
            reverse('makeReports:api-slo-by-dp')+"?report__degreeProgram="+str(dp.pk)+"&report__year__gte=2016&report__year__lte=2019")
        self.assertContains(resp,slo.pk)
        self.assertNotContains(resp,slo2.pk)
    def test_assess_by_slo(self):
        """
        Tests the API collects assessments within the SLO, and that the results are unique by assessment
        """
        rept = baker.make("Report",year=2018)
        r2 = baker.make("Report",year=2016)
        slo = baker.make("SLO")
        sloIR = baker.make("SLOInReport",report=rept,slo=slo)
        sloIR2 = baker.make("SLOInReport",report=r2,slo=slo)
        slo2 = baker.make("SLO")
        sloIRNo = baker.make("SLOInReport",report__year=2019,slo=slo2)
        a = baker.make("Assessment")
        assess = baker.make("AssessmentVersion",assessment=a,report=rept,slo=sloIR)
        assess2 = baker.make("AssessmentVersion",assessment=a,report=r2,slo=sloIR2)
        assessNo = baker.make("AssessmentVersion",slo=sloIRNo)
        resp = self.client.get(reverse('makeReports:api-assess-by-slo')+"?slo__slo="+str(slo.pk)+"&report__year__gte=2015&report__year__lte=2019")
        self.assertContains(resp,assess.pk)
        self.assertNotContains(resp,assess2.pk)
        self.assertNotContains(resp,assessNo.pk)
    def test_api_new_graph_1(self):
        """
        Tests the status code the new graph API for type 1
        """
        department = baker.make("Department")
        program = baker.make("DegreeProgram",department=department)
        r = baker.make("Report", degreeProgram=program, year=2017)
        slo = baker.make("SLOInReport",report=r)
        assessHere = baker.make("AssessmentVersion",report=r,slo=slo)
        baker.make("AssessmentData",assessmentVersion=assessHere,overallProficient=93)
        data = {
            'report__degreeProgram__department': department.pk,
            'report__degreeProgram': program.pk,
            'report__year__gte': 2015,
            'report__year__lte': 2018,
            'decision': 1,
            'sloIR': slo.pk,
            'assess': assessHere.assessment.pk,
            'sloWeights': "{\""+str(slo.pk)+"\": 1}"
        }
        resp = self.client.post(reverse('makeReports:api-new-graph'),data)
        self.assertEquals(resp.status_code,200)
    def test_api_new_graph_2(self):
        """
        Tests the status code the new graph API for type 2
        """
        department = baker.make("Department")
        program = baker.make("DegreeProgram",department=department)
        r = baker.make("Report", degreeProgram=program, year=2018)
        slo = baker.make("SLOInReport",report=r)
        assessHere = baker.make("AssessmentVersion",report=r,slo=slo)
        baker.make("AssessmentData",assessmentVersion=assessHere,overallProficient=93)
        data = {
            'report__degreeProgram__department': department.pk,
            'report__degreeProgram': program.pk,
            'report__year__gte': 2015,
            'report__year__lte': 2018,
            'decision': 2,
            'sloIR': slo.pk,
            'assess': assessHere.assessment.pk,
            'sloWeights': "{\""+str(slo.pk)+"\": 1}"
        }
        resp = self.client.post(reverse('makeReports:api-new-graph'),data)
        self.assertEquals(resp.status_code,200)
    def test_api_new_graph_3(self):
        """
        Tests the status code the new graph API for type 3
        """
        department = baker.make("Department")
        program = baker.make("DegreeProgram",department=department)
        r = baker.make("Report", degreeProgram=program, year=2016)
        slo = baker.make("SLOInReport",report=r)
        assessHere = baker.make("AssessmentVersion",report=r,slo=slo)
        baker.make("AssessmentData",assessmentVersion=assessHere,overallProficient=93)
        data = {
            'report__degreeProgram__department': department.pk,
            'report__degreeProgram': program.pk,
            'report__year__gte': 2015,
            'report__year__lte': 2018,
            'decision': 3,
            'sloIR': slo.pk,
            'assess': assessHere.assessment.pk,
            'sloWeights': "{\""+str(slo.pk)+"\": 1}"
        }
        resp = self.client.post(reverse('makeReports:api-new-graph'),data)
        self.assertEquals(resp.status_code,200)
    #Bloom's suggestion API is not done yet, so no tests for it
    



