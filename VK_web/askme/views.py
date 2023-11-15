from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


class Question:
    def __init__(self, title, content, rating, author_img):
        self.title = title
        self.content = content
        self.rating = rating
        self.author_img = author_img


question_item = Question(
    'Sample Title',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eget tortor at odio tempus scelerisque.',
    777,
    'https://sun9-74.userapi.com/impg/IkdqPKOIfRr8TF5XrDpx0FApStrqI3N00iDHmw/McWp1do3_sU.jpg?size=1080x1080&quality=95&sign=050a9d0bbcbb22084f2f41f5574b7c71&type=album'
)


def index(request):
    questions = [question_item for _ in range(3)]
    return render(request, 'index.html', {'questions': questions})


def ask_question(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def tag_list(request, tag):
    questions = [question_item for _ in range(1)]
    return render(request, 'index.html', {'questions': questions})


def signup(request):
    return render(request, 'signup.html')


def question(request, question_id):
    answers = ['Просто какой-то текст' for _ in range(3)]
    return render(request, 'question.html', {'question': question_item, 'answers': answers})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
