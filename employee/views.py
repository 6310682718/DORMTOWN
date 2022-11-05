from django.shortcuts import render

# Create your views here.

def index(request, user_id):
    detail = {
        'employee': {
            'name': 'Kantapat Kowadisai',
            'Tel': '0897827356',
            'Address': '9330 W Lake Dr ## A, Eagle River, Alaska 99577, USA'}        
        }
    
    return render(request, "employee/index.html", detail)

def submit(rq):
    detail = {
        'report_id': {
            'name': 'Cleaning Service',
            'room': '3401',
            'Tel': '0897827356',
            'Duedate': '9330 W Lake Dr ## A, Eagle River, Alaska 99577, USA',
            'assign_to_user_id':'0001',
            }        
        }
    return render(rq, "employee/submit.html")

def assign(rq):
    detail = {
        'report_id': {
            'name': 'Cleaning Service',
            'room': '3401',
            'Tel': '0897827356',
            'Duedate': '9330 W Lake Dr ## A, Eagle River, Alaska 99577, USA',
            'assign_to_user_id':'0001',
            }        
        }
    return render(rq, "employee/assign.html")

