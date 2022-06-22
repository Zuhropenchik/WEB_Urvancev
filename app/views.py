from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Question, Tag, Profile, Answer, Like
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import LoginForm, SignUpForm, AskForm, AnswerForm
from django.contrib import auth
from django.contrib.auth.models import User

PAGINATION_SIZE = 10


def pagination(list_obj, request):
    paginator = Paginator(list_obj, PAGINATION_SIZE)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    content = pagination(Question.objects.all().annotate(answers_count=Count("answer", distinct=True)), request)
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "index.html", {"questions": content, "tags": tags, "top_users": top_users})


def login_view(request):
    if request.method == 'GET':
        user_form = LoginForm()
    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error('password', "Not such Login/Password")
                user_form.add_error('username', "")
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "login.html", {"form": user_form, "tags": tags, "top_users": top_users})


def signup_view(request):
    popular_tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    if request.method == 'GET':
        user_form = SignUpForm()
    elif request.method == 'POST':
        user_form = SignUpForm(data=request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                            email=user_form.cleaned_data['email'],
                                            password=user_form.cleaned_data['password'],
                                            )
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('login'))
    return render(request, "reg.html", {"form": user_form, "tags": popular_tags, "top_users": top_users})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="login")
def ask_view(request):
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    if request.method == 'GET':
        form = AskForm()
    elif request.method == 'POST':
        form = AskForm(data=request.POST)
        if form.is_valid():
            temp_question = Question.objects.create(title=form.cleaned_data['title'],
                                                    text=form.cleaned_data['text'],
                                                    author=Profile.objects.get(user=request.user))
            temp_question.save()
            if temp_question:
                return redirect(reverse("question", args=[temp_question.id]))
            else:
                return redirect(reverse('ask'))

    return render(request, "ask.html",
                  {"form": form, "tags": tags, "top_users": top_users, "key": "authorized"})


@login_required(login_url="login")
def question(request, i: int):
    quest = Question.objects.get_question_by_id(i).annotate(answers_count=Count("answer", distinct=True))[0]
    answers = pagination(Answer.objects.get_answers_by_question(i), request)
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    tags_for_quest = quest.get_tags().values()[:3]

    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            temp_answer = Answer.objects.create(question=Question.objects.get_question_by_id(i).get(),
                                                content=form.cleaned_data['content'],
                                                author=Profile.objects.get(user=request.user))
            temp_answer.save()
            if temp_answer:
                    return redirect(reverse("answer", args=[temp_answer.id]))
    return render(request, "question_page.html",
                  {'form': form, 'question': quest, "answers": answers, "top_users": top_users,
                   "tags": tags, "tags_for_quest": tags_for_quest})


def reg(request):
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "reg.html", {"tags": tags, "top_users": top_users})


def hot(request):
    content = pagination(Question.objects.get_popular(), request)
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "index.html", {"questions": content, "tags": tags, "top_users": top_users})


# def question(request, i: int):
#     quest = Question.objects.get_question_by_id(i).annotate(answers_count=Count("answer", distinct=True))[0]
#     answers = pagination(Answer.objects.get_answers_by_question(i), request)
#     tags = Tag.objects.get_popular()
#     top_users = Profile.objects.get_top_users()
#     tags_for_quest = quest.get_tags().values()[:3]
#     return render(request, "question_page.html", {'question': quest, "answers": answers, "top_users": top_users,
#                                                   "tags": tags, "tags_for_quest": tags_for_quest})


def tags(request, i: int):
    tag = Tag.objects.get_tag_by_id(i)[0]
    return render(request, "inc/tags.html", {"tag": tag})


def questions_with_tags(request, tag_title):
    content = pagination(
        Question.objects.get_questions_by_tag_title(tag_title).annotate(answers_count=Count("answer", distinct=True)),
        request)
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "index.html", {"questions": content, "tags": tags, "top_users": top_users})


def setting(request):
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "setting.html", {"tags": tags, "top_users": top_users})

def answer(request, i: int):
    answer = Answer.objects.get_answers_by_id(i)[0]
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "answer_page.html", {"answer":answer, "tags": tags, "top_users": top_users})