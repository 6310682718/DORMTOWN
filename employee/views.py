from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
import datetime
from django.contrib.auth.models import User
from occupant.models import UserInfo,Report,StatusType

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)
    else:
        user = User.objects.filter(pk=request.user.id).first()
        user_info = UserInfo.objects.filter(user_id=request.user.id).first()
        role_name = user_info.role_id.role_name
        report_a = Report.objects.filter(assign_to_id=request.user,status_id=StatusType.objects.get(pk=2)).order_by('due_date')
        report_na = Report.objects.filter(assign_to_id__isnull=True).order_by('due_date')
        print("reportna")
        print(report_a)
        rooms_reporter_a = {}
        for report in report_a:
            Object_reporter = UserInfo.objects.get(user_id=report.from_user_id.id)
            reporter_room = Object_reporter.room_id
            rooms_reporter_a.update({report.from_user_id:reporter_room})

        rooms_reporter_na = {}
        for report in report_na:
            Object_reporter = UserInfo.objects.get(user_id=report.from_user_id.id)
            reporter_room = Object_reporter.room_id
            rooms_reporter_na.update({report.from_user_id:reporter_room})
        
        iri=0
        fix=0
        clean=0
        move=0
        for i in report_a:
            print("THISIS I")
            print(i)
            print("THISIS INSIDE")
            print(i.problem_type_id)
            if str(i.problem_type_id) == "Fix electric equipment":
                fix +=1
            elif str(i.problem_type_id) == "Cleaning Service":
                clean +=1
            elif str(i.problem_type_id) == "Irrigation problem":
                iri +=1
            elif str(i.problem_type_id) == "Move Out":
                move +=1
        print(fix)
        print(clean)
        print(move)
       
        if role_name == 'Technician' or 'Housekeeper':
            print("can_access = true")
            can_access = True
        else:
            can_access = False
            print("can_access = false")
        for i in report_na:
            print(i.problem_type_id.problem_name)
        if(can_access):
            return render(request, 'employee/index.html', {
                'user': user,   
                'user_info': user_info,
                'role_name': role_name,
                'report_a' : report_a,
                'report_na' : report_na,
                'fix' :fix,
                'clean' :clean,
                'move' :move,
                'iri' :iri,
                'rooms_reporter_a' :rooms_reporter_a,
                'rooms_reporter_na' :rooms_reporter_na,

            })
        else:    
            return render(request, "rooms/index.html")


def edit_profile(request):
    print("EDIT pROGIEL")
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
    except:
        return render(request, 'rooms/500.html', status=500)

    return render(request, 'employee/edit_profile.html', {
        'user': user,
        'user_info': user_info,
    })

def update_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    if request.method == 'POST':
        try:
            user = User.objects.get(pk=request.user.id)
            user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        except:
            return render(request, 'rooms/500.html', status=500)

        first = request.POST.get('firstname', user.first_name)
        last = request.POST.get('lastname', user.last_name)
        tel = request.POST.get('phoneNumber', user_info.phone_number)
        address = request.POST.get('address', user_info.address)
        street = request.POST.get('street', user_info.street)
        state = request.POST.get('state', user_info.state)
        city = request.POST.get('city', user_info.city)
        country = request.POST.get('country', user_info.country)
        zip_code = request.POST.get('zip', user_info.zip_code)

        User.objects.filter(pk=request.user.id).update(
            first_name =  first,
            last_name = last,
        )

        UserInfo.objects.filter(user_id=user).update(
            phone_number = tel,
            address = address,
            street = street,
            state = state,
            city = city,
            country = country,
            zip_code = zip_code
        )
        print("hello BBBBBIIIIIIITTTTTTEEEEEEECCCCCHHHHHHHH")
        return redirect(reverse('employee:index'))
    else:
        return render(request, 'rooms/404.html', status=404)

def submit(request,report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        report = Report.objects.get(pk=report_id)
        assign_to = report.assign_to_id
        due_date = report.due_date
        print("THSIS")  
        print(report.from_user_id.id)      
        reporter = UserInfo.objects.get(user_id=report.from_user_id.id)
        print("THSIS Reporter") 
        print(reporter)
        reporter_room = reporter.room_id
        print("THSIS ReporterRoom") 
        print(reporter_room)
        reporter_contact = reporter.phone_number
        print("THSIS Reportercontact")    
        print(reporter_contact)     
        
    except:
        return render(request, 'rooms/500.html', status=500)
    
    return render(request, 'employee/submit.html', {
        'user': user,
        'user_info': user_info,
        'report': report,
        'assign_to': assign_to,
        'due_date': due_date,
        'reporter_room': reporter_room,
        'reporter_contact': reporter_contact,
        })

def assign(request,report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        report = Report.objects.get(pk=report_id)
        assign_to = report.assign_to_id
        due_date = report.due_date
        #print("THSIS")  
        #print(report.from_user_id.id)      
        reporter = UserInfo.objects.get(user_id=report.from_user_id.id)
        #print(reporter)
        reporter_room = reporter.room_id
        #print(reporter_room)
        reporter_contact = reporter.phone_number

    except:
        return render(request, 'rooms/500.html', status=500)
    
    return render(request, 'employee/assign.html', {
        'user': user,
        'user_info': user_info,
        'report': report,
        'assign_to': assign_to,
        'due_date': due_date,
        'reporter_room': reporter_room,
        'reporter_contact': reporter_contact,
        
        })
    
def get_assign(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        report = Report.objects.get(pk=report_id)
    
    except:
        return render(request, 'rooms/404.html', status=404)

    report.assign_to_id=user
    report.status_id=StatusType.objects.get(pk=2)
    report.save()
    
    return redirect(reverse('employee:index'))

def get_submit(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        report = Report.objects.get(pk=report_id)
    
    except:
        return render(request, 'rooms/404.html', status=404)

    report.assign_to_id=user
    report.status_id=StatusType.objects.get(pk=3)
    report.save()
    
    return redirect(reverse('employee:index'))