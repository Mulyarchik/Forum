from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserForm, LoginUserForm, QuestionCreate, CommentCreate
from .models import Question, Comment


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


# @login_required
def view_question(request, question_id):
    question = Question.objects.get(pk=question_id)

    if request.method == "POST":
        form_comment = CommentCreate(request.POST)
        if form_comment.is_valid():
            reply_obj = None
            try:
                reply_id = int(request.POST.get('reply_id'))
            except:
                reply_id = None
            if reply_id:
                reply_obj = Comment.objects.get(id=reply_id)

            #author = form_comment.cleaned_data['author']
            content = form_comment.cleaned_data['content']
            if reply_obj:
                Comment(author=request.user, content=content, reply=reply_obj, question=question).save()
            else:
                Comment(author=request.user, content=content, question=question).save()
                    # reply_comment = form_comment.save(commit=False)
                    # reply_comment.reply = reply_obj
                    # reply_comment.reply_id = int(request.POST.get("reply"))

            # if request.POST.get("reply", None):
            #     form_comment.reply_id = int(request.POST.get("reply"))

            # answer = form_comment.save(commit=False)
            # answer.author = request.user
            # answer.question_id = question.pk
            # answer.save()
            return redirect('/')
    else:
        form_comment = CommentCreate()

    comment = Comment.objects.all().filter(question_id=question.pk)

    context = {
        'comment': comment,
        'question': question,
        'form_comment': form_comment,
    }
    return render(request, 'backends/view_thread.html', context=context)
