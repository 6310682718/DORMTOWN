from django.shortcuts import render
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
        user = User.objects.filter(pk=request.user.id).first()

        UserInfo.objects.filter(user_id=user).update(
            phone_number = tel,
            address = address,
            street = street,
            state = state,
            city = city,
            country = country,
            zip_code = zip_code
        )
        user_info = UserInfo.objects.filter(user_id=user).first()

        if user_info.role_id.role_name == 'Occupant':
            room_status = True
        else:
            room_status = False

        return render(request, 'occupant/index.html', {
            'room_status': room_status,
            'user': user,
            'user_info': user_info,
        })
    else:
        return render(request, 'rooms/index.html', status=400)

def reserve(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=400)

    rooms = RoomType.objects.all()
    rooms_sperated = list()
    for room in rooms:
        rooms_by_type = Room.objects.filter(room_type=room, status=True)

        rooms_sperated.append({
            'room': room,
            'available': (rooms_by_type.count() > 0)
        })

    user = User.objects.filter(email=request.user.email).first()
    reserve = Reserve.objects.filter(user_id=user).first()
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

    user = User.objects.filter(email=request.user.email).first()
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
        rooms = RoomType.objects.all()
        rooms_sperated = list()
        for room in rooms:
            rooms_by_type = Room.objects.filter(room_type=room, status=True)

            rooms_sperated.append({
                'room': room,
                'available': (rooms_by_type.count() > 0)
            })

        return render(request, 'occupant/reserve.html', {
            'room_status': room_status,
            'rooms': rooms,
        })

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
        problem_type = ProblemType.objects.first()

        problem = request.POST.get('problem', problem_type)
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

        user_info = UserInfo.objects.filter(user_id=request.user.id).first()
        if user_info.role_id.role_name == 'Occupant':
            room_status = True
        else:
            room_status = False

        return render(request, 'occupant/result_report.html', {
            'report': report,
            'room_status': room_status,
            'user_info': user_info,
            'header': 'Summary of Reporting'
        })
    else:
        return render(request, 'occupant/index.html', status=400)

def update_report(request):
    pass

def get_report(request, report_id):
    # if did not login return login detail
    # else extract data from db
    # if already report get report id then go to result_report.html
    # else return 404 not found
    detail = {
        'report': {
            'problem': 'room service',
            'date': datetime.date.today(),
            'note': 'Do not stole my stuff'
        },
        'employee': {
            'name': 'Natnicha Faksang',
            'Tel': '0644153591',
            'Job': 'Housekeeper'
        },
        'room_status': False,
        'header': 'Summary of Reporting'
    }

    return render(request, 'occupant/result_report.html', detail)

def list_report(request):
    # if did not login return login detail
    # else extract all report of the usert from db then return list report page
    lists = {
        'report': {
            'id': 1,
            'title': 'assign_to',
            'date': datetime.date.today(),
        },
        'header': 'List of Report',
        'room_status': False,
    }

    return render(request, 'occupant/list_report.html', lists)

def delete_report(request, report_id):
    # if did not login return login detail
    # check report_id if valid, delete and return home page
    # else return 404 not found
    return render(request, 'occupant/index.html', {
        'room_status': False
    })