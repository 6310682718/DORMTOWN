from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from occupant.models import *
from django.db.models import Q
from django.urls import reverse

# Create your views here.


@login_required
def index(req):
    if req.user.is_authenticated:    
        user_info = UserInfo.objects.get(user_id=req.user)
        rooms_available = Room.objects.filter(status=True)
        rooms_unavailable = Room.objects.filter(status=False)
        return render(req, "manager/dashboard.html", {"user_info": user_info, "rooms_a": rooms_available, "rooms_b": rooms_unavailable})
    return render(req, "manager/dashboard.html")

def rooms_available(req):
    
    try:
        rooms = Room.objects.filter(status=True)
    except:
        pass
    return render(req, "manager/available_rooms.html", {"rooms": rooms})

def rooms_reserve(req):
    return render(req, "manager/reserve_rooms.html")

def rooms_unavailable(req):
    try:
        rooms = Room.objects.filter(status=False)
    except:
        pass
    return render(req, "manager/unavailable_rooms.html", {"rooms": rooms})

def employee_list(req):
    try:
        user_info = UserInfo.objects.filter(Q(role_id=2) | Q(role_id = 3))
    except:
        pass
    return render(req, "manager/employee_list.html", {"user_info": user_info})

def occupant_list(req):
    try:
        user_info = UserInfo.objects.filter(Q(role_id=4) | Q(role_id = 5))
    except:
        pass
    return render(req, "manager/employee_list.html", {"user_info": user_info})

def report_logs(req):
    try:
        reports = Report.objects.all()
    except:
        pass
    return render(req, "manager/report_logs.html", {"reports": reports})

def edit_profile(request, user_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)
    try:
        user = User.objects.get(pk=user_id)
        user_info = get_object_or_404(UserInfo, user_id=user)
    except:
        return render(request, 'rooms/500.html', status=500)

    return render(request, 'users/edit_profile.html', {
        'user': user,
        'user_info': user_info,
    })

def delete_user(request, user_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=user_id)
        user_info = get_object_or_404(UserInfo, user_id=user)
    except:
        return render(request, 'rooms/500.html', status=500)

    if user is not None:
        user.delete()

    return redirect(reverse('manager:dashboard'))