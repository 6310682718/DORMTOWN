from chat import views
from django.urls import path

app_name = "chat"

urlpatterns = [
    path("", views.index, name="rooms"),
    # path('<int:room_number>/', views.room, name='chat'),
    path("<int:user_id>", views.chat_list, name="chat_list")
]
