from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *
import datetime

class TestUrl(SimpleTestCase):
    def test_login_is_resolved(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func, login)

    def test_logout_is_resolved(self):
        url = reverse("users:logout")
        self.assertEqual(resolve(url).func, logout)

    def test_logout_is_resolved(self):
        url = reverse("users:register")
        self.assertEqual(resolve(url).func, register)

class TestView(TestCase):
    def test_register(self):
        url = "/users/register"
        body = {
            "username": "test@gmail.com",
            "firstname": "test",
            "lastname": "test",
            "password": "test1",
            "confirm_password": "test1",
            "email": "test@gmail.com",
            "phone": "0963711479",
            "address": "test",
            "street": "test",
            "city": "test",
            "state": "test",
            "country": "test",
            "zip": "1234",
        }
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400) 

    def test_login(self):
        url = "/users/login"
        body = {"username": "admin", "password": "admin1234"}
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400) 
