from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import *
# Create your tests here.


class TestUrl(SimpleTestCase):
    def setUp(self):
        self.urls = {
            "dashboard": reverse("manager:dashboard"),
            "rooms_available": reverse("manager:rooms_available"),
            "rooms_reserve": reverse("manager:rooms_reserve"),
            "rooms_unavailable": reverse("manager:rooms_unavailable"),
            "employee_list": reverse("manager:employee_list"),
            "occupant_list": reverse("manager:occupant_list"),
            "report_logs": reverse("manager:report_logs")


        }

    def test_dashboard(self):
        
        self.assertEqual(resolve(self.urls['dashboard']).func, index)
    
    def test_rooms_available(self):
        self.assertEqual(resolve(self.urls['rooms_available']).func, rooms_available)
    
    def test_rooms_reserve(self):
        self.assertEqual(resolve(self.urls['rooms_reserve']).func, rooms_reserve)

    def test_rooms_unavailable(self):
        self.assertEqual(resolve(self.urls['rooms_unavailable']).func, rooms_unavailable)
    
    def test_employee_list(self):
        self.assertEqual(resolve(self.urls['employee_list']).func, employee_list)
    
    def test_occupant_list(self):
        self.assertEqual(resolve(self.urls['occupant_list']).func, occupant_list)

    def test_edit_profile_is_resolved(self):
        url = reverse("manager:edit_profile", args=[1])
        self.assertEqual(resolve(url).func, edit_profile)
    
    def test_delete_user_is_resolved(self):
        url = reverse("manager:delete_user", args=[1])
        self.assertEqual(resolve(url).func, delete_user)
class TestViews(TestCase):
    def setUp(self):
        self.urls = {
            "dashboard": reverse("manager:dashboard"),
            "rooms_available": reverse("manager:rooms_available"),
            "rooms_reserve": reverse("manager:rooms_reserve"),
            "rooms_unavailable": reverse("manager:rooms_unavailable"),
            "employee_list": reverse("manager:employee_list"),
            "occupant_list": reverse("manager:occupant_list"),
            "report_logs": reverse("manager:report_logs"),
            "edit_profile": reverse("manager:edit_profile", args=[1]),
            "edit_profile_error": reverse("manager:edit_profile", args=[1000]),
            "delete_profile": reverse("manager:delete_user", args=[1]),
            "delete_profile_error": reverse("manager:delete_user", args=[1000])
        }
        self.client = Client()

        # initial account
        
        self.room_type_s = RoomType.objects.create(
            class_level='S',
            price=6500,
            room_service=2,
            tv_fridge=True,
            wardrobe=True,
            water_heater=True
        )
        self.room_type_a = RoomType.objects.create(
            class_level='A',
            price=4500,
            room_service=1,
            tv_fridge=False,
            wardrobe=True,
            water_heater=True
        )

        self.room_available = Room.objects.create(
            room_number='101',
            room_type=self.room_type_s,
            status=True
        )
        self.room_unavailable = Room.objects.create(
            room_number='102',
            room_type=self.room_type_a,
            status=False
        )
        self.manager_username = 'manager'
        self.manager_password = 'password'
        self.credentials = {
            'username': self.manager_username,
            'password': self.manager_password,
            'email': 'occupant@dormtown.com',
            'first_name': 'Occupant',
            'last_name': 'Dormtown'}
        self.manager_user = User.objects.create_superuser(**self.credentials)
        self.role_manager = Role.objects.create(role_name='Manager')
        self.manager_userinfo = UserInfo.objects.create(
            user_id=self.manager_user,
            role_id=self.role_manager,
            room_id=None,
            phone_number='0987654321',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.client = Client()
        self.temp_username = 'temp'
        self.temp_password = 'password'
        self.credentials = {
            'username': self.temp_username,
            'password': self.temp_password,
            'email': 'temp@dormtown.com',
            'first_name': 'Temp',
            'last_name': 'Dormtown'}
        self.temp_user = User.objects.create_user(**self.credentials)

        

    def test_dashboard_login(self):
        self.client.login(username=self.manager_username, password=self.manager_password)
        response = self.client.get(self.urls["dashboard"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/dashboard.html')
    
    def test_dashboard_without_login(self):
        response = self.client.get(self.urls["dashboard"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/dashboard.html')
    
    def test_rooms_available_login(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(self.urls["rooms_available"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/available_rooms.html')

    def test_rooms_unavailable_login(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(self.urls["rooms_unavailable"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/unavailable_rooms.html')
    
    def test_rooms_reserve_login(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(self.urls["rooms_reserve"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/reserve_rooms.html')

    def test_employee_list_login(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(self.urls["employee_list"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/employee_list.html')
    
    def test_occupant_list_login(self):
            self.client.login(username="admin", password="admin")
            response = self.client.get(self.urls["occupant_list"])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'manager/occupant_list.html')
    
    def test_report_logs_login(self):
            self.client.login(username="admin", password="admin")
            response = self.client.get(self.urls["report_logs"])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'manager/report_logs.html')

    def test_edit_profile_without_login(self):
            response = self.client.get(self.urls["edit_profile"])
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, 'users/login.html')
    
    def test_edit_profile_login(self):
            self.client.login(username=self.manager_username, password=self.manager_password)
            response = self.client.get(self.urls["edit_profile"])
            self.assertTemplateUsed(response, 'users/edit_profile.html')

    def test_edit_profile_error_userinfo(self):
        # serch reservation page with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
            self.client.login(username=self.temp_username, password=self.temp_password)
            response = self.client.get(self.urls["edit_profile_error"])
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, 'rooms/500.html')

    def test_delete_profile_without_login(self):
            response = self.client.get(self.urls["delete_profile"])
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_profile_login(self):
            self.client.login(username=self.manager_username, password=self.manager_password)
            response = self.client.get(self.urls["delete_profile"])
            self.assertTemplateUsed(response, 'manager/dashboard.html')

    def test_delete_profile_error_userinfo(self):
        # serch reservation page with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
            self.client.login(username=self.temp_username, password=self.temp_password)
            response = self.client.get(self.urls["delete_profile_error"])
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, 'rooms/500.html')




    #     response = self.client.get(self.urls["dashboard"])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "manager/dashboard.html")
