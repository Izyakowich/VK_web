from django.contrib import admin
from .models import Profile, Like, Tag, Question, Answer


admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
