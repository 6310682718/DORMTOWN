from django.contrib import admin
from .models import *

class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name']

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['class_level', 'price']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'status']

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'role_id', 'room_id', 'phone_number', 'address', 'street', 'state', 'city', 'country', 'zip_code']

class StatusTypeAdmin(admin.ModelAdmin):
    list_display = ['status_name']

class ReserveAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'room_type', 'due_date', 'create_at', 'status_type']

class ProblemTypeAdmin(admin.ModelAdmin):
    list_display = ['problem_name']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['from_user_id', 'problem_type_id', 'due_date', 'note', 'status_id', 'assign_to_id', 'role_id']

admin.site.register(Role, RoleAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(StatusType, StatusTypeAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(ProblemType, ProblemTypeAdmin)
admin.site.register(Report, ReportAdmin)