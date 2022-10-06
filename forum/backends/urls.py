from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = 'vlads_app'

urlpatterns = [
    path('', backends, name='home'),
    path('register/', user_registation, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create/', ask_a_guestion, name='ask_a_guestion'),
    path('thread/<int:question_id>/', view_question, name='post'),
    path('post/<int:question_id>/add_answer', add_answer, name='add_answer')
]
