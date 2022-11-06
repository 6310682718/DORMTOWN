from django.shortcuts import render
from django.contrib.auth.models import User
from occupant.models import *

def login(req):
    return render(req, "users/login.html", {})

def register(req):
    return render(req, "users/register.html", {})

def regist(request):
    if request.method == 'POST':
        first = request.POST['firstname']
        last = request.POST['lastname']
        email = request.POST['email']
        tel = request.POST['phoneNumber']
        password = request.POST['password']
        con_pass = request.POST['confirmPassword']

        if password != con_pass:
            return render(request, "users/register.html", {
                'message': 'Password is invalid.',
                'message_tag': "alert alert-danger"
            })

        check_email = User.objects.filter(email=email).first()
        if check_email is not None:
            return render(request, "users/register.html", {
                'message': 'Email in invalid.',
                'message_tag': "alert alert-danger"
            })

        check_tel = UserInfo.objects.filter(phone_number=tel).first()
        if check_tel is not None:
            return render(request, "users/register.html", {
                'message': 'Phon number in invalid.',
                'message_tag': "alert alert-danger"
            })  

        new_user = User.objects.create(
            username = tel,
            first_name = first,
            last_name = last,
            email = email
        )

        # UserInfo.objects.create(
        #     user_id = new_user
        # )

        return render(request, "users/login.html", {})