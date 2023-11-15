from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import Http404, HttpResponseNotFound
from . import models


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    questions = models.Question.objects.with_new()
    if not questions:
        return data_is_empty(request)

    page_obj = paginate(questions, request, 5)
    return render(
        request,
        "index.html",
        {
            "questions": questions[page_obj.start_index() - 1 : page_obj.end_index()],
            "title": "New questions",
            "page_obj": page_obj,
        },
    )


def ask_question(request):
    return render(request, "ask_question.html")


def settings(request):
    return render(request, "settings.html")


def login(request):
    return render(request, "login.html")


def hot_list(request):
    hot_questions = models.Question.objects.with_rating_order()
    if not hot_questions:
        return data_is_empty(request)

    page_obj = paginate(hot_questions, request, 5)
    return render(
        request,
        "index.html",
        {
            "title": "Hot Questions",
            "questions": hot_questions[
                page_obj.start_index() - 1 : page_obj.end_index()
            ],
            "page_obj": page_obj,
        },
    )


def tag_list(request, tag):
    questions = models.Question.objects.with_tag(tag)
    page_obj = paginate(questions, request, 5)
    return render(
        request,
        "index.html",
        {
            "title": f'Questions with tag: "{tag}"',
            "questions": questions[page_obj.start_index() - 1 : page_obj.end_index()],
            "page_obj": page_obj,
        },
    )


def signup(request):
    return render(request, "signup.html")


def question(request, question_id):
    our_question = models.Question.objects.filter(id=question_id)
    if not our_question:
        raise Http404
    our_question = our_question.first()
    answers = models.Answer.objects.with_question(question_id)
    return render(
        request, "question.html", {"question": our_question, "answers": answers}
    )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


def data_is_empty(request):
    page_obj = paginate([], request, 5)
    return render(
        request,
        "index.html",
        {
            "questions": [],
            "title": "Questions not found :(",
            "page_obj": page_obj,
        },
    )
