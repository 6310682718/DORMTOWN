from django.contrib import admin
from .models import *
# Register your models here.

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['room_name']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'content', 'date_added']


admin.site.register(Message, MessageAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)