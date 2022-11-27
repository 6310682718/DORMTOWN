from manager import views
from django.urls import path

app_name = "manager"
urlpatterns = [
    path("", views.index, name="dashboard"),
    path("rooms_available", views.rooms_available, name="rooms_available"),
    path("rooms_reserve", views.rooms_reserve, name="rooms_reserve"),
    path("rooms_unavailable", views.rooms_unavailable, name="rooms_unavailable"),
    path("employee_list", views.employee_list, name="employee_list"),
    path("occupant_list", views.occupant_list, name="occupant_list"),
    path("report_logs", views.report_logs, name="report_logs"),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('approve_reservation/<int:user_id>', views.approve_reservation, name='approve_reservation'),
]
