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
    print("Messages : ", messages)
    return render(req, "chat/index.html", {"messages": messages})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def chat_list(req, user_id):
    # For admin only
    try:
        room_name = f"room-{user_id}"
        chat_room, is_created = ChatRoom.objects.get_or_create(room_name=room_name)
        messages = Message.objects.filter(room=chat_room)
        print("Messages chat list : ", messages)
        return render(req, "chat/chat_list.html", {"messages": messages})
    except Exception as e:
        print(f"<-- ERROR {e} -->")

# def rooms(request):
#     rooms = Room.objects.all()

#     return render(request, 'chat/rooms.html', {'rooms': rooms})

# def room(request, room_number):
#     print("<---- Room Page --->")
#     try:
#         room = Room.objects.get(room_number=room_number)
#         messages = Message.objects.filter(room=room)[0:25]

#         return render(request, 'chat/room.html', {'room': room, 'messages': messages})
#     except Exception as e:
#         print("Error from get room : ", e)
#     obj = {
#         "room_number": 0,
#         "room_type": {
#             "class_level": "A",
#             "price": 6500,
#             "room_service": 1
#         },
#         "status": True
#     }
#     return render(request, "chat/room.html", {"room": obj, "messages": []})