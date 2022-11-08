from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import datetime
from .models import *

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.filter(pk=request.user.id).first()
    user_info = UserInfo.objects.filter(user_id=request.user.id).first()

    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    return render(request, 'occupant/index.html', {
        'room_status': room_status,
        'user': user,
        'user_info': user_info,
    })

def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.filter(pk=request.user.id).first()
    user_info = UserInfo.objects.filter(user_id=request.user.id).first()

    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    return render(request, 'occupant/edit_profile.html', {
        'room_status': room_status,
        'user': user,
        'user_info': user_info,
    })

def update_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    if request.method == 'POST':
        user = User.objects.filter(pk=request.user.id).first()
        user_info = UserInfo.objects.filter(user_id=user).first()

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

        return redirect(reverse('occupant:index'))
    else:
        return render(request, 'rooms/index.html', status=400)

def reserve(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    rooms = RoomType.objects.all()
    for room in rooms:
        rooms_by_type = Room.objects.filter(room_type=room, status=True)
        room.available = (rooms_by_type.count() > 0)

    user = User.objects.filter(pk=request.user.id).first()
    user_info = UserInfo.objects.filter(user_id=request.user.id).first()
    reserve = Reserve.objects.filter(user_id=user).first()

    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    if reserve is None:
        return render(request, 'occupant/reserve.html', {
            'room_status': room_status,
            'rooms': rooms,
        })
    else:
        return render(request, 'occupant/result_reserve.html', {
            'room_status': room_status,
            'room': reserve.room_type,
            'header': 'List of Reservation',
            "reserve_id": reserve.id
        })

def create_reserve(request, room_type):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.filter(pk=request.user.id).first()
    user_info = UserInfo.objects.filter(user_id=request.user.id).first()

    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    reserve = Reserve.objects.filter(user_id=user).first()
    if reserve is None:
        room_type = RoomType.objects.filter(pk=room_type).first()
        status_type = StatusType.objects.filter(pk=1).first()

        reserve = Reserve.objects.create(
            user_id=user,
            room_type=room_type,
            due_date=datetime.datetime.today(),
            create_at=datetime.datetime.now(),
            status_type=status_type
        )

    return render(request, 'occupant/result_reserve.html', {
        'room_status': room_status,
        'room': reserve.room_type,
        'reserve_id': reserve.id,
        'header': 'Summary of Reservation'
    })

def get_reserve(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.filter(id=request.user.id).first()
    user_info = UserInfo.objects.filter(user_id=request.user.id).first()

    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    reserve = Reserve.objects.filter(user_id=user).first()

    if reserve is not None:
        return render(request, 'occupant/result_reserve.html', {
            'room_status': room_status,
            'room': reserve.room_type,
            'reserve_id': reserve.id,
            'header': 'List of Reservation'
        })
    else:
        return redirect(reverse('occupant:reserve'))

def delete_reserve(request, reserve_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    reserve = Reserve.objects.filter(pk=reserve_id, user_id=request.user)

    if reserve is not None:
        reserve.delete()

    return index(request)

def report(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    problem_type = ProblemType.objects.all()

    user_info = UserInfo.objects.filter(user_id=request.user.id).first()
    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    return render(request, 'occupant/report.html', {
        'room_status': room_status,
        'problems': problem_type
    })

def create_report(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    if request.method == 'POST':
        if request.POST.get('problem', None) is None:
            return redirect(reverse('occupant:report'))

        problem = request.POST.get('problem', None)
        due_date = request.POST.get('due_date', datetime.datetime.today())
        note = request.POST.get('note', None)

        user = User.objects.filter(id=request.user.id).first()
        problem_type = ProblemType.objects.filter(problem_name=problem).first()
        status = StatusType.objects.filter(status_name='Idle').first()

        report = Report.objects.create(
            from_user_id=user,
            problem_type_id=problem_type,
            due_date=due_date,
            note=note,
            status_id=status,
            assign_to_id=None,
            role_id=None
        )

        return redirect(reverse('occupant:get_report', args=[report.id]))
    else:
        return render(request, 'occupant/index.html', status=400)

def edit_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.filter(pk=request.user.id).first()
    report = get_object_or_404(Report, pk=report_id, from_user_id=user)
    report.due_date = report.due_date.strftime(("%Y-%m-%d"))

    if report is None:
        return redirect(reverse('occupant:index'))

    user_info = UserInfo.objects.filter(user_id=user).first()
    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    problem_type = ProblemType.objects.all()

    return render(request, 'occupant/edit_report.html', {
        'report': report,
        'room_status': room_status,
        'problems': problem_type
    })
    

def update_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    if request.method == 'POST':
        if request.POST.get('problem', None) is None:
            return redirect(reverse('occupant:report'))

        user = get_object_or_404(User, pk=request.user.id)
        report = get_object_or_404(Report, pk=report_id, from_user_id=user)

        problem = request.POST.get('problem', report.problem_type_id.problem_name)
        due_date = request.POST.get('due_date', report.due_date)
        note = request.POST.get('note', report.note)

        problem_type = ProblemType.objects.filter(problem_name=problem).first()

        Report.objects.filter(pk=report_id, from_user_id=user).update(
            problem_type_id=problem_type,
            due_date=due_date,
            note=note
        )

        return redirect(reverse('occupant:list_report'))
    else:
        return redirect(reverse('occupant:index'))

def get_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.get(pk=request.user.id)
    user_info = UserInfo.objects.filter(user_id=user).first()
    report = Report.objects.filter(pk=report_id, from_user_id=user).first()

    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    return render(request, 'occupant/result_report.html', {
        'report': report,
        'room_status': room_status,
        'header': 'Summary of Reporting',
        'user_info': user_info
    })

def list_report(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.filter(pk=request.user.id).first()
    user_info = UserInfo.objects.filter(user_id=user).first()
    reports = Report.objects.filter(from_user_id=user).order_by('creation_time')

    if user_info.role_id.role_name == 'Occupant':
        room_status = True
    else:
        room_status = False

    return render(request, 'occupant/list_report.html', {
        'header': 'List of Report',
        'room_status': room_status,
        'reports': reports
    })

def delete_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    user = User.objects.get(pk=request.user.id)
    report = Report.objects.filter(pk=report_id, from_user_id=user).first()

    if report is None:
        return redirect(reverse('occupant:index'))

    report.delete()
    
    return redirect(reverse('occupant:list_report'))