from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *
import datetime


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


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

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

        self.phone = '0987654321'
        self.address = '123/123'
        self.street = 'SomeRoad'
        self.city = 'Pakkret'
        self.state = 'Nonthaburi'
        self.country = 'Thailand'
        self.zip = '12345'

        self.phone1 = '0987654320'

        self.room_type = RoomType.objects.create(
            class_level='S',
            price=6500,
            room_service=2,
            tv_fridge=True,
            wardrobe=True,
            water_heater=True
        )

        self.status_idle = StatusType.objects.create(
            status_name='Idle'
        )
        self.status_doing = StatusType.objects.create(
            status_name='Doing'
        )
        self.status_done = StatusType.objects.create(
            status_name='Done'
        )

        self.reserve1 = Reserve.objects.create(
            user_id=self.new_user1,
            room_type=self.room_type,
            due_date=datetime.datetime.today(),
            create_at=datetime.datetime.now(),
            status_type=self.status_done
        )

        self.room_available = Room.objects.create(
            room_number='101',
            room_type=self.room_type,
            status=True
        )

        self.room_unavailable = Room.objects.create(
            room_number='102',
            room_type=self.room_type,
            status=False
        )

        self.user_info = UserInfo.objects.create(
            user_id=self.new_user,
            role_id=self.outsite_role,
            room_id=self.room_available,
            phone_number=self.phone,
            address=self.address,
            street=self.street,
            city=self.city,
            state=self.state,
            country=self.country,
            zip_code=self.zip,
        )

        self.user_info1 = UserInfo.objects.create(
            user_id=self.new_user1,
            role_id=self.occupant_role,
            room_id=self.room_unavailable,
            phone_number=self.phone1,
            address=self.address,
            street=self.street,
            city=self.city,
            state=self.state,
            country=self.country,
            zip_code=self.zip,
        )

        self.index_url = reverse('occupant:index')
        self.edit_profile_url = reverse('occupant:edit_profile')
        self.update_profile_url = reverse('occupant:update_profile')
        self.reserve_url = reverse('occupant:reserve')
        self.create_reserve_url = reverse('occupant:create_reserve', args=[self.room_type.id])
        self.detail_reserve_url = reverse('occupant:get_reserve')
        self.delete_reserve_url = reverse('occupant:delete_reserve', args=[self.reserve1.id])
        self.report_url = reverse('occupant:report')
        self.create_report_url = reverse('occupant:create_report')
        self.detail_report_url = reverse('occupant:get_report', args=[1])
        self.list_report_url = reverse('occupant:list_report')
        self.delete_report_url = reverse('occupant:delete_report', args=[1])

    def test_index_without_login(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_index_outside(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')
    
    def test_index_occupant(self):
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')

    def test_edit_profile_without_login(self):
        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_edit_profile_outside(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/edit_profile.html')

    def test_edit_profile_occupate(self):
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/edit_profile.html')

    def test_update_profile_without_login(self):
        response = self.client.get(self.update_profile_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_update_profile_get(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.update_profile_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'rooms/index.html')

    def test_update_profile_post_outside(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(self.update_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')

    def test_update_profile_post_occupant(self):
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.post(self.update_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')

    def test_reserve_without_login(self):
        response = self.client.get(self.reserve_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_reserve_outside(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/reserve.html')

    def test_reserve_occupant(self):
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get(self.reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_reserve.html')

    def test_create_reserve_without_login(self):
        response = self.client.get(self.create_reserve_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_create_reserve_outside(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.create_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_reserve.html')

    def test_create_reserve_occupant(self):
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get(self.create_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_reserve.html')

    def test_detail_reserve_without_login(self):
        response = self.client.get(self.detail_reserve_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_detail_reserve_outside(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.detail_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/reserve.html')

    def test_detail_reserve_occupant(self):
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get(self.detail_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_reserve.html')

    def test_delete_reserve_without_login(self):
        response = self.client.get(self.delete_reserve_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_delete_reserve_outside(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.delete_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')

    def test_delete_reserve_occupant(self):
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get(self.delete_reserve_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')

    def test_report(self):
        response = self.client.get(self.report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/report.html')

    def test_create_report_post(self):
        response = self.client.post(self.create_report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_report.html')

    def test_create_report_get(self):
        response = self.client.get(self.create_report_url)

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'occupant/index.html')

    def test_detail_report(self):
        response = self.client.get(self.detail_report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/result_report.html')

    def test_list_report(self):
        response = self.client.get(self.list_report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/list_report.html')

    def test_delete_report(self):
        response = self.client.get(self.delete_report_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'occupant/index.html')


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
        self.assertEquals(self.role.__str__(), self.role.role_name)

    def test_room_type_str(self):
        self.assertEquals(self.room_type.__str__(), self.room_type.class_level)

    def test_room_str(self):
        self.assertEquals(self.room.__str__(
        ), f'#{ self.room.room_number } Class { self.room.room_type }')

    def test_user_info_str(self):
        self.assertEquals(self.user_info.__str__(),
                          f'{ self.new_user.username } { self.role.role_name }')

    def test_status_type_str(self):
        self.assertEquals(self.status_type.__str__(),
                          self.status_type.status_name)

    def test_reserve_str(self):
        self.assertEquals(self.reserve.__str__(
        ), f'Class { self.room_type.class_level } { self.status_type.status_name }')

    def test_problem_type_str(self):
        self.assertEquals(self.problem_type.__str__(),
                          self.problem_type.problem_name)

    def test_report_str(self):
        self.assertEquals(self.report.__str__(
        ), f'{ self.new_user.username } assign { self.problem_type.problem_name } to { self.another_user.username }')
