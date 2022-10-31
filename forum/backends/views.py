from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserForm, LoginUserForm, QuestionCreate, AnswerCreate, CommentCreate, UserPhotoUpdate
from .models import Question, Comment, Answer, User


def user_registation(request):
    error = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user_form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
        else:
            messages.error(request, "Форма не прошла валидацию!")
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


def backends(request):
    question = Question.objects.select_related('author').order_by('-created_at')

    return render(request, 'backends/backends.html', {'thread': question})


def ask_a_guestion(request):
    if not request.user.is_authenticated:
        error = ''
        messages.error(request, "Для создания вопроса вам необходимо авторизоваться")
        return redirect("/login")

    if request.method == "POST":
        form = QuestionCreate(request.POST)
        print("СОЗДАНИЕ ПОСТ")
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
        else:
            messages.error(request, "Форма не прошла валидацию!")
        return redirect('/')
    else:
        form = QuestionCreate()
    return render(request, 'backends/create_post.html', locals())


def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'GET':
        print("РЕДАКТИРОВАНИЕ ГЕТ")
        if request.user != question.author:
            messages.error(request, "У вас нету прав для редактирования записи!")
            return redirect(question.get_absolute_url())
        form = QuestionCreate(instance=question)

    if request.method == 'POST':
        print("РЕДАКТИРОВАНИЕ ПОСТ")
        form = QuestionCreate(request.POST, instance=question)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Форма не прошла валидацию!")
        return redirect(question.get_absolute_url())

    context = {
        'form': form,
        'question': question
    }
    return render(request, 'backends/create_post.html', context)


# @login_required
def view_question(request, question_id):
    question = Question.objects.select_related('author').get(pk=question_id)
    answer = Answer.objects.select_related('author').all().filter(question_id=question.pk)
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Для создания вопроса вам необходимо авторизоваться")
            return redirect(question.get_absolute_url())

        if request.POST.get("reply_to"):
            form = CommentCreate(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.answer = answer.get(pk=request.POST.get("reply_to"))
                comment.author = request.user
                comment.save()
            else:
                messages.error(request, "Форма не прошла валидацию!")
            return redirect(question.get_absolute_url())
        else:
            form = AnswerCreate(request.POST)
            if form.is_valid():
                answer_form = form.save(commit=False)
                answer_form.question_id = question.pk
                answer_form.author = request.user
                form.save()
            else:
                messages.error(request, "Форма не прошла валидацию!")
            return redirect(question.get_absolute_url())
    else:
        form = AnswerCreate()

    comment = Comment.objects.select_related('author')

    context = {
        'answer': answer,
        'question': question,
        'form': form,
        'comment': comment,
    }
    return render(request, 'backends/view_thread.html', context=context)


# def update_comment(request, answer_id, question_id):

# def update_comment(request, question_id, answer_id, comment_id):
def update_comment(request, question_id, answer_id, comment_id):
    question = get_object_or_404(Question, pk=question_id)

    if comment_id == 0:
        answer = get_object_or_404(Answer, pk=answer_id)

    elif comment_id != 0:
        answer = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'GET':
        if request.user != answer.author:
            messages.error(request, "У вас нету прав для редактирования записи!")
            return redirect(question.get_absolute_url())
        form = CommentCreate(instance=answer)

    if request.method == 'POST':
        form = CommentCreate(request.POST, instance=answer)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Форма не прошла валидацию!")
        return redirect(question.get_absolute_url())

    return render(request, 'backends/update_comment.html', locals())


def view_profile(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == "POST":
        form = UserPhotoUpdate(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Изображение пользователя успешно изменено!")
        else:
            messages.error(request, "Изображение пользователя не было изменено!")
        return redirect('/')
    else:
        form = UserPhotoUpdate()

    context = {
        'user': user,
        'form': form

    }
    return render(request, 'backends/view_profile.html', context=context)


def delete_answer(request, question_id, answer_id):
    question = Question.objects.get(pk=question_id)
    Answer.objects.get(pk=answer_id).delete()
    return redirect(question.get_absolute_url())


# @user_passes_test(lambda u: u.is_staff)
def delete_comment(request, question_id, answer_id, comment_id):
    question = Question.objects.get(pk=question_id)
    Comment.objects.get(pk=comment_id).delete()
    return redirect(question.get_absolute_url())


def delete_question(request, question_id):
    Question.objects.get(pk=question_id).delete()
    return redirect('/')
