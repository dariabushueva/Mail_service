from django.urls import path

from users.apps import UsersConfig
from .views import *

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('user_list/', UserList.as_view(), name='user_list'),
    path('verify/<str:key>/', verify_email, name='verify_email'),
    path('generate_password/', generate_and_send_password, name='generate_password'),
    path('blocked_user/<int:pk>', blocked_user, name='blocked_user'),
    ]
