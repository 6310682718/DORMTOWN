from django.shortcuts import render

# Create your views here.

def login(req):
    return render(req, "users/login.html", {})

def register(req):
    return render(req, "users/register.html", {})