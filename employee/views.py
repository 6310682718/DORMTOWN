from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.contrib.auth.models import User
# from ..occupant.models import *
from occupant.models import UserInfo,Report, StatusType

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)
    else:
        user = User.objects.filter(pk=request.user.id).first()
        user_info = UserInfo.objects.filter(user_id=request.user.id).first()
        role_name = user_info.role_id.role_name
        #status_type, status_type_created = StatusType.objects.get_or_create(status_name="idle")
        report = Report.objects.filter(assign_to_id=request.user)

        print("Reports : ", report)
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
                'report' : report,
            })
        else:    
            return render(request, "rooms/index.html")

