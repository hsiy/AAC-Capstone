"""
This tests the grading forms work as expected
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

class RubricFormsTests(TestCase):
    """
    Tests forms related to the rubric forms
    """
    def test_section_rubric_valid(self):
        """
        Tests that SectionRubricForm accepts valid data
        """
        rI = baker.make("RubricItem")
        rI2 = baker.make("RubricItem")
        f = SectionRubricForm({
            'rI'+str(rI.pk): RUBRIC_GRADES_CHOICES[0][0],
            'rI'+str(rI2.pk): RUBRIC_GRADES_CHOICES[1][0],
            'section_comment':"KLDKFLJS"
        },rubricItems= RubricItem.objects.all())
        self.assertTrue(f.is_valid())
    def test_section_rubric_choice_failed(self):
        """
        Tests that SectionRubricForm fails when the rubric item is not one of the choices
        """
        rI = baker.make("RubricItem")
        rI2 = baker.make("RubricItem")
        f = SectionRubricForm( {
            'rI'+str(rI.pk): RUBRIC_GRADES_CHOICES[0][0],
            'rI'+str(rI2.pk): "not a valid choice",
            'section_comment':"KLDKFLJS"
        },rubricItems= RubricItem.objects.all())
        self.assertFalse(f.is_valid())
    def test_section_rubric_toolong(self):
        """
        Tests the form is invalid when the section comment is too long
        """
        rI = baker.make("RubricItem")
        rI2 = baker.make("RubricItem")
        f = SectionRubricForm({
            'rI'+str(rI.pk): RUBRIC_GRADES_CHOICES[0][0],
            'section_comment':"KLDKFLJSfskljjjdssf"*200
        },rubricItems= RubricItem.objects.all())
        self.assertFalse(f.is_valid())      
    def test_item_form_valid(self):
        """
        Tests that RubricItemForm accepts valid data
        """
        f = RubricItemForm({
            'text':'dlkfjsdlfj jflksdjflj sdjfllk',
            'abbreviation':'JK',
            'section':3,
            'order':5,
            'DMEtext':'skdlfj skldfj skdlfja s',
            'MEtext':'skdlfjsd sdklfj a',
            'EEtext':'sdkfljsd fkalsjf beab'
        })
        self.assertTrue(f.is_valid())
    def test_item_form_nonint(self):
        """
        Tests that the RubricItemForm rejects form with non-integer section
        """
        f = RubricItemForm({
            'text':'dlkfjsdlfj jflksdjflj sdjfllk',
            'abbreviation':'JK',
            'section':3.3,
            'order':5,
            'DMEtext':'skdlfj skldfj skdlfja s',
            'MEtext':'skdlfjsd sdklfj a',
            'EEtext':'sdkfljsd fkalsjf beab'
        })
        self.assertFalse(f.is_valid())
    def test_dup_rub(self):
        """
        Tests that the duplicate rubric form accepts valid data
        """
        f = DuplicateRubricForm({
            'new_name': "sldkfj sdklfj dsklfjlllaskjleiowjeo QQ@29!22"
        })
        self.assertTrue(f.is_valid())
    def test_dup_rub_toolong(self):
        """
        Tests the form rejects when the new name is too long
        """
        f = DuplicateRubricForm({
            'new_name': "sldkfj sdklfj dsklfjlllaskjleiowjeo QQ@29!22"*300
        })
        self.assertFalse(f.is_valid())
    def test_submitGrade(self):
        """
        Tests the SubmitGrade form properly takes true argument
        """
        f = SubmitGrade({
            'hidden':'a'
        },valid=True)
        self.assertTrue(f.is_valid())
    def test_submitGradeFalse(self):
        """
        Tests the SubmitGrade form properly fails when given a false argument
        """
        f = SubmitGrade({
            'hidden':''
        },valid=False)
        self.assertFalse(f.is_valid())
    def test_overallcomment(self):
        """
        Test the OverallCommentForm properly allows valid text
        """
        f = OverallCommentForm({
            'text':'kdlsfj sdlkfjjk as sdfjks dfl sdaklfwjiof jeoiw fewjfo sdf <b>skdlfj</b>'
        })
        self.assertTrue(f.is_valid())
    