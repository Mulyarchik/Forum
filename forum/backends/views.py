from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import UserForm, LoginUserForm, QuestionCreate, AnswerCreate
from .models import Question, Answer


def user_registation(request):
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


def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginUserForm()
    return render(request, 'backends/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


# !!!! id title username created_at
def backends(request):
    questions = Question.objects.all()
    context = {
        'thread': questions,
        'title': 'список новостей'
    }
    return render(request, 'backends/backends.html', context=context)


@login_required
def ask_a_guestion(request):
    if request.method == "POST":
        form = QuestionCreate(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('/')
    else:
        form = QuestionCreate()
    return render(request, 'backends/create_post.html', locals())



def view_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    try:
        answer = Answer.objects.get(pk=question_id)
        return render(request, 'backends/view_thread.html', {'question': question, 'answer': answer})
    except ObjectDoesNotExist:
        return render(request, 'backends/view_thread.html', {'question': question})

@login_required
def add_answer(request):
    if request.method == "POST":
        form_answer = AnswerCreate(request.POST)
        if form_answer.is_valid():
            question = form_answer.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('/')
    else:
        form_answer = AnswerCreate()
    return render(request, 'backends/test.html', locals())
