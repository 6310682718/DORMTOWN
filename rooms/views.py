from django.shortcuts import render
from occupant.models import *


def index(req):
    if req.user.is_authenticated:    
        user_info = UserInfo.objects.get(user_id=req.user)
        return render(req, "rooms/index.html", {"user_info": user_info})

    return render(req, "rooms/index.html", {})


def handler404(request, exception):
    print(exception)
    
    return render(request, 'rooms/404.html', {})


def handler500(request):
    return render(request, 'rooms/500.html', {})
