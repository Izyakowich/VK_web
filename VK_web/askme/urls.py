# Copyright 2023 Dmitriy Permyakov <dimapermyakov55@gmail.com>

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('ask-question', ask_question, name='ask-question'),
    path('question/<int:question_id>', question, name='question'),
    path('settings', settings, name='settings'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('tag/<str:tag>', tag_list, name='tag_list'),
]
