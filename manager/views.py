from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from occupant.models import *
from django.db.models import Q
from django.urls import reverse
import sweetify


# Create your views here.


def index(req):
    if req.user.is_authenticated:    
        user_info = UserInfo.objects.get(user_id=req.user)
        rooms_available = Room.objects.filter(status=True)
        rooms_unavailable = Room.objects.filter(status=False)
        status_type = StatusType.objects.filter(status_name='Idle').first()
        rooms_reserve = Reserve.objects.filter(status_type=status_type)
        return render(req, "manager/dashboard.html", {"user_info": user_info, "rooms_a": rooms_available, "rooms_b": rooms_unavailable, "rooms_s": rooms_reserve})
    return render(req, "manager/dashboard.html")

def rooms_available(req):
    rooms = Room.objects.filter(status=True)
    return render(req, "manager/available_rooms.html", {"rooms": rooms})

def rooms_reserve(req):
    status_type = StatusType.objects.filter(status_name='Idle').first()
    rooms = Reserve.objects.filter(status_type=status_type)
    num_rooms = Room.objects.filter(status=True)
    return render(req, "manager/reserve_rooms.html", {"rooms": rooms, "num_rooms": num_rooms})

def rooms_unavailable(req):
    rooms = Room.objects.filter(status=False)
    return render(req, "manager/unavailable_rooms.html", {"rooms": rooms})

def employee_list(req):
    user_info = UserInfo.objects.filter(Q(role_id=2) | Q(role_id = 3))
    return render(req, "manager/employee_list.html", {"user_info": user_info})

def occupant_list(req):
    user_info = UserInfo.objects.filter(Q(role_id=4))
    return render(req, "manager/occupant_list.html", {"user_info": user_info})

def report_logs(req):
    reports = Report.objects.all()
    return render(req, "manager/report_logs.html", {"reports": reports})

def edit_profile(request, user_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)
    else:
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
        sweetify.success(request, "Deleted", button=True)
    return render(request, 'manager/dashboard.html')

def approve_reservation(req, user_id):
    user = User.objects.filter(pk=user_id).first()
    user_info = get_object_or_404(UserInfo, user_id=user)
    if (req.method == "POST"):
        status_type = StatusType.objects.filter(status_name='Done').first()
        room = req.POST.get('room', None)
        room_id = Room.objects.filter(room_number=room).first()
        user_info.room_id = room_id
        user_info.save()
        reservetion = Reserve.objects.filter(user_id=user_id).first()
        reservetion.status_type = status_type
        reservetion.save()
        return render(req, 'manager/reserve_rooms.html')


