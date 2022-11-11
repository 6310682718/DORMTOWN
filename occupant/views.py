from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import datetime
from .models import *

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
    except:
        return render(request, 'rooms/500.html', status=500)

    return render(request, 'occupant/index.html', {
        'user': user,
        'user_info': user_info,
    })

def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
    except:
        return render(request, 'rooms/500.html', status=500)

    return render(request, 'occupant/edit_profile.html', {
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

        return redirect(reverse('occupant:index'))
    else:
        return render(request, 'rooms/404.html', status=404)

def reserve(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    rooms = RoomType.objects.all()
    for room in rooms:
        rooms_by_type = Room.objects.filter(room_type=room, status=True)
        room.available = (rooms_by_type.count() > 0)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        reserve = Reserve.objects.filter(user_id=user).first()
    except:
        return render(request, 'rooms/500.html', status=500)

    if reserve is None:
        return render(request, 'occupant/reserve.html', {
            'user_info': user_info,
            'rooms': rooms
        })
    else:
        return redirect(reverse('occupant:get_reserve'))

def create_reserve(request, room_type):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.filter(pk=request.user.id).first()
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        reserve = Reserve.objects.filter(user_id=user).first()
    except:
        return render(request, 'rooms/500.html', status=500)

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

    role = Role.objects.get(role_name='Manager')
    managers = UserInfo.objects.filter(role_id=role)

    return render(request, 'occupant/result_reserve.html', {
        'user_info': user_info,
        'room': reserve.room_type,
        'reserve_id': reserve.id,
        'header': 'Summary of Reservation',
        'managers': managers
    })

def get_reserve(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        reserve = Reserve.objects.filter(user_id=user).first()
    except:
        return render(request, 'rooms/500.html', status=500)

    role = Role.objects.get(role_name='Manager')
    managers = UserInfo.objects.filter(role_id=role)

    if reserve is not None:
        return render(request, 'occupant/result_reserve.html', {
            'user_info': user_info,
            'room': reserve.room_type,
            'reserve_id': reserve.id,
            'header': 'List of Reservation',
            'managers': managers
        })
    else:
        return redirect(reverse('occupant:reserve'))

def delete_reserve(request, reserve_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    reserve = Reserve.objects.filter(pk=reserve_id, user_id=request.user).first()

    if reserve is not None:
        reserve.delete()

    return redirect(reverse('occupant:index'))

def report(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        problem_type = ProblemType.objects.all()
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
    except:
        return render(request, 'rooms/500.html', status=500)

    return render(request, 'occupant/report.html', {
        'user_info': user_info,
        'problems': problem_type
    })

def create_report(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    if request.method == 'POST':
        if request.POST.get('problem', None) is None:
            return redirect(reverse('occupant:report'))

        problem = request.POST.get('problem', None)
        due_date = request.POST.get('due_date', datetime.datetime.today())
        note = request.POST.get('note', None)

        user = User.objects.get(id=request.user.id)
        problem_type = ProblemType.objects.get(problem_name=problem)
        status = StatusType.objects.get(status_name='Idle')

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
        return render(request, 'rooms/404.html', status=404)

def edit_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        report = get_object_or_404(Report, pk=report_id, from_user_id=user)
    except:
        return render(request, 'rooms/404.html', status=404)

    user_info = UserInfo.objects.get(user_id=user)
    problem_type = ProblemType.objects.all()
    report.due_date = report.due_date.strftime(("%Y-%m-%d"))

    return render(request, 'occupant/edit_report.html', {
        'report': report,
        'user_info': user_info,
        'problems': problem_type
    })
    

def update_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    if request.method == 'POST':
        if request.POST.get('problem', None) is None:
            return redirect(reverse('occupant:report'))

        try:
            user = User.objects.get(pk=request.user.id)
            report = get_object_or_404(Report, pk=report_id, from_user_id=user)
        except:
            return render(request, 'rooms/404.html', status=404)

        problem = request.POST.get('problem', report.problem_type_id.problem_name)
        due_date = request.POST.get('due_date', report.due_date)
        note = request.POST.get('note', report.note)

        problem_type = ProblemType.objects.get(problem_name=problem)

        Report.objects.filter(pk=report_id).update(
            problem_type_id=problem_type,
            due_date=due_date,
            note=note
        )
        return redirect(reverse('occupant:list_report'))
    else:
        return render(request, 'rooms/404.html', status=404)

def get_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=user)
        report = Report.objects.get(pk=report_id)
    except:
        return render(request, 'rooms/500.html', status=500)

    return render(request, 'occupant/result_report.html', {
        'report': report,
        'header': 'Summary of Reporting',
        'user_info': user_info
    })

def list_report(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try: 
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=user)
        reports = Report.objects.filter(from_user_id=user).order_by('due_date')
    except:
        return render(request, 'rooms/500.html', status=500)
    
    return render(request, 'occupant/list_report.html', {
        'header': 'List of Report',
        'user_info': user_info,
        'reports': reports
    })

def delete_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        report = get_object_or_404(Report, pk=report_id)
    except:
        return render(request, 'rooms/404.html', status=404)

    report.delete()
    
    return redirect(reverse('occupant:list_report'))