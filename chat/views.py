from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Room, Message

@login_required
def index(req):
    messages = Message.objects.filter(user=req.user)
    print("Messages : ", messages)
    return render(req, "chat/index.html", {"messages": messages})

def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'chat/rooms.html', {'rooms': rooms})

def room(request, room_number):
    print("<---- Room Page --->")
    try:
        room = Room.objects.get(room_number=room_number)
        messages = Message.objects.filter(room=room)[0:25]

        return render(request, 'chat/room.html', {'room': room, 'messages': messages})
    except Exception as e:
        print("Error from get room : ", e)
    obj = {
        "room_number": 0,
        "room_type": {
            "class_level": "A",
            "price": 6500,
            "room_service": 1
        },
        "status": True
    }
    return render(request, "chat/room.html", {"room": obj, "messages": []})