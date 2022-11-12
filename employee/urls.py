from django.urls import path
from employee import views

app_name = 'employee'

urlpatterns = [
    path("", views.index, name='index'),

    path("edit_profile", views.edit_profile, name='edit_profile'),
    path('update_profile', views.update_profile, name='update_profile'),

    path("submit/<int:report_id>", views.submit, name='submit'),
    path("submit/get_submit/<int:report_id>", views.get_submit, name='get_submit'),
    path("assign/<int:report_id>", views.assign, name='assign'),
    path("assign/get_assign/<int:report_id>", views.get_assign, name='get_assign'),

]
