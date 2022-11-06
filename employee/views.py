from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import *

# Create your views here.

def index(request):   
    return render(request, "employee/index.html")

def submit(rq):
    return render(rq, "employee/submit.html")

def assign(rq):
    return render(rq, "employee/assign.html")


