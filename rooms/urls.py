from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.index, name='index'),
    path('404.html/<str:exception>', views.handler404, name='handler404'),
    path('500.html', views.handler500, name='handler500'),
]