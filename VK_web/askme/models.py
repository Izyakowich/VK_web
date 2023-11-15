from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField(
        default='https://w.forfun.com/fetch/15/156edf6b7f00b207e365081fd2cd8186.jpeg',
        max_length=500
    )

    def __str__(self):
        return self.user.username
