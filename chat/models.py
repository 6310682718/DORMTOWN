from django.contrib.auth.models import User
from django.db import models
from occupant.models import Room
class ChatRoom(models.Model):
    user =  models.ForeignKey(User, related_name='chat_room', on_delete=models.CASCADE)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class Meta:
        ordering = ('date_added',)