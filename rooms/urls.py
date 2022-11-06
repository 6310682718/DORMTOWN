from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.index, name='index'),
    path('404', views.handler404, name="404")
]
