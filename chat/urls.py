from chat import views
from django.urls import path

app_name = "chat"

urlpatterns = [
    path("", views.index, name="chat_to_admin"),
    path("<int:user_id>", views.chat_list, name="chat_users"),
    path("user/<int:user_id>", views.chat_log, name="chat_to_user")
]
