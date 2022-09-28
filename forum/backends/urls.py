from django.urls import path
from .views import *

urlpatterns = [
    path('', backends),
    path('register/', mycreate_user, name='register'),
    path('login/', login, name='login'),
]