from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *
import datetime

class TestUrl(SimpleTestCase):
    def test_index_is_resolved(self):
        # test occupant index url use index method for homepage of user (occupant and outside role)
        url = reverse("occupant:index")
        self.assertEqual(resolve(url).func, index)

    def test_reserve_is_resolved(self):
        # test occupant reserve url use reserve method for reservation page
        url = reverse("occupant:reserve")
        self.assertEqual(resolve(url).func, reserve)

    def test_create_reserve_is_resolved(self):
        # test occupant create reserve url use create reserve method for creating reservation
        url = reverse("occupant:create_reserve", args=[1])
        self.assertEqual(resolve(url).func, create_reserve)

    def test_detail_reserve_is_resolved(self):
        # test occupant get reserve url use get reserve method for detail of reservation
        url = reverse("occupant:get_reserve")
        self.assertEqual(resolve(url).func, get_reserve)

    def test_delete_reserve_is_resolved(self):
        # test occupant delete reserve url use delete reserve method for deleting reservation
        url = reverse("occupant:delete_reserve", args=[1])
        self.assertEqual(resolve(url).func, delete_reserve)

    def test_report_is_resolved(self):
        # test occupant report url use report method for report problem page
        url = reverse("occupant:report")
        self.assertEqual(resolve(url).func, report)

    def test_detail_report_is_resolved(self):
        # test occupant get report url use get report method for detail of reporting
        url = reverse("occupant:get_report", args=[1])
        self.assertEqual(resolve(url).func, get_report)

    def test_all_report_is_resolved(self):
        # test occupant list report url use get list method for all of occpant's reporting
        url = reverse("occupant:list_report")
        self.assertEqual(resolve(url).func, list_report)

    def test_delete_report_is_resolved(self):
        # test occupant delete report url use delete report method for deleting reporting
        url = reverse("occupant:delete_report", args=[1])
        self.assertEqual(resolve(url).func, delete_report)

    def test_edit_report_is_resolved(self):
        # test occupant edit report url use delete report method for deleting reporting
        url = reverse("occupant:edit_report", args=[1])
        self.assertEqual(resolve(url).func, edit_report)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.role_outside = Role.objects.create(role_name='Outside')
        self.role_occupant = Role.objects.create(role_name='Occupant')
        self.role_manager = Role.objects.create(role_name='Manager')

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
            room_id=self.room_unavailable,
            phone_number='0987654322',
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
            'email': 'occupant@dormtown.com',
            'first_name': 'Occupant',
            'last_name': 'Dormtown'}
        self.manager_user = User.objects.create_user(**self.credentials)
        self.manager_userinfo = UserInfo.objects.create(
            user_id=self.manager_user,
            role_id=self.role_manager,
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

        self.occupant_reserve = Reserve.objects.create(
            user_id=self.occupant_user,
            room_type=self.room_type_a,
            due_date=datetime.datetime.today(),
            create_at=datetime.datetime.now(),
            status_type=self.status_done
        )

        self.problem_type = ProblemType.objects.create(
            problem_name='Cleaning service'
        )

        self.report = Report.objects.create(
            from_user_id=self.occupant_user,
            problem_type_id=self.problem_type,
            due_date=datetime.datetime.today(),
            note='',
            status_id=self.status_idle,
        )

        self.index_url = reverse('occupant:index')
        self.reserve_url = reverse('occupant:reserve')
        self.create_reserve_url = reverse('occupant:create_reserve', args=[self.room_type_s.id])
        self.detail_reserve_url = reverse('occupant:get_reserve')
        self.delete_reserve_url = reverse('occupant:delete_reserve', args=[self.occupant_reserve.id])
        self.report_url = reverse('occupant:report')
        self.detail_report_url = reverse('occupant:get_report', args=[self.report.id])
        self.list_report_url = reverse('occupant:list_report')
        self.delete_report_url = reverse('occupant:delete_report', args=[self.report.id])
        self.edit_report_url = reverse('occupant:edit_report', args=[self.report.id])

    def test_index_without_login(self):
        # search occupant homepage without authorization, return login page with 403 Forbidden
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_index_error_userinfo(self):
        # search occupant homepage with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_index(self):
        # authorize for occupant homepage with user and userinfo model, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')

    def test_reserve_without_login(self):
        # search reservation page without authorization, return login page with 403 Forbidden
        response = self.client.get(self.reserve_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_reserve_error_userinfo(self):
        # search reservation page with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.reserve_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_reserve_outside(self):
        # outside role search reservation page with authorization, return the page with 200 OK
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.get(self.reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/reserve.html')

    def test_reserve_occupant(self):
        # occupant role search reservation page with authorization (already reserved), redirect to result of seservation path
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.reserve_url)

        self.assertRedirects(response, '/occupant/reserve/detail', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_create_reserve_without_login(self):
        # create reservation without authorization, return login page with 403 Forbidden
        response = self.client.get(self.create_reserve_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_create_reserve_error_userinfo(self):
        # create reservation with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.create_reserve_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_create_reserve_get(self):
        # get reservation form page by outside role, return the page with 200 OK
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.get(self.create_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/reserve_form.html')

    def test_create_reserve_post(self):
        # create reservation page by post method, return result of reservation page with 200 OK
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.post(self.create_reserve_url, {
            'due_date': datetime.datetime.today().strftime(("%Y-%m-%d")),
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_reserve.html')

    def test_detail_reserve_without_login(self):
        # get detail of reservation without authorization, return login page with 403 Forbidden
        response = self.client.get(self.detail_reserve_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_detail_reserve_error_userinfo(self):
        # get detail of reservation with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.detail_reserve_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_detail_reserve_outside(self):
        # outside role get detail of reservation but have no reservation, redirct to reservation page
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.get(self.detail_reserve_url)

        self.assertRedirects(response, '/occupant/reserve', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_detail_reserve_occupant(self):
        # occupant role (or outside role who has reserved already) get detail of reservation with authorization, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.detail_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_reserve.html')

    def test_delete_reserve_without_login(self):
        # delete reservation without authorization, return login page with 403 Forbidden
        response = self.client.get(self.delete_reserve_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_reserve_outside(self):
        # outside role delete reservation but have no reservation, redirect to occupant homepage
        self.client.login(username=self.outside_username, password=self.outside_password)

        response = self.client.get(self.delete_reserve_url)

        self.assertRedirects(response, '/occupant/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_delete_reserve_occupant(self):
        # occupant role (or outside role who has reserved already) delete reservation, delete reservation and redirct to occupant homepage
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.delete_reserve_url)

        self.assertRedirects(response, '/occupant/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_report_without_login(self):
        # search reservation page without authorization, return login page with 403 Forbidden
        response = self.client.get(self.report_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_report_error_userinfo(self):
        # search report page with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.report_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_report_get(self):
        # search report page with get method, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.temp_password)

        response = self.client.get(self.report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/report.html')

    def test_report_post_without_data(self):
         # occupant create reporting with post method without data, redirect to report page
         self.client.login(username=self.occupant_username, password=self.occupant_password)

         response = self.client.post(self.report_url)

         self.assertRedirects(response, '/occupant/report/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_report_post(self):
        # occupant create reporting with post method, redirect to result of reporting
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.post(self.report_url, {
            'problem': self.problem_type,
            'due_date': datetime.datetime.today().strftime(("%Y-%m-%d")),
            'note': ''
        })

        self.assertRedirects(response, '/occupant/report/detail/2', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_report_without_login(self):
        # edit reporing without authorization, return login page with 403 Forbidden
        response = self.client.get(self.edit_report_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_edit_report_without_report(self):
        # athorize to edit reporing without report data, return 404.html with 404 Not Found
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        url = reverse('occupant:edit_report', args=[2])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'rooms/404.html')

    def test_edit_report_get(self):
        # occupant want to edit reporting with get method, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.edit_report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/edit_report.html')

    def test_edit_report_post_without_data(self):
        # occupant edit reporting with post method without data, redirect to report page
        self.client.login(username=self.occupant_username, password=self.occupant_password)
        
        response = self.client.post(self.edit_report_url)

        self.assertRedirects(response, '/occupant/report/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_report_post(self):
        # occupant create reporting with post method without data, redirect to list of report page
        self.client.login(username=self.occupant_username, password=self.occupant_password)
        
        response = self.client.post(self.edit_report_url, {
            'problem': self.problem_type,
            'due_date': datetime.datetime.today().strftime(("%Y-%m-%d")),
            'note': ''
        })

        self.assertRedirects(response, '/occupant/report/all', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_detail_report_without_login(self):
        # get detail of report without authorization, return login page with 403 Forbidden
        response = self.client.get(self.detail_report_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_detail_report_error_userinfo(self):
        # search detail of report with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.detail_report_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_detail_report(self):
        # search detail of report with authorization, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.detail_report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_report.html')

    def test_list_report_without_login(self):
        # get list of report without authorization, return login page with 403 Forbidden
        response = self.client.get(self.list_report_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_list_report_error_userinfo(self):
        # search list of report with authorization but do not have userinfo data, return 500.html with 500 Internal Server Error
        self.client.login(username=self.temp_username, password=self.temp_password)

        response = self.client.get(self.list_report_url)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'rooms/500.html')

    def test_list_report(self):
        # search list of report with authorization, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.list_report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/list_report.html')

    def test_delete_report_without_login(self):
        # delete report without authorization, return login page with 403 Forbidden
        response = self.client.get(self.delete_report_url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_report_without_data(self):
        # occupant delete reporting with authorization but do not have the reporting, return 404.html with 404 Not Found
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        url = url = reverse('occupant:delete_report', args=[2])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'rooms/404.html')

    def test_delete_report(self):
        # occupant delete reporting with authorization and data, redirect to list of reporting page
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.post(self.delete_report_url)

        self.assertRedirects(response, '/occupant/report/all', status_code=302, target_status_code=200, fetch_redirect_response=True)

class TestModel(TestCase):
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

        self.username = 'user'
        self.password = 'userpass'
        self.email = 'user@dormtown.com'
        self.first = 'Another'
        self.last = 'User'
        self.credentials = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first,
            'last_name': self.last}
        self.another_user = User.objects.create_user(**self.credentials)

        self.role = Role.objects.create(
            role_name='Manager'
        )

        self.room_type = RoomType.objects.create(
            class_level='C',
            price=6500
        )

        self.room = Room.objects.create(
            room_number=101,
            room_type=self.room_type,
            status=True
        )

        self.user_info = UserInfo.objects.create(
            user_id=self.new_user,
            role_id=self.role,
            room_id=self.room,
            phone_number='0644153591',
            address='56 Moo. 3',
            street='SomeStreet Road',
            state='SomeState',
            city='SomeCity',
            country='Thailand',
            zip_code='12345'
        )

        self.status_type = StatusType.objects.create(
            status_name='Idle'
        )

        self.reserve = Reserve.objects.create(
            user_id=self.new_user,
            room_type=self.room_type,
            due_date=datetime.date.today(),
            create_at=datetime.date.today(),
            status_type=self.status_type
        )

        self.problem_type = ProblemType.objects.create(
            problem_name='Cleaning service'
        )

        self.report = Report.objects.create(
            from_user_id=self.new_user,
            problem_type_id=self.problem_type,
            due_date=datetime.date.today(),
            note='Do not stole my stuff',
            status_id=self.status_type,
            assign_to_id=self.another_user,
            role_id=self.role
        )

    def test_role_str(self):
        # test method str in Role model
        self.assertEquals(self.role.__str__(), self.role.role_name)

    def test_room_type_str(self):
        # test method str in RoomType model
        self.assertEquals(self.room_type.__str__(), self.room_type.class_level)

    def test_room_str(self):
        # test method str in Room model
        self.assertEquals(self.room.__str__(
        ), f'#{ self.room.room_number } Class { self.room.room_type }')

    def test_user_info_str(self):
        # test method str in UserInfo model
        self.assertEquals(self.user_info.__str__(),
                          f'{ self.new_user.username } { self.role.role_name }')

    def test_status_type_str(self):
        # test method str in StatusType model
        self.assertEquals(self.status_type.__str__(),
                          self.status_type.status_name)

    def test_reserve_str(self):
        # test method str in Reserve model
        self.assertEquals(self.reserve.__str__(
        ), f'Class { self.room_type.class_level } { self.status_type.status_name }')

    def test_problem_type_str(self):
        # test method str in ProblemType model
        self.assertEquals(self.problem_type.__str__(),
                          self.problem_type.problem_name)

    def test_report_str(self):
        # test method str in Report model
        self.assertEquals(self.report.__str__(
        ), f'{ self.new_user.username } report { self.problem_type.problem_name }')