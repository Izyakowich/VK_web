from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import auth
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Question, Tag, Answer, Profile
from django.urls import reverse
from .forms import LoginForm, RegisterForm, ProfileEditForm, QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    questions = Question.objects.get_questions_all()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "tags": TAGS,
               "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "index.html", context)


def question(request, id: int):
    try:
        question = Question.objects.get_by_id(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    if request.method == "GET":
        answer_form = AnswerForm()
    elif request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_id = answer_form.save(request.user, question)
            answers_cou = question.answers.count()
            num_page = (answers_cou // 10) + 1
            return HttpResponseRedirect(reverse("question", args=[id]) + f"?page={num_page}#answer-{answer_id}")

    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    answers = question.answers.all()
    context = {
        "question": question,
        "page_obj": paginate(answers, request),
        "tags": TAGS, "best_members": MEMBERS,
        "form": answer_form,
    }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "question.html", context)


@login_required(login_url="login", redirect_field_name="continue")
def setting(request):
    if request.method == "GET":
        setting_form = ProfileEditForm(request.user.id, initial=dict(upload_avatar=request.user.profile.avatar,
                                                                     username=request.user.username,
                                                                     first_name=request.user.first_name,
                                                                     last_name=request.user.last_name,
                                                                     email=request.user.email))
    elif request.method == "POST":
        setting_form = ProfileEditForm(request.user.id, request.POST, request.FILES)
        if setting_form.is_valid():
            setting_form.save()
            return HttpResponseRedirect(reverse("settings"))

    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS, "best_members": MEMBERS,
        "form": setting_form,
    }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "settings.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def log_in(request):
    continue_url = request.GET.get("continue")
    if continue_url is None or continue_url[0] != "/":
        continue_url = "/"

    if request.method == "GET":
        login_form = LoginForm()
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(continue_url)
            else:
                login_form.add_error(None, "Incorrect login or password")

    setattr(login_form, "continue_url", continue_url)
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS,
        "best_members": MEMBERS,
        "form": login_form,
    }
    return render(request, "login.html", context)


def signup(request):
    if request.method == "GET":
        register_form = RegisterForm()
    elif request.method == "POST":
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect("/")
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"tags": TAGS, "best_members": MEMBERS,
               "form": register_form}
    return render(request, "register.html", context)


def search_by_tag(request, tag: str):
    try:
        questions = Question.objects.by_tag(tag)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "tag": tag,
               "tags": TAGS, "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "tag.html", context)


@login_required(login_url="login", redirect_field_name="continue")
def ask(request):
    if request.method == "GET":
        question_form = QuestionForm()
    elif request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_id = question_form.save(request.user)
            return HttpResponseRedirect(reverse("question", args=[question_id]))

    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS,
        "best_members": MEMBERS,
        "form": question_form,
    }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "ask.html", context)


def hot(request):
    questions = Question.objects.hot_questions()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "tags": TAGS, "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "hot.html", context)


def best_users(request, id: int):
    try:
        profile = Profile.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    questions = profile.questions.all()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "tags": TAGS, "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "index.html", context)
