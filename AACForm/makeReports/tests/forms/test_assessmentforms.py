"""
This tests the assessment forms work as expected
"""
from django.test import TestCase
from django.urls import reverse
from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
from model_bakery import baker
from django import forms
from makeReports.forms import *
from datetime import datetime

class AssessmentFormTests(TestCase):
    """
    Tests that assessment forms work as expected
    """
    def test_create_new_valid(self):
        """
        Tests that CreateNewAssessment properly accepts valid data
        """
        slo = baker.make("SLOInReport")
        f = CreateNewAssessment({
            'slo':slo.pk,
            'title':'dslkfj sdlkf',
            'description':'ldkfjsdlkfj fasldkfj slfjsadl',
            'domain':["Pe"],
            'directMeasure':True,
            'finalTerm':False,
            'where':'kldsfj',
            'allStudents':True,
            'sampleDescription':'lksfdj flksdjf lsdklfj',
            'frequencyChoice': FREQUENCY_CHOICES[0][0],
            'frequency':'lksdjf',
            'threshold':'sldkfj',
            'target':93
        },sloQS=SLOInReport.objects.all())
        print(f.errors)
        self.assertTrue(f.is_valid())
        
    def test_create_new_invalid(self):
        """
        Tests that CreateNewAssessment reject when not all fields are present
        """
        slo = baker.make("SLOInReport")
        f = CreateNewAssessment({
            'slo':slo.pk,
            'domain':["Pe"],
            'directMeasure':True,
            'finalTerm':False,
            'where':'kldsfj',
            'allStudents':True,
            'sampleDescription':'lksfdj flksdjf lsdklfj',
            'frequencyChoice': FREQUENCY_CHOICES[0][0],
            'frequency':'lksdjf',
            'target':93
        },sloQS=SLOInReport.objects.all()
        )
        self.assertFalse(f.is_valid())
    def test_import_form(self):
        """
        Tests the ImportAssessmentForm takes valid data
        """
        a = baker.make("AssessmentVersion")
        s = baker.make("SLOInReport")
        f = ImportAssessmentForm({
            'assessment':[a.pk],
            'slo':s.pk
        },assessChoices=AssessmentVersion.objects.all(),
            slos=SLOInReport.objects.all()
        )
        print(f.errors)
        self.assertTrue(f.is_valid())
    def test_import_form_invalid(self):
        """
        Tests the ImportAssessmentForm rejects when assessment is not in the QuerySet
        """
        a = baker.make("AssessmentVersion")
        baker.make("AssessmentVersion")
        s = baker.make("SLOInReport")
        f = ImportAssessmentForm({
            'assessment':[a.pk],
            'slo':s.pk
        },assessChoices=AssessmentVersion.objects.all().exclude(pk=a.pk),
            slos=SLOInReport.objects.all()
        )
        self.assertFalse(f.is_valid())
    
