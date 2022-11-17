from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from occupant.models import Role,ProblemType,Room,RoomType
from .views import *
import datetime

class TestUrl(SimpleTestCase):
    def test_index_is_resolved(self):
        url = reverse("employee:index")
        self.assertEqual(resolve(url).func, index)
    
    def test_edit_profile_is_resolved(self):
        url = reverse("employee:edit_profile")
        self.assertEqual(resolve(url).func, edit_profile)
    
    def test_update_profile_is_resolved(self):
        url = reverse("employee:update_profile")
        self.assertEqual(resolve(url).func, update_profile)

    def test_submit_is_resolved(self):
        url = reverse("employee:submit", args=[1])
        self.assertEqual(resolve(url).func, submit)

    def test_get_submit_is_resolved(self):
        url = reverse("employee:get_submit", args=[1])
        self.assertEqual(resolve(url).func, get_submit)

    def test_assign_is_resolved(self):
        url = reverse("employee:assign", args=[1])
        self.assertEqual(resolve(url).func, assign)

    def test_get_assign_is_resolved(self):
        url = reverse("employee:get_assign", args=[1])
        self.assertEqual(resolve(url).func, get_assign)

    def test_list_of_jobs_is_resolved(self):
        url = reverse("employee:list_of_jobs")
        self.assertEqual(resolve(url).func, list_of_jobs)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.role_technician = Role.objects.create(role_name='Technician')
        self.role_housekeeper = Role.objects.create(role_name='Housekeeper')
        self.role_occupant = Role.objects.create(role_name='Occupant')

        self.room_type_s = RoomType.objects.create(
            class_level='S',
            price=6500,
            room_service=2,
            tv_fridge=True,
            wardrobe=True,
            water_heater=True
        )

        self.room_available = Room.objects.create(
            room_number='101',
            room_type=self.room_type_s,
            status=True
        )

        self.technician_username = 'technician'
        self.technician_password = 'technician_pw'
        self.credentials = {
            'username': self.technician_username,
            'password': self.technician_password,
            'email': 'technician@dormtown.com',
            'first_name': 'Technician',
            'last_name': 'Dormtown'}
        self.technician_user = User.objects.create_user(**self.credentials)
        self.technician_userinfo = UserInfo.objects.create(
            user_id=self.technician_user,
            role_id=self.role_technician,
            room_id=None,
            phone_number='0812345678',
            address='18/5',
            street='Petchahueng21',
            city='Prapadang',
            state='Samutprakarn',
            country='Thailand',
            zip_code='11111',
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
            role_id=self.role_occupant,
            room_id=self.room_available,
            phone_number='0987654322',
            address='123/45',
            street='Changwattana',
            city='Pakkret',
            state='Nonthabuti',
            country='Thailand',
            zip_code='12345',
        )

        self.housekeeper_username = 'housekeeper'
        self.housekeeper_password = 'housekeeper_pw'
        self.credentials = {
            'username': self.housekeeper_username,
            'password': self.housekeeper_password,
            'email': 'housekeeper@dormtown.com',
            'first_name': 'Housekeeper',
            'last_name': 'Dormtown'}
        self.housekeeper_user = User.objects.create_user(**self.credentials)
        self.housekeeper_userinfo = UserInfo.objects.create(
            user_id=self.housekeeper_user,
            role_id=self.role_housekeeper,
            room_id=None,
            phone_number='0987654323',
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
        

        self.status_idle = StatusType.objects.create(
            status_name='Idle'
        )
        self.status_doing = StatusType.objects.create(
            status_name='Doing'
        )
        self.status_done = StatusType.objects.create(
            status_name='Done'
        )

        self.problem_type = ProblemType.objects.create(
            problem_name='Fix electric equipment'
        )

        self.problem_type1 = ProblemType.objects.create(
            problem_name='Move out'
        )

        self.problem_type2 = ProblemType.objects.create(
            problem_name='Irrigation problem'
        )

        self.problem_type3 = ProblemType.objects.create(
            problem_name='Cleaning Service'
        )

        self.report = Report.objects.create(
            from_user_id=self.occupant_user,
            problem_type_id=self.problem_type,
            due_date=datetime.datetime.today(),
            note='',
            status_id=self.status_idle,
        )

        self.report1 = Report.objects.create(
            from_user_id=self.occupant_user,
            problem_type_id=self.problem_type1,
            due_date=datetime.datetime.today(),
            note='',
            status_id=self.status_idle,
        )

        self.report2 = Report.objects.create(
            from_user_id=self.occupant_user,
            problem_type_id=self.problem_type1,
            due_date=datetime.datetime.today(),
            assign_to_id = self.technician_user,
            note='',
            status_id=self.status_idle,
        )

        self.report3 = Report.objects.create(
            from_user_id=self.occupant_user,
            problem_type_id=self.problem_type2,
            due_date=datetime.datetime.today(),
            assign_to_id = self.technician_user,
            note='',
            status_id=self.status_idle,
        )

        self.report4 = Report.objects.create(
            from_user_id=self.occupant_user,
            problem_type_id=self.problem_type3,
            due_date=datetime.datetime.today(),
            assign_to_id = self.technician_user,
            note='',
            status_id=self.status_idle,
        )

        self.index_url = reverse('employee:index')
        self.list_of_jobs_url = reverse('employee:list_of_jobs')
        self.edit_profile_url = reverse('employee:edit_profile')
        self.update_profile_url = reverse('employee:update_profile')
        self.assign_url = reverse('employee:assign',args=[self.report.id])
        self.get_assign_url = reverse('employee:get_assign',args=[self.report.id])
        self.get_assign2_url = reverse('employee:get_assign',args=[self.report3.id])
        self.get_assign3_url = reverse('employee:get_assign',args=[self.report4.id])
        self.get_assign1_url = reverse('employee:get_assign',args=[self.report1.id])
        self.submit_url = reverse('employee:submit',args=[self.report.id])
        self.get_submit_url = reverse('employee:get_submit',args=[self.report.id])
        self.get_submit2_url = reverse('employee:get_submit',args=[self.report2.id])
        
        
    def test_index_without_login(self):
        # serch occupant homepage without authorization, return login page with 403 Forbidden
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_index_wrong_role(self):
        # serch occupant homepage without authorization, return login page with 403 Forbidden
        self.client.login(username=self.occupant_username, password=self.occupant_password)
        response = self.client.get(self.index_url)

        self.assertTemplateUsed(response, 'rooms/index.html')


    def test_index_error_userinfo(self):
        # serch occupant homepage with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_index(self):
        # authorize for occupant homepage with user and userinfo model, return the page with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        Report.objects.create(
            from_user_id=self.occupant_user,
            problem_type_id=self.problem_type,
            assign_to_id =self.technician_user,
            due_date=datetime.datetime.today(),
            note='',
            status_id=self.status_doing)
              
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/index.html')

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

    def test_edit_profile(self):
        # authorize for editing profile with user and userinfo data, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/edit_profile.html')

    def test_update_profile_without_login(self):
        # update profile to model without authorization, return login page with 403 Forbidden
        response = self.client.get(self.update_profile_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_update_profile_get(self):
        # update profile to model with get method, return 404.html with 404 Not Found
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.update_profile_url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'rooms/404.html')

    def test_update_profile_error_userinfo(self):
        # update profile to model with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.post(self.update_profile_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_update_profile(self):
        # authorize for updating profile to model with userinfo model and post method, redirect to occupant:index
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.post(self.update_profile_url)

        self.assertRedirects(response, '/employee/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_submit_without_login(self):
        response = self.client.get(self.submit_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_submit_error_userinfo(self):
        # serch reservation page with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.submit_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')
    
    def test_submit(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.get(self.submit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/submit.html')
    
    def test_get_submit_without_login(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        response = self.client.get(self.get_submit_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_get_submit(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.get(self.get_submit2_url)

        self.assertRedirects(response, '/employee/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    
    def test_assign_without_login(self):
        response = self.client.get(self.assign_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_assign_error_userinfo(self):
        # serch reservation page with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.assign_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')
    
    def test_assign(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.get(self.assign_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/assign.html')
    
    def test_get_assign_without_login(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        response = self.client.get(self.get_assign_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_get_assign(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.get(self.get_assign1_url)

        self.assertRedirects(response, '/employee/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_get_assign2(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.get(self.get_assign2_url)

        self.assertRedirects(response, '/employee/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_get_assign3(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.get(self.get_assign3_url)

        self.assertRedirects(response, '/employee/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_list_of_jobs_without_login(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        response = self.client.get(self.assign_url)
        response = self.client.get(self.list_of_jobs_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_list_of_jobs(self):
        # occupant role search reservation page with authorization (already reserved), return result of seservation path with 200 OK
        self.client.login(username=self.technician_username, password=self.technician_password)

        response = self.client.get(self.list_of_jobs_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/list_of_jobs.html')
    
    def test_list_of_jobs_error_userinfo(self):
        # serch reservation page with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.list_of_jobs_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')
    
