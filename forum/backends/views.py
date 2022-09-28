from django.shortcuts import render, redirect

from .models import Thread, Post, User
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.backends import *
#messages.add_message(request, messages.INFO, 'Hello world.')

# def register(request):
#     form = UserCreationForm()
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             print(form)
#             form.save()
#             messages.success(request, "Success")
#             return redirect('login')
#         else:
#             messages.error(request, 'Error')
#     else:
#         form = UserCreationForm()
#     return render(request, 'backends/register.html', {"form":form})


# def register(request):
#     return render(request, 'backends/register.html')

def mycreate_user(request):
    error = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(
                user_form.cleaned_data["password"]
            )
            user.save()
            user_form.save()
            return redirect('/')
        else:
            error = 'ОШИБКА РЕГИСТРАЦИИ'
        context  = {
            'user_form': user_form,
            'error': error
        }
    else:
        context = {
            'user_form': UserForm(),
            'error': error
        }
    return render(request, 'backends/register.html', context)


def login(request):
    return render(request, 'backends/login.html')


def backends(request):
    thread = Thread.objects.all()
    return render(request, 'backends/backends.html', {'thread': thread, 'title':'Список новостей'})


