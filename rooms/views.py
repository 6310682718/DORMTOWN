from django.shortcuts import render

# Create your views here.


def index(req):
    # require only admin
    return render(req, "rooms/index.html", {})


def handler404(request, exception):
    print("<-- 404 -->")
    response = render(request, '404.html', {}, status=404)
    # response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {}, status=500)
    # response.status_code = 500
    return response
