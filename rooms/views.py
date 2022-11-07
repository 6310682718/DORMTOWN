from django.shortcuts import render

# Create your views here.


def index(req):
    # require only admin
    return render(req, "rooms/index.html", {})


def handler404(request, exception):
    print("<-- 404 -->")
    response = render(request, 'rooms/404.html', {}, status=404)
    return response


def handler500(request):
    response = render(request, 'rooms/500.html', {}, status=500)
    return response
