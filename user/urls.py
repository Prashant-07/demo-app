from django.urls import path
from django.urls import path
from .views import *

urlpatterns = [
    path('register',createUser),
    path('updateAccountInfo',updateInfo),
    path('deleteAccount',deleteUser),
    path('login',login),
    path('logout',logout),
    ]