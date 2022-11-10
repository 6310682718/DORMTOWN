from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.contrib.auth.models import User
# from ..occupant.models import *
from occupant.models import UserInfo,Report

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)
    else:
        user = User.objects.filter(pk=request.user.id).first()
        user_info = UserInfo.objects.filter(user_id=request.user.id).first()
        role_name = user_info.role_id.role_name
        report_a = Report.objects.filter(assign_to_id=request.user)
        print("REPORT_A -----")
        print(report_a)
        report_na = Report.objects.filter(assign_to_id__isnull=True)
        print("REPORT_NA -----")
        print(report_na)

        if role_name == 'Technician' or 'Housekeeper':
            print("can_access = true")
            can_access = True
        else:
            can_access = False
            print("can_access = false")

        if(can_access):
            return render(request, 'employee/index.html', {
                'user': user,
                'user_info': user_info,
                'role_name': role_name,
                'report_a' : report_a,
                'report_na' : report_na,
            })
        else:    
            return render(request, "rooms/index.html")

