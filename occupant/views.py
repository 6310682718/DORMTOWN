from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import datetime
from .models import *
import sweetify

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

def reserve(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    rooms = RoomType.objects.all()
    for room in rooms:
        rooms_by_type = Room.objects.filter(room_type=room, status=True)
        room.available = rooms_by_type.count()
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
        room_type = RoomType.objects.filter(pk=room_type).first()
        role = Role.objects.get(role_name='Manager')
        managers = UserInfo.objects.filter(role_id=role)
    except:
        return render(request, 'rooms/500.html', status=500)

    if request.method == 'POST':
        status_type = StatusType.objects.filter(status_name='Idle').first()

        due_date = request.POST.get('due_date')

        reserve = Reserve.objects.create(
            user_id=user,
            room_type=room_type,
            due_date=due_date,
            status_type=status_type
            )

        sweetify.success(request, 'Reserve successful')
        return render(request, 'occupant/result_reserve.html', {
            'user_info': user_info,
            'room': reserve.room_type,
            'reserve_id': reserve.id,
            'header': 'Summary of Reservation',
            'managers': managers
        })
    else:
        return render(request, 'occupant/reserve_form.html', {
            'user_info': user_info,
            'room': room_type
        })

def get_reserve(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        reserve = Reserve.objects.filter(user_id=user).first()
        role = Role.objects.get(role_name='Manager')
        managers = UserInfo.objects.filter(role_id=role)
    except:
        return render(request, 'rooms/500.html', status=500)

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

    sweetify.success(request, 'Remove reservation successful')
    return redirect(reverse('occupant:index'))

def report(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        problem_type = ProblemType.objects.all()
        user = User.objects.get(id=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=user)
    except:
        return render(request, 'rooms/500.html', status=500)

    if request.method == 'POST':
        if request.POST.get('problem', None) is None:
            return redirect(reverse('occupant:report'))

        problem = request.POST.get('problem', None)
        due_date = request.POST.get('due_date', datetime.datetime.today())
        note = request.POST.get('note', None)

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

        sweetify.success(request, 'Create report successful')
        return redirect(reverse('occupant:get_report', args=[report.id]))
    else:
        return render(request, 'occupant/report.html', {
            'user_info': user_info,
            'problems': problem_type
        })

def edit_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = UserInfo.objects.get(user_id=user)
        report = get_object_or_404(Report, pk=report_id, from_user_id=user)
    except:
        return render(request, 'rooms/404.html', status=404)

    if request.method == 'POST':
        if request.POST.get('problem', None) is None:
            return redirect(reverse('occupant:report'))

        problem = request.POST.get('problem', report.problem_type_id.problem_name)
        due_date = request.POST.get('due_date', report.due_date)
        note = request.POST.get('note', report.note)

        problem_type = ProblemType.objects.get(problem_name=problem)

        Report.objects.filter(pk=report_id).update(
            problem_type_id=problem_type,
            due_date=due_date,
            note=note
        )

        sweetify.success(request, 'Edit report successful')
        return redirect(reverse('occupant:list_report'))
    else:
        problem_type = ProblemType.objects.all()
        report.due_date = report.due_date.strftime(("%Y-%m-%d"))

        return render(request, 'occupant/edit_report.html', {
            'report': report,
            'user_info': user_info,
            'problems': problem_type
        })

def get_report(request, report_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = get_object_or_404(UserInfo, user_id=user)
        report = Report.objects.get(pk=report_id, from_user_id=user)
        assign_to_user_info = UserInfo.objects.filter(user_id=report.assign_to_id).first()
        role = Role.objects.get(role_name='Manager')
        managers = UserInfo.objects.filter(role_id=role)
    except:
        return render(request, 'rooms/500.html', status=500)

    return render(request, 'occupant/result_report.html', {
        'report': report,
        'header': 'Summary of Reporting',
        'user_info': user_info,
        'assign_to_user_info': assign_to_user_info,
        'managers': managers
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
        report = get_object_or_404(Report, pk=report_id, from_user_id=user)
    except:
        return render(request, 'rooms/404.html', status=404)

    report.delete()
    
    sweetify.success(request, 'Delete report successful')
    return redirect(reverse('occupant:list_report'))