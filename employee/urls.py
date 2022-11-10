from django.urls import path
from employee import views

app_name = 'employee'

urlpatterns = [
    path("", views.index, name='index'),
    # path("submit", views.submit, name='submit'),
    # path("assign", views.assign, name='assign'),

]
