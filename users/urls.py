from django.urls import path

from users.apps import UsersConfig
from .views import *

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:key>/', verify_email, name='verify_email'),
    ]
