from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import *

# Create your views here.

def index(request):
    detail = {
        'employee': {
            'name': 'Kantapat Kowadisai',
            'Tel': '0897827356',
            'Address': '9330 W Lake Dr ## A, Eagle River, Alaska 99577, USA'}        
        }
    
    return render(request, "employee/index.html", detail)

def submit(rq):
    detail = {
        'report': {
            'name': 'Cleaning Service',
            'room': '3401',
            'Tel': '0897827356',
            'Duedate': '01/02/2022',
            'assign_to_user_id':'0001',
            'id' : '0001',
            }        
    }
    return render(rq, "employee/submit.html",detail)

def assign(rq):
    detail = {
        'report_id': {
            'name': 'Cleaning Service',
            'room': '3401',
            'Tel': '0897827356',
            'Duedate': '01/02/2022',
            'assign_to_user_id':'0001',
            'id' : '0001',
            }        
        }
    return render(rq, "employee/assign.html",detail)


