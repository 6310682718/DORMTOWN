from django.http import HttpResponse
from django.shortcuts import render
import datetime

def index(request):
    # homepage of occupant
    return render(request, 'occupant/index.html', {
        'room_status': True
    })

def reserve(request):
    # detail of room to reserve
    room = {
        'A': {
            'detail': 'BRAHHHHHHHHH',
            'available': 2
        },
        'B': {
            'detail': 'BRAHHHHHHHHH',
            'available': 0
        }
    }
    return render(request, 'occupant/reserve.html', {
        'room_status': True,
        'room': room,
        'header': 'Summary of Reservation'
    })

def post_reserve(request, reserve_id):
    # after click reserve button the reserve, check reservation before if none create reservation to db else do not thing, and go to reservation detail
    detail = {
        'employee': {
            'name': 'Natnicha Faksang',
            'Tel': '0644153591',
            'Job': 'Manager'
        },
        'room': {
            'detail': 'BRAHHHHHHHH'
        },
        'room_status': True,
        'header': 'Summary of Reservation'
    }
    return render(request, 'occupant/result_reserve.html', detail)

def list_reserve(request):
    # extract data from db if already reserve get reserve id then go to result_reserve.html
    room = {
        'detail': 'BRAHHHHHHHH',
        'header': 'List of Reservation',
        'room_status': True,
    }

    if room is not None:
        return render(request, 'occupant/result_reserve.html', room)
    else:
        return reserve(request)

def report(request):
    # form to report something
    return render(request, 'occupant/report.html', {
        'room_status': True
    })

def post_report(request, report_id):
    # after fill the form, submit, create to db, then go to summary the report
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
        'room_status': True,
        'header': 'Summary of Reporting'
    }
    return render(request, 'occupant/result_report.html', detail)

def list_report(request):
    lists = {
        'report': {
            'id': 1,
            'title': 'assign_to',
            'date': datetime.date.today(),
        },
        'header': 'List of Report',
        'room_status': True,
    }

    return render(request, 'occupant/list_report.html', lists)
