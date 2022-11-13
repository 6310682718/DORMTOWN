from django.shortcuts import render
from occupant.models import *

# Create your views here.


def index(req):
    try:
        if req.user.is_authenticated:    
            user_info = UserInfo.objects.get(user_id=req.user)
            return render(req, "rooms/index.html", {"user_info": user_info})
    except:
        return render(req, "rooms/index.html", {})


def handler404(request, exception):
    print("<-- 404 -->")
    response = render(request, 'rooms/404.html', {}, status=404)
    return response


def handler500(request):
    response = render(request, 'rooms/500.html', {}, status=500)
    return response
