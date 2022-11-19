from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from .views import *
# Create your tests here.


class TestUrl(SimpleTestCase):
    def setUp(self):
        # self up urls
        self.urls = {
            "index": reverse("chat:chat_to_admin"),
            "chat_to_user": reverse("chat:chat_to_user", args=[1]), # user id = 1
        }

    def test_chat_to_admin(self):
        # test resolve function [User chat to Admin] from url to view function
        self.assertEqual((resolve(self.urls["index"])).func, index)
 
    def test_chat_to_user(self):
        # test resolve function [Admin chat to user] from url to view function
        self.assertEqual((resolve(self.urls["chat_to_user"])).func, chat_log)




class TestViews(TestCase):
    def setUp(self):
        # Setup urls & user account & admin account
        self.urls = {
            "index": reverse("chat:chat_to_admin"),
            "chat_to_user": reverse("chat:chat_to_user", args=[1]), # user id = 1
            "chat_unknown_user": reverse("chat:chat_to_user", args=[10])
        }
        self.client = Client()

        self.account1 = {
            'username': "admin",
            'password': "admin",
            'email': "admin@gmail.com",
            'first_name': "AdminNaja",
            'last_name': "LastnameAdmin"
        }
        self.admin_account = User.objects.create_superuser(**self.account1)

        self.account2 = {
            'username': "user1",
            'password': "user1pass",
            'email': "user@gmail.com",
            'first_name': "User1Naja",
            'last_name': "LastnameUser1"
        }
        self.user1_account = User.objects.create_user(**self.account2)

    def test_chat_page_not_login(self):
        # Test no account chat to admin [ FAIL ]
        response = self.client.get(self.urls["index"])
        self.assertEqual(response.status_code, 302)
    
    def test_chat_page_login(self):
        # test user chat to account [ SUCCESS ]
        self.client.login(username=self.account2['username'], password=self.account2['password']);
        response = self.client.get(self.urls["index"])
        self.assertEqual(response.status_code, 200)

    def test_chat_admin_not_login(self):
        # test not login chat to user [ FAIL ]
        response = self.client.get(self.urls["chat_to_user"])
        self.assertEqual(response.status_code, 302)

    def test_chat_admin_login_user(self):
        # test user account chat to user [ FAIL ]
        self.client.login(username=self.account2['username'], password=self.account2['password']);
        response = self.client.get(self.urls["chat_to_user"])
        self.assertEqual(response.status_code, 302)

    def test_chat_admin_login_admin(self):
        # test admin chat to user [ SUCCESS ]
        self.client.login(username=self.account1['username'], password=self.account1['password']);
        response = self.client.get(self.urls["chat_to_user"])
        self.assertEqual(response.status_code, 200)

    def test_chat_admin_login_admin_with_user(self):
        # test admin chat to user [ SUCCESS ]
        # user send message
        chat_room = ChatRoom.objects.create(room_name="room-1")
        Message.objects.create(room=chat_room, user=self.user1_account, content="Hello")
        self.client.login(username=self.account1['username'], password=self.account1['password']);
        response = self.client.get(self.urls["chat_to_user"])
        self.assertEqual(response.status_code, 200)

    def test_admin_chat_unknown_account(self):
        # test admin chat to unknown account [ FAIL ]
        self.client.login(username=self.account1['username'], password=self.account1['password']);
        response = self.client.get(self.urls["chat_unknown_user"])
        self.assertEqual(response.status_code, 200)


class TestModel(TestCase):
    def setUp(self):
        self.urls = {
            "index": reverse("chat:chat_to_admin"),
            "chat_to_user": reverse("chat:chat_to_user", args=[1]) # user id = 1
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
        self.user1_account = User.objects.create_user(**account2)

        # Adding initial data in model
        self.chat_room = ChatRoom.objects.create(
            room_name="room-1"
        )
        self.message = Message.objects.create(
            room=self.chat_room,
            user=self.user1_account,
            content="hello admin"
        )

    def test_chat_room_str(self):
        self.assertEqual(self.chat_room.__str__(), self.chat_room.room_name)

    def test_message_str(self):
        self.assertEqual(self.message.__str__(), self.message.room.room_name)