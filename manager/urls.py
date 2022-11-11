from manager import views
from django.urls import path

app_name = "manager"
urlpatterns = [
    path("", views.index, name="dashboard"),
    path("rooms_available", views.rooms_available, name="rooms_available")
]
