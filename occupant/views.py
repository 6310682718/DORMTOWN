from django.http import HttpResponse
from django.shortcuts import render
import datetime
from .models import *

def index(request):
    # if did not login return login page
    # if not request.user.is_authenticated:
    #     return render(request, 'users/login.html',status = 400)
    # else return occupant page
    return render(request, 'occupant/index.html', {
        'room_status': False
    })

def reserve(request):
    # if did not login return login detail
    # if not request.user.is_authenticated:
    #     return render(request, 'users/login.html',status = 400)
    # else get detail of room from database then return room detail 
    rooms = RoomType.objects.all()
    rooms_sperated = list()
    for room in rooms:
        rooms_by_type = Room.objects.filter(room_type=room, status=True)

        rooms_sperated.append({
            'room_type': room.class_level,
            'price': room.price,
            'available': rooms_by_type.count()
        })

    print(rooms_sperated)

    return render(request, 'occupant/reserve.html', {
        'room_status': False,
        'rooms': rooms,
        'header': 'Summary of Reservation'
    })

def create_reserve(request, room_type):
    # if did not login return login detail
    # else check reservation before
    # if none create reservation to db then go to reservation detail
    # else return to reservation page
    detail = {
        'employee': {
            'name': 'Natnicha Faksang',
            'Tel': '0644153591',
            'Job': 'Manager'
        },
        'room': {
            'detail': 'BRAHHHHHHHH',
            'type': room_type
        },
        'room_status': False,
        'header': 'Summary of Reservation'
    }
    return render(request, 'occupant/result_reserve.html', detail)

def get_reserve(request):
    # if did not login return login detail
    # else extract data from db
    # if already reserve get reserve id then go to result_reserve.html
    # else return 404 not found
    room = {
        'detail': 'BRAHHHHHHHH',
        'header': 'List of Reservation',
        'room_status': False,
    }

    if room is not None:
        return render(request, 'occupant/result_reserve.html', room)

def delete_reserve(request, reserve_id):
    # if did not login return login detail
    # check reserve_id if valid, delete and return home page
    # else return 404 not found
    return render(request, 'occupant/index.html', {
        'room_status': False
    })

def report(request):
    # if did not login return login detail
    # else return report form
    return render(request, 'occupant/report.html', {
        'room_status': False
    })

def create_report(request):
    # if did not login return login detail
    # else check report form
    # if it is post then go to report detail
    # else return to create report page
    if request.method == 'POST':
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
    else:
        return render(request, 'occupant/index.html', status=400)

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