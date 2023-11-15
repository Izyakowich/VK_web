from django.contrib import admin

from . import models

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Ratings)
admin.site.register(models.Tag)
admin.site.register(models.User)
