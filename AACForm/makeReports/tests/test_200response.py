from django.test import TestCase
from django.urls import reverse

from makeReports.models import *
from unittest import mock
from django.http import HttpResponse
import requests
class BookTest(TestCase):
    def setUp(self):
        #Book.objects.create(title='Work Week', author="Gary S.")
        pass
    def test_title(self):
        #book = Book.objects.get(pk=1)
        #self.assertEquals(f'{book.title}',"Work Week")
        pass
    def test_author(self):
        #book = Book.objects.get(pk=1)
        #self.assertEquals(f'{book.author}',"Gary S.")
        pass
    def test_view(self):
        response = self.client.get(reverse('books'))
        self.assertEquals(response.status_code,200)
        #self.assertContains(response, "Work Week by Gary S.")
        #self.assertContains(response, "Cat Fact")
        #self.assertTemplateUsed(response,"books.html")