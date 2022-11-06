from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
# Create your tests here.
from .views import *


class TestUrl(SimpleTestCase):
    def test_dashboard(self):
        url = reverse("manager:dashboard")
        self.assertEqual(resolve(url).func, index)


class TestViews(TestCase):
    def setUp(self):
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
