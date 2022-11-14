from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import *
# Create your tests here.


class TestUrl(SimpleTestCase):
    def setUp(self):
        self.urls = {
            "dashboard": reverse("manager:dashboard")
        }

    def test_dashboard(self):
        self.assertEqual(resolve(self.urls['dashboard']).func, index)


class TestViews(TestCase):
    def setUp(self):
        self.urls = {
            "dashboard": reverse("manager:dashboard")
        }
        self.client = Client()

        # initial account
        account1 = {
            'username': "admin",
            'password': "admin",
            'email': "admin@gmail.com",
            'first_name': "AdminNaja",
            'last_name': "LastnameAdmin"
        }

        self.new_user = User.objects.create_superuser(**account1)

    def test_dashboard(self):
        response_fail = self.client.get(self.urls['dashboard'])
        self.assertEqual(response_fail.status_code, 302)  # require login
        self.client.login(username="admin", password="admin")
    #     response = self.client.get(self.urls["dashboard"])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "manager/dashboard.html")
