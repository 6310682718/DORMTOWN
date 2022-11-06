from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from occupant.models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def login(req):
    if (req.method == "POST"):
        username = req.POST.get("username", False)
        password = req.POST.get("password", False)
        user = authenticate(req, username=username, password=password)
        login_user = User.objects.get(username=username)
        user_info = UserInfo.objects.get(user_id=login_user.id)
        print(user_info.role_id)

        # find role and return to right path plz

        if (user is not None):
            auth_login(req, user)
            if (user_info.role_id == "Outside" or user_info.role_id == "Occupant"):
                print("++++++++++")
                return redirect("/occupant/")
            if (user_info.role_id == "Manager"):
                return redirect("/manager/dashboard")
        else:
            return render(req, "users/login.html", {"message": "Invalid credential"}, status=400)
    return render(req, "users/login.html")

def logout(req):
    auth_logout(req)
    return render(req, "users/login.html", {"message": "Logged out"})

def register(req):
    obj = {
        "status": True,
        "message": ""
    }
    if req.method == "POST":
        username = req.POST["email"]
        firstname = req.POST["firstname"]
        lastname = req.POST["lastname"]
        password = req.POST["password"]
        email = req.POST["email"]
        con_password = req.POST.get("confirmPassword", False)
        phone = req.POST["phoneNumber"]
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
            obj['status'] = False
            obj["message"] = "Confirm password fail"
        if (username == "" or len(username) == 0 or firstname == "" or lastname == "" or password == "" or con_password == "" or email == ""):
            obj["status"] = False
            obj["message"] = "Enter your information"

            # when regist new user user info did not create anything

        # Register Process
        if (obj["status"]):
            obj['message'] = "Register successfully"
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=firstname, last_name=lastname)
            user_info = UserInfo.objects.create(
                user_id=user, phone_number=phone, address=address, street=street, state=state, city=city, country=country, zip_code=zip
            )
            return render(req, "users/login.html", {"status": True, "message": obj["message"]}, status=200)
        else:
            return render(req, "users/register.html", {"status": False, "message": obj["message"]}, status=400)
    return render(req, "users/register.html", obj, status=200)
