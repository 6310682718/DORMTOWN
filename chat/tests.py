from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import *
# Create your tests here.


class TestUrl(SimpleTestCase):
    def setUp(self):
        self.urls = {
            "index": reverse("chat:index")
        }

    # def test_chat_page(self):
    #     self.assertEqual((resolve(self.urls["index"])).func, index)


class TestViews(TestCase):
    def setUp(self):
        self.urls = {
            "index": reverse("chat:index")
        }
        self.client = Client()

        account1 = {
            'username': "admin",
            'password': "admin",
            'email': "admin@gmail.com",
            'first_name': "AdminNaja",
            'last_name': "LastnameAdmin"
        }
        self.admin_account = User.objects.create_superuser(**account1)

        account2 = {
            'username': "user1",
            'password': "user1pass",
            'email': "user@gmail.com",
            'first_name': "User1Naja",
            'last_name': "LastnameUser1"
        }
        self.user1_account = User.objects.create(**account2)

    # def test_chat_page(self):
    #     response = self.client.get(self.urls["index"])
    #     self.assertEqual(response.status_code, 200)
