from django.contrib.auth.models import User
from django.db import models
from occupant.models import Room
class ChatRoom(models.Model):
    room_name = models.CharField(max_length=10, default="all-rooms")


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class Meta:
    ordering = ('date_added',)