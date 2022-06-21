from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Question, Tag, User, Answer, Like
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

PAGINATION_SIZE = 10


def pagination(list_obj, request):
    paginator = Paginator(list_obj, PAGINATION_SIZE)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    content = pagination(Question.objects.all().values(), request)
    tags = Tag.objects.all().values()
    return render(request, "index.html", {"questions": content, "tags": tags})

def login_view(request):
    if request.method == 'GET':
        user_form = LoginForm()
    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('login'))

    return render(request, "login.html", {"form": user_form})

def ask(request):
    tags = Tag.objects.all().values()
    return render(request, "ask.html", {"tags": tags})


def login(request):
    tags = Tag.objects.all().values()
    return render(request, "login.html", {"tags": tags})


def reg(request):
    tags = Tag.objects.all().values()
    return render(request, "reg.html", {"tags": tags})


def hot(request):
    content = pagination(Question.objects.get_popular(), request)
    tags = Tag.objects.all().values()
    return render(request, "index.html", {"questions": content, "tags": tags})


def question(request, i: int):
    quest = Question.objects.get_question_by_id(i)[0]
    answers = pagination(Answer.objects.get_answers_by_question(i), request)
    tags = Tag.objects.all().values()
    tags_for_quest = quest.get_tags().values()
    return render(request, "question_page.html", {'question': quest, "answers": answers, "tags": tags,
                                                  "tags_for_quest": tags_for_quest})



def tags(request, i: int):
    tag = Tag.objects.get_tag_by_id(i)[0]
    return render(request, "inc/tags.html", {"tag": tag})


def questions_with_tags(request, tag_title):
    content = pagination(Question.objects.get_questions_by_tag_title(tag_title), request)
    tags = Tag.objects.all().values()
    return render(request, "index.html", {"questions": content, "tags": tags})


def setting(request):
    tags = Tag.objects.all().values()
    return render(request, "setting.html", {"tags": tags})
