from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from occupant.models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password

def login(req):
    if (req.method == "POST"):
        username = req.POST.get("username", False)
        password = req.POST.get("password", False)
        user = authenticate(req, username=username, password=password)
        try:
            # find role and return to right path plz
            if (user is not None):
                user_info = UserInfo.objects.filter(user_id=user).first()
                auth_login(req, user)
                return redirect(reverse('rooms:index'))
            else:
                return render(req, "users/login.html", {"message": "Invalid credential"}, status=400)
        except Exception as e:
            pass
    return render(req, "users/login.html")

def logout(req):
    auth_logout(req)
    return render(req, "users/login.html", {"message": "Logged out"})

def register(req):
    if req.method == "POST":
        username = req.POST["email"]
        firstname = req.POST["firstname"]
        lastname = req.POST["lastname"]
        password = req.POST["password"]
        email = req.POST["email"]
        con_password = req.POST.get("confirmPassword", False)
        phone = req.POST.get("phoneNumber", False)
        address = req.POST.get("address", False)
        street = req.POST.get("street", False)
        city = req.POST.get("city", False)
        state = req.POST.get("state", False)
        country = req.POST.get("country", False)
        zip = req.POST.get("zip", False)
        try:
            _user = User.objects.get(email=email)
            return render(req, "users/register.html", {"status": False, "message": "Username already used"}, status=400)
        except:
            pass
            # print("<--- User not found (Can register) --->")
        if (con_password != password):
            return render(req, "users/register.html", {"status": False, "message": "Confirm password fail"}, status=400)
        if (username == "" or len(username) == 0 or firstname == "" or lastname == "" or password == "" or con_password == "" or email == ""):
            return render(req, "users/register.html", {"status": False, "message": "Enter your information"}, status=400)
        role = Role.objects.get(role_name="Outside")
        rooms = Room.objects.first()
        user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
        user_info = UserInfo.objects.create(user_id=user, phone_number=phone, address=address, street=street, state=state, city=city, country=country, zip_code=zip, role_id=role, room_id=rooms)
        return render(req, "users/login.html", {"status": True, "message": "Register Success"}, status=200)
    else:
        return render(req, "users/register.html", status=200)

def change_pass(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', status=403)

    try:
        user = User.objects.get(pk=request.user.id)
        user_info = UserInfo.objects.get(user_id=user)
    except:
        return render(request, 'rooms/500.html', status=500)

    if (request.method == "POST"):
        old_password = request.POST['old_pass']
        new_password = request.POST['new_password']
        con_password = request.POST['con_password']

        if (new_password != con_password) or (not user.check_password(old_password)):
            return render(request, 'users/changepass.html', {
                'message': 'Password is invalid.',
                'message_tag': 'alert alert-danger'
            })
        
        user.set_password(new_password)
        user.save()

        return redirect(reverse('users:login'))
    else:
        return render(request, "users/changepass.html", {
            'user_info': user_info
        })
