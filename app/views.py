from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Question, Tag, Profile, Answer, Like
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import LoginForm
from django.contrib import messages
from django.contrib import auth

PAGINATION_SIZE = 10


def pagination(list_obj, request):
    paginator = Paginator(list_obj, PAGINATION_SIZE)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    content = pagination(Question.objects.all().annotate(answers_count=Count("answer", distinct=True)),
                         request)
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

    return render(request, "login.html", {"form": user_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required(redirect_field_name="login")
# def setting(request):
#     tags = Tag.objects.all().values()[:20]
#     return render(request, "setting.html", {"tags": tags})


# @login_required(redirect_field_name="login")
# def profile_edit(request):
#     if request.method == 'GET':
#         p_form = ProfileEdit(instance=request.user.profile)
#         u_form = UserEdit(instance=request.user)
#
#     elif request.method == 'POST':
#         p_form = ProfileEdit(data=request.POST, instance=request.user.profile)
#         u_form = UserEdit(data=request.POST, instance=request.user)
#         if p_form.is_valid() and u_form.is_valid():
#             u_form.instance.save()
#             p_form.instance.save()
#             messages.success(request, f"Your account has been updated!")
#             return redirect('profile_edit')
#         else:
#             messages.success(request, f"Your account has not been updated :(")
#             return redirect(reverse('profile_edit'))
#
#     content = {
#         "p_form": p_form,
#         "u_form": u_form,
#         "tags": Tag.objects.all().values()[:100]
#     }
#
#     return render(request, "profile_edit.html", content)


def ask(request):
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "ask.html", {"tags": tags, "top_users": top_users})


def login(request):
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "login.html", {"tags": tags, "top_users": top_users})


def reg(request):
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "reg.html", {"tags": tags, "top_users": top_users})


def hot(request):
    content = pagination(Question.objects.get_popular(), request)
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    return render(request, "index.html", {"questions": content, "tags": tags, "top_users": top_users})


def question(request, i: int):
    quest = Question.objects.get_question_by_id(i).annotate(answers_count=Count("answer", distinct=True))[0]
    answers = pagination(Answer.objects.get_answers_by_question(i), request)
    tags = Tag.objects.get_popular()
    top_users = Profile.objects.get_top_users()
    tags_for_quest = quest.get_tags().values()[:3]
    return render(request, "question_page.html", {'question': quest, "answers": answers, "top_users": top_users,
                                                  "tags": tags, "tags_for_quest": tags_for_quest})


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
