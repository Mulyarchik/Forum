from django.urls import path
from .views import *
from . import views
from django.urls import path, include

urlpatterns = [
    path('', backends),
    path('register/', user_registation, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
