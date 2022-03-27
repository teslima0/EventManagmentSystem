from django.urls import path
from .views import *


urlpatterns = [
path('login_user', login_user, name = 'loginpage'),
path('logout_user', logout_user, name = 'logout'),
path('register_user', Register_user, name = 'register_user'),
]