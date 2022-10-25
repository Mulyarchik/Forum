from django.contrib import messages
from django.contrib.auth import login, logout
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserForm, LoginUserForm, QuestionCreate, AnswerCreate, CommentCreate
from .models import Question, Comment, Answer, User


def user_registation(request):
    error = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user_form.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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

    context = {
        'form': form
    }
    return render(request, 'backends/login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('/')


# !!!! id title username created_at
def backends(request):
    questions = Question.objects.all()
    # questions = Question.objects.select_related('author')
    # profile = Profile.objects.all()
    context = {
        'thread': questions,
        #    'profile': profile
    }
    return render(request, 'backends/backends.html', context=context)


# @login_required
def ask_a_guestion(request):
    if not request.user.is_authenticated:
        error = ''
        messages.error(request, "Для создания вопроса вам необходимо авторизоваться")
        return redirect("/login")

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


# @login_required
def view_question(request, question_id):
    question = Question.objects.select_related('author').get(pk=question_id)
    answer = Answer.objects.select_related('author').all().filter(question_id=question.pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            error = ''
            messages.error(request, "Для создания вопроса вам необходимо авторизоваться")
            return redirect(question.get_absolute_url())

        if request.POST.get("reply_to"):
            form = CommentCreate(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.answer = answer.get(pk=request.POST.get("reply_to"))
                comment.author = request.user
                comment.save()
                return redirect(question.get_absolute_url())
        else:
            form = AnswerCreate(request.POST)
            if form.is_valid():
                answer_form = form.save(commit=False)
                answer_form.question_id = question.pk
                answer_form.author = request.user
                form.save()
                return redirect(question.get_absolute_url())
    else:
        form = AnswerCreate()

    # comment = Comment.objects.all().filter(question_id=question_id)
    comment = Comment.objects.select_related('author')

    context = {
        'answer': answer,
        'question': question,
        'form': form,
        'comment': comment,
    }
    return render(request, 'backends/view_thread.html', context=context)


def view_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {
        'user': user,
    }
    return render(request, 'backends/view_profile.html', context=context)
