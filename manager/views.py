from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(req):
    print("User : ", req.user.is_superuser)
    return render(req, "manager/dashboard.html")
