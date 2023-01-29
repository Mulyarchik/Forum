from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserForm, LoginUserForm, QuestionCreate, AnswerCreate, CommentCreate, UserPhotoUpdate
from .models.answer import Answer
from .models.question import Question
from .models.tag import Tag
from .models.user_voting import User, Voting, AlreadyVoted
from .models.comment import Comment


def user_registation(request):
    error = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user_form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "You have successfully registered!")
            return redirect('/')
        else:
            messages.error(request, "Registration error")
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
            messages.error(request, "Wrong username/password!")
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
    question = Question.objects.select_related('author', 'voting').order_by('-created_at')

    return render(request, 'backends/backends.html', {'questions': question})


def ask_a_guestion(request):
    tags = Tag.objects.all().order_by('-name')

    if not request.user.is_authenticated:
        messages.error(request, "Для создания вопроса вам необходимо авторизоваться")
        return redirect("/login")

    if request.method == "POST":
        form = QuestionCreate(request.POST)
        if form.is_valid():
            Question().create_question(user=request.user, request_post=request.POST, count_up=0, count_down=0)
        else:
            messages.error(request, "Форма не прошла валидацию!")
        return redirect('/')
    else:
        form = QuestionCreate()

    context = {
        'form': form,
        'tags': tags,

    }
    return render(request, 'backends/create_post.html', context=context)


def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    tag = Tag.objects.all()

    if request.method == 'GET':
        if request.user != question.author:
            messages.error(request, "У вас нету прав для редактирования записи!")
            return redirect(question.get_absolute_url())
        form = QuestionCreate(instance=question)

    if request.method == 'POST':
        form = QuestionCreate(request.POST, instance=question)
        if form.is_valid():
            question.update(request.user, request.POST)
        else:
            messages.error(request, "Форма не прошла валидацию!")
        return redirect(question.get_absolute_url())

    context = {
        'form': form,
        'question': question,
        'tags': tag
    }
    return render(request, 'backends/create_post.html', context)


def question_rating_up(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.voting.vote_up(request.user.id)
        messages.success(request, "Your review has been submitted successfully for this entry!")
    except ObjectDoesNotExist:
        messages.error(request, f"Question with ID '{question.id}' doesn't exists")
    except AlreadyVoted:
        messages.error(request, "You have already voted on that question!")

    return redirect(question.get_absolute_url())


def question_rating_down(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.voting.vote_up(request.user.id)
        messages.success(request, "Your review has been submitted successfully for this entry!")
    except ObjectDoesNotExist:
        messages.error(request, f"Question with ID '{question.id}' doesn't exists")
    except AlreadyVoted:
        messages.error(request, "You have already voted on that question!")

    return redirect(question.get_absolute_url())


def comment_answer_create(request, question_id):
    question = Question.objects.select_related('author', 'voting').get(pk=question_id)
    answer = Answer.objects.select_related('author', 'voting').all().filter(question_id=question.pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to reply !")
            return redirect(question.get_absolute_url())

        if request.POST.get("reply_to"):
            form = CommentCreate(request.POST)
            if form.is_valid():
                Comment().create(request.POST.get("reply_to"), request.user, request.POST)
            else:
                messages.error(request, "Form not validated!")
            return redirect(question.get_absolute_url())

        else:
            form = AnswerCreate(request.POST)
            if form.is_valid():
                Answer().create(question, request.user, request.POST, count_up=0, count_down=0)
            else:
                messages.error(request, "Form not validated!")
            return redirect(question.get_absolute_url())
    else:
        form = AnswerCreate()

    comment = Comment.objects.select_related('author')

    context = {
        'answers': answer,
        'question': question,
        'form': form,
        'comments': comment,
    }
    return render(request, 'backends/view_thread.html', context=context)


def answer_rating_up(request, question_id, answer_id):
    question = Question.objects.get(pk=question_id)
    try:
        answer = Answer.objects.get(id=answer_id)
        answer.voting.vote_up(request.user.id)
        messages.success(request, "Your review has been submitted successfully for this entry!")
    except ObjectDoesNotExist:
        messages.error(request, f"Question with ID '{answer.id}' doesn't exists")
    except AlreadyVoted:
        messages.error(request, "You have already voted on that question!")

    return redirect(question.get_absolute_url())


def answer_rating_down(request, question_id, answer_id):
    question = Question.objects.get(pk=question_id)
    try:
        answer = Answer.objects.get(id=answer_id)
        answer.voting.vote_down(request.user.id)
        messages.success(request, "Your review has been submitted successfully for this entry!")
    except ObjectDoesNotExist:
        messages.error(request, f"Question with ID '{answer.id}' doesn't exists")
    except AlreadyVoted:
        messages.error(request, "You have already voted on that question!")

    return redirect(question.get_absolute_url())


def update_comment(request, question_id, answer_id, comment_id):
    question = get_object_or_404(Question, pk=question_id)

    if comment_id == 0:
        answer = get_object_or_404(Answer, pk=answer_id)

    elif comment_id != 0:
        answer = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'GET':
        if request.user != answer.author:
            messages.error(request, "You do not have permission to edit the post!")
            return redirect(question.get_absolute_url())
        form = CommentCreate(instance=answer)

    if request.method == 'POST':
        form = CommentCreate(request.POST, instance=answer)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Form not validated!")
        return redirect(question.get_absolute_url())

    return render(request, 'backends/update_comment.html', locals())


def update_status(request, question_id, answer_id):
    question = Question.objects.get(pk=question_id)
    answer = Answer.objects.get(pk=answer_id, question_id=question_id)
    if answer.is_useful:
        answer.is_useful = False
        answer.save()
        messages.error(request, "Removed helpful response status!")
    else:
        answer.is_useful = True
        answer.save()
        messages.success(request, "Useful response status set!")

    return redirect(question.get_absolute_url())


def view_profile(request, user_id):
    user = User.objects.get(pk=user_id)

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your profile!")
        return redirect('/login')

    if request.method == "POST":
        form = UserPhotoUpdate(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User image changed successfully!")
        else:
            messages.error(request, "User picture has not been changed!")
        return redirect('/')
    else:
        form = UserPhotoUpdate()

    context = {
        'user': user,
        'form': form,

    }
    return render(request, 'backends/view_profile.html', context=context)


def delete_answer(request, question_id, answer_id):
    question = Question.objects.get(pk=question_id)
    answer = Answer.objects.get(pk=answer_id)

    if request.user.id != answer.author.id:
        messages.error(request, "You do not have permission to delete a comment!")
        return redirect('/login')
    else:
        Voting.objects.get(pk=answer.voting.id).delete()
    return redirect(question.get_absolute_url())


def delete_comment(request, question_id, answer_id, comment_id):
    question = Question.objects.get(pk=question_id)
    comment = Comment.objects.get(pk=comment_id)
    if request.user != comment.pk:
        messages.error(request, "You do not have permission to delete a comment!")
        return redirect('/login')
    else:
        Comment.objects.get(pk=comment_id).delete()
    return redirect(question.get_absolute_url())


@user_passes_test(lambda u: u.is_staff)
def delete_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    Voting.objects.get(pk=question.voting.id).delete()
    return redirect('/')
