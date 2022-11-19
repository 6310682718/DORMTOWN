from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *
import datetime


class TestUrl(SimpleTestCase):
    #test_url_login
    def test_login_is_resolved(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func, login)

    #test_url_logout
    def test_logout_is_resolved(self):
        url = reverse("users:register")
        self.assertEqual(resolve(url).func, register)


class TestView(TestCase):
    # set up user1
    def setUp(self):
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
            'last_name': self.last}
        self.new_user = User.objects.create_user(**self.credentials)
        
        # set up user2

        self.username1 = 'newuser1'
        self.password1 = 'newuserpass1'
        self.email1 = 'newuser1@dormtown.com'
        self.first1 = 'New1'
        self.last1 = 'User1'
        self.credentials1 = {
            'username': self.username1,
            'password': self.password1,
            'email': self.email1,
            'first_name': self.first1,
            'last_name': self.last1}
        self.new_user1 = User.objects.create_user(**self.credentials1)

        self.outsite_role = Role.objects.create(role_name='Outside')
        self.occupant_role = Role.objects.create(role_name='Occupant')
        self.manager_role = Role.objects.create(role_name='Manager')
        self.technician_role = Role.objects.create(role_name='Technician')
        self.housekeeper_role = Role.objects.create(role_name='Housekeeper')

        self.user_manager = UserInfo.objects.filter(user_id=2).update(role_id=1)
        # self.phone = '0987654321'
        # self.address = '123/123'
        # self.street = 'SomeRoad'
        # self.city = 'Pakkret'
        # self.state = 'Nonthaburi'
        # self.country = 'Thailand'
        # self.zip = '12345'

        self.room_type = RoomType.objects.create(
            class_level='S',
            price=6500,
            room_service=2,
            tv_fridge=True,
            wardrobe=True,
            water_heater=True
        )

        self.room_available = Room.objects.create(
            room_number='101',
            room_type=self.room_type,
            status=True
        )

        # self.user_info = UserInfo.objects.create(
        #     user_id=self.new_user,
        #     role_id=self.outsite_role,
        #     room_id=self.room_available,
        #     phone_number=self.phone,
        #     address=self.address,
        #     street=self.street,
        #     city=self.city,
        #     state=self.state,
        #     country=self.country,
        #     zip_code=self.zip,
        # )
        self.register_url = reverse('users:register')

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
            role_id=self.outsite_role,
            room_id=None,
            phone_number='0987654321',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.occupant_username = 'occupant'
        self.occupant_password = 'password'
        self.credentials = {
            'username': self.occupant_username,
            'password': self.occupant_password,
            'email': 'occupant@dormtown.com',
            'first_name': 'Occupant',
            'last_name': 'Dormtown'}
        self.occupant_user = User.objects.create_user(**self.credentials)
        self.occupant_userinfo = UserInfo.objects.create(
            user_id=self.occupant_user,
            role_id=self.occupant_role,
            room_id=None,
            phone_number='0987654321',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.manager_username = 'manager'
        self.manager_password = 'password'
        self.credentials = {
            'username': self.manager_username,
            'password': self.manager_password,
            'email': 'manager@dormtown.com',
            'first_name': 'Manager',
            'last_name': 'Dormtown'}
        self.manager_user = User.objects.create_user(**self.credentials)
        self.manager_userinfo = UserInfo.objects.create(
            user_id=self.manager_user,
            role_id=self.manager_role,
            room_id=None,
            phone_number='0987654321',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.technician_username = 'technician'
        self.technician_password = 'password'
        self.credentials = {
            'username': self.technician_username,
            'password': self.technician_password,
            'email': 'technician@dormtown.com',
            'first_name': 'Technician',
            'last_name': 'Dormtown'}
        self.technician_user = User.objects.create_user(**self.credentials)
        self.technician_userinfo = UserInfo.objects.create(
            user_id=self.technician_user,
            role_id=self.technician_role,
            room_id=None,
            phone_number='0987654321',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.housekeeper_username = 'housekeeper'
        self.housekeeper_password = 'password'
        self.credentials = {
            'username': self.housekeeper_username,
            'password': self.housekeeper_password,
            'email': 'housekeeper@dormtown.com',
            'first_name': 'Housekeeper',
            'last_name': 'Dormtown'}
        self.housekeeper_user = User.objects.create_user(**self.credentials)
        self.housekeeper_userinfo = UserInfo.objects.create(
            user_id=self.housekeeper_user,
            role_id=self.housekeeper_role,
            room_id=None,
            phone_number='0987654321',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.temp_username = 'temp'
        self.temp_password = 'password'
        self.credentials = {
            'username': self.temp_username,
            'password': self.temp_password,
            'email': 'temp@dormtown.com',
            'first_name': 'Temp',
            'last_name': 'Dormtown'}
        self.temp_user = User.objects.create_user(**self.credentials)

        self.change_password_url = reverse('users:change_password')
        self.edit_profile_url = reverse('users:edit_profile')
        self.login_url = reverse('users:login')


    # test when user get to register page  will get response register.html
    def test_register_index_with_login(self):
        self.client.login(username=self.outside_username, password=self.outside_password)
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'rooms/index.html')
    
    def test_login_index_with_login(self):
        self.client.login(username=self.outside_username, password=self.outside_password)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'rooms/index.html')
    
    def test_register_index(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    # test when user register with all correct form 
    def test_register(self):
        url = "/users/register"
        body = {
            "username": "test1@gmail.com",
            "firstname": "test",
            "lastname": "test",
            "password": "test1",
            "confirmPassword": "test1",
            "email": "test@gmail.com",
            "phoneNumber": "0963711479",
            "address": "test",
            "street": "test",
            "city": "test",
            "state": "test",
            "country": "test",
            "zip": "1234",
        }
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 200)

    def test_register_fail_con_pass(self):
        url = "/users/register"
        body2 = {
            "username": "test1@gmail.com",
            "firstname": "",
            "lastname": "test",
            "password": "test1",
            "confirmPassword": "test1",
            "email": "test@gmail.com",
            "phoneNumber": "0963711479",
            "address": "test",
            "street": "test",
            "city": "test",
            "state": "test",
            "country": "test",
            "zip": "1234",
        }
        response = self.client.post(url, body2)
        self.assertEqual(response.status_code, 400)

    def test_register_fail_no_input(self):
        url = "/users/register"
        body3 = {
            "username": "test1@gmail.com",
            "firstname": "test",
            "lastname": "test",
            "password": "test1",
            "confirmPassword": "test123",
            "email": "test@gmail.com",
            "phoneNumber": "0963711479",
            "address": "test",
            "street": "test",
            "city": "test",
            "state": "test",
            "country": "test",
            "zip": "1234",
        }
        response = self.client.post(url, body3)
        self.assertEqual(response.status_code, 400)
    
    def test_register_fail_username_same(self):
        url = "/users/register"
        body4 = {
            "username": "newuser",
            "firstname": "test",
            "lastname": "test",
            "password": "test1",
            "confirmPassword": "test123",
            "email": "newuser@dormtown.com",
            "phoneNumber": "0963711479",
            "address": "test",
            "street": "test",
            "city": "test",
            "state": "test",
            "country": "test",
            "zip": "1234",
        }
        response = self.client.post(url, body4)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        url = "/users/login"
        body = {"username": "outside", "password": "password"}
        response = self.client.post(url, body)

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_login_error(self):
        url = "/users/login"
        body2 = {"username": "newuser1", "password": "newuserpa"}
        response = self.client.post(url, body2)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logout(self):
        url = "/users/logout"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_change_password_without_login(self):
        # serch change password page without authorization, return login page with 403 Forbidden
        response = self.client.get(self.change_password_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_report_error_userinfo(self):
        # change password with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.change_password_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_change_password_post(self):
        # change password with post method, return login page with 200 OK
        self.client.login(username=self.outside_username, password=self.outside_password)
        
        response = self.client.post(self.change_password_url, {
            'old_password': self.outside_password,
            'new_password': 'newpassword',
            'con_password': 'newpassword'
        })

        self.assertRedirects(response, '/users/login', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_change_password_post_error_old_password(self):
        # change password with post method but old password is invalid, return login page with 400 Bad Request
        self.client.login(username=self.outside_username, password=self.outside_password)
        
        response = self.client.post(self.change_password_url, {
            'old_password': 'oldpassword',
            'new_password': 'newpassword',
            'con_password': 'newpassword'
        })

        self.assertRedirects(response, '/users/changepassword', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_change_password_post_error_new_password(self):
        # change password with post method but old password is invalid, return login page with 400 Bad Request
        self.client.login(username=self.outside_username, password=self.outside_password)
        
        response = self.client.post(self.change_password_url, {
            'old_password': self.outside_password,
            'new_password': 'newpass',
            'con_password': 'newpassword'
        })

        self.assertRedirects(response, '/users/changepassword', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_change_password_get(self):
        # change password with get method, return change password page with 400 Bad Request
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.get(self.change_password_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/changepass.html')

    def test_edit_profile_without_login(self):
        # edit profile without authorization, return login page with 403 Forbidden
        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_edit_profile_error_userinfo(self):
        # edit profile with authorization but do not have userinfo model, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_edit_profile_get(self):
        # authorize for editing profile with get method, return the page with 200 OK
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')

    def test_edit_profile_outside_post(self):
        # outsite role authorize for editing profile with get method, redirect index with 200 OK
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.post(self.edit_profile_url)

        self.assertRedirects(response, '/occupant/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_profile_occupant_post(self):
        # occupant role authorize for editing profile with get method, redirect index with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.post(self.edit_profile_url)

        self.assertRedirects(response, '/occupant/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_profile_technician_post(self):
        # technician role authorize for editing profile with get method, redirect index with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.post(self.edit_profile_url)

        self.assertRedirects(response, '/employee/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_profile_housekeeper_post(self):
        # housekeeper role authorize for editing profile with get method, redirect index with 200 OK
        self.client.login(username=self.housekeeper_username, password=self.housekeeper_password)

        response = self.client.post(self.edit_profile_url)

        self.assertRedirects(response, '/employee/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_profile_manager_post(self):
        # housekeeper role authorize for editing profile with get method, redirect index with 200 OK
        self.client.login(username=self.manager_username, password=self.manager_password)

        response = self.client.post(self.edit_profile_url)

        self.assertRedirects(response, '/manager/', status_code=302, target_status_code=200, fetch_redirect_response=True)