from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    # 1 -> Manager 2 -> Housekeeper 3 -> Technician 4 -> Occupant 5 -> Outside
    role_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{ self.role_name }'


class RoomType(models.Model):
    class_level = models.CharField(max_length=5)
    price = models.IntegerField()
    room_service = models.IntegerField(default=1)
    tv_fridge = models.BooleanField(default=True)
    wardrobe = models.BooleanField(default=True)
    water_heater = models.BooleanField(default=True)

    def __str__(self):
        return f'{ self.class_level }'


class Room(models.Model):
    room_number = models.CharField(max_length=3)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="room_type", default="1")
    # True -> Available for reservation False -> Unavailable for reservation
    status = models.BooleanField()

    def __str__(self):
        return f'#{ self.room_number } Class {self.room_type}'


class UserInfo(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_id", default="1")
    role_id = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="role_id")
    room_id = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room_id", default="1")
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    street = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{ self.user_id.username } { self.role_id.role_name }'


class StatusType(models.Model):
    # 1 -> idle 2 -> Doing 3 -> Done
    status_name = models.CharField(max_length=10)

    def __str__(self):
        return f'{ self.status_name }'


class Reserve(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reserved_user_id", default="1")
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="reserved_room_type")
    due_date = models.DateField()
    create_at = models.DateTimeField()
    status_type = models.ForeignKey(
        StatusType, on_delete=models.CASCADE, related_name="status_type")

    def __str__(self):
        return f'Class { self.room_type.class_level } { self.status_type }'


class ProblemType(models.Model):
    problem_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{ self.problem_name }'


class Report(models.Model):
    from_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user_id", default="1")
    problem_type_id = models.ForeignKey(
        ProblemType, on_delete=models.CASCADE, related_name="problem_type_id", default="1")
    due_date = models.DateField()
    note = models.CharField(max_length=150)
    status_id = models.ForeignKey(
        StatusType, on_delete=models.CASCADE, related_name="status_id", default="1")
    assign_to_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assign_to_id", default="1")
    role_id = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="reported_role_id", default="1")

    def __str__(self):
        return f'{ self.from_user_id.username } assign { self.problem_type_id.problem_name } to { self.assign_to_id.username }'
