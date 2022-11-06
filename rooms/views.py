from django.shortcuts import render

# Create your views here.


def index(req):
    # require only admin
    return render(req, "rooms/index.html", {})
