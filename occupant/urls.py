from django.urls import path
from . import views

app_name = 'occupant'

urlpatterns = [
    path('', views.index, name='index'),
    path('reserve/', views.reserve, name='reserve'),
    path('reserve/detail/<int:reserve_id>', views.post_reserve, name='post_reserve'),
    path('reserve/all', views.list_reserve, name='list_reserve'),
    path('report/', views.report, name='report'),
    path('report/detail/<int:report_id>', views.post_report, name='post_report'),
    path('report/all', views.list_report, name='list_report'),
]
