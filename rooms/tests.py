from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *

class TestUrl(SimpleTestCase):
    def test_index_is_resolved(self):
        # test occupant index url use index method for homepage of user (occupant and outside role)
        url = reverse("rooms:index")
        self.assertEqual(resolve(url).func, index)

    def test_handler404_is_resolved(self):
        # test handler404 url use handler404 method
        url = reverse('rooms:handler404', args=[0])
        self.assertEqual(resolve(url).func, handler404)

    def test_handler500_is_resolved(self):
        # test handler500 url use handler500 method
        url = reverse('rooms:handler500')
        self.assertEqual(resolve(url).func, handler500)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.role_outside = Role.objects.create(role_name='Outside')

        self.outside_username = 'outside'
        self.outside_password = 'password'
        self.credentials = {
            'username': self.outside_username,
            'password': self.outside_password,
            'email': 'outside@dormtown.com',
            'first_name': 'Outside',
            'last_name': 'Dormtown'}
        self.outside_user = User.objects.create_user(**self.credentials)
        self.outside_userinfo = UserInfo.objects.create(
            user_id=self.outside_user,
            role_id=self.role_outside,
            room_id=None,
            phone_number='0987654321',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.index_url = reverse('rooms:index')
        self.error_404 = reverse('rooms:handler404', args=[0])
        self.error_500 = reverse('rooms:handler500')
        
    def test_index_without_login(self):
        # search occupant homepage without authorization, return login page with 403 Forbidden
        response = self.client.get(self.index_url)
        self.assertTemplateUsed(response, 'rooms/index.html')

    def test_index(self):
        # authorize for homepage, return the page with 200 OK
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms/index.html')
    
    def test_404(self):
        # when server cannot find the requested resource, return 404.html with 200 OK
        response = self.client.get(self.error_404)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'rooms/404.html')
    
    def test_500(self):
        # when server has encountered a situation it does not know how to handle, return 500.html with 200 OK
        response = self.client.get(self.error_500)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')