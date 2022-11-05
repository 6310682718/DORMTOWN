from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *

class TestUrl(SimpleTestCase):
    def test_index_is_resolved(self):
        url = reverse("occupant:index")
        self.assertEqual(resolve(url).func, index)

    def test_reserve_is_resolved(self):
        url = reverse("occupant:reserve")
        self.assertEqual(resolve(url).func, reserve)

    def test_create_reserve_is_resolved(self):
        url = reverse("occupant:create_reserve", args=[1])
        self.assertEqual(resolve(url).func, create_reserve)

    def test_detail_reserve_is_resolved(self):
        url = reverse("occupant:get_reserve")
        self.assertEqual(resolve(url).func, get_reserve)

    def test_delete_reserve_is_resolved(self):
        url = reverse("occupant:delete_reserve", args=[1])
        self.assertEqual(resolve(url).func, delete_reserve)

    def test_report_is_resolved(self):
        url = reverse("occupant:report")
        self.assertEqual(resolve(url).func, report)

    def test_create_report_is_resolved(self):
        url = reverse("occupant:create_report")
        self.assertEqual(resolve(url).func, create_report)

    def test_detail_report_is_resolved(self):
        url = reverse("occupant:get_report", args=[1])
        self.assertEqual(resolve(url).func, get_report)

    def test_all_report_is_resolved(self):
        url = reverse("occupant:list_report")
        self.assertEqual(resolve(url).func, list_report)

    def test_delete_report_is_resolved(self):
        url = reverse("occupant:delete_report", args=[1])
        self.assertEqual(resolve(url).func, delete_report)