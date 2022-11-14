from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message, Room
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser == False)
def index(req):
    chat_room, is_created = ChatRoom.objects.get_or_create(room_name=f"room-{req.user.id}")
    messages = Message.objects.filter(room=chat_room)
    return render(req, "chat/index.html", {
        "messages": messages
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def chat_log(req, user_id):
    try:
        room_name = f"room-{user_id}"
        chat_room, is_created = ChatRoom.objects.get_or_create(room_name=room_name)
        messages = Message.objects.filter(room=chat_room)
        text_to_admin = Message.objects.order_by().values_list('user', flat=True).distinct()
        text_to = User.objects.get(id=user_id)
        text_arr = []
        for i in text_to_admin:
            user = User.objects.get(id=i)
            if(user.is_superuser == False):
                text_arr.append(user)
        return render(req, "chat/chat_log.html", {
            "text_to": text_to,
            "messages": messages,
            "only_texter" : text_arr,
            "message_count": len(messages)
        })
    except Exception as e:
        print(f"<-- ERROR {e} -->")


