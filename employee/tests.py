from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *
import datetime

class TestUrl(SimpleTestCase):
    def test_index_is_resolved(self):
        url = reverse("employee:index")
        self.assertEqual(resolve(url).func, index)

    #def test_reserve_is_resolved(self):
    #    url = reverse("employee:assign")
    #    self.assertEqual(resolve(url).func, assign)

    #def test_create_reserve_is_resolved(self):
    #    url = reverse("employee:submit")
    #    self.assertEqual(resolve(url).func, submit)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = 'newuser'
        self.password = 'newuserpass'
        self.email = 'newuser@dormtown.com'
        self.first = 'New'
        self.last = 'User'
        self.credentials = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first,
            'last_name': self.last }
        self.new_user = User.objects.create_user(**self.credentials)

        self.index_url = reverse('employee:index')
        self.assign_url = reverse('employee:assign')
        self.submit_url = reverse('employee:submit')
        
    def test_index(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/index.html')
    
    def test_assign(self):
        response = self.client.get(self.assign_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/assign.html')
    
    def test_submit(self):
        response = self.client.get(self.submit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/submit.html')
