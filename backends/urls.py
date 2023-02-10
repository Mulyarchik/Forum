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
    path('questions/create/', ask_a_guestion, name='ask_a_guestion'),
    path('questions/<int:question_id>/', comment_answer_create, name='comment_answer_create'),
    path('questions/<int:question_id>/edit', update_question, name='post_update'),
    path('questions/<int:question_id>/delete', delete_question, name='delete_question'),
    path('questions/<int:question_id>/rating_up', question_rating_up, name='question_rating_up'),
    path('questions/<int:question_id>/rating_down', question_rating_down, name='question_rating_down'),
    path('questions/<int:question_id>/answers/<int:answer_id>/rating_up', answer_rating_up, name='answer_rating_up'),
    path('questions/<int:question_id>/answers/<int:answer_id>/rating_down', answer_rating_down, name='answer_rating_down'),
    path('questions/<int:question_id>/answers/<int:answer_id>/delete', delete_answer, name='delete_answer'),
    path('questions/<int:question_id>/answers/<int:answer_id>/update_status', update_status, name='update_status_comment'),
    path('questions/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>/update', update_comment, name='update_comment'),
    path('questions/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>/delete', delete_comment, name='delete_comment'),
    path('profile/<int:user_id>/', view_profile, name='profile')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
