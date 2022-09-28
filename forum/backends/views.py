from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserForm
from .models import Thread


def mycreate_user(request):
    error = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user_form.save()
            messages.success(request, "Вы успешно зарегестрировались")
            return redirect('/')
        else:
            messages.error(request, "Ошибка регистрации")
        context = {
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
    return render(request, 'backends/backends.html', {'thread': thread, 'title': 'Список новостей'})
