from django.urls import path
from . import views

app_name = 'occupant'

urlpatterns = [
    path('', views.index, name='index'),

    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('update_profile', views.update_profile, name='update_profile'),

    path('reserve', views.reserve, name='reserve'),
    path('reserve/create/<int:room_type>', views.create_reserve, name='create_reserve'),
    path('reserve/detail', views.get_reserve, name='get_reserve'),
    path('reserve/delete/<int:reserve_id>', views.delete_reserve, name='delete_reserve'),

    path('report/', views.report, name='report'),
    path('report/create', views.create_report, name='create_report'),
    path('report/detail/<int:report_id>', views.get_report, name='get_report'),
    path('report/all', views.list_report, name='list_report'),
    path('report/delete/<int:report_id>', views.delete_report, name='delete_report'),
]