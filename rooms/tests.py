from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .views import *
import datetime
# Create your tests here.
class TestUrl(SimpleTestCase):
    def test_index_is_resolved(self):
        # test occupant index url use index method for homepage of user (occupant and outside role)
        url = reverse("rooms:index")
        self.assertEqual(resolve(url).func, index)

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

        self.index_url = reverse('rooms:index')

        
    def test_index_without_login(self):
        # serch occupant homepage without authorization, return login page with 403 Forbidden
        response = self.client.get(self.index_url)
        self.assertTemplateUsed(response, 'rooms/index.html')

    def test_index(self):
        # authorize for occupant homepage with user and userinfo model, return the page with 200 OK
        self.client.login(username=self.occupant_username, password=self.occupant_password)

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms/index.html')
    
    def test_404(self):
        url = "rooms/ssss"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'rooms/404.html')
    
        