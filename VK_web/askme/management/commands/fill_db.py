from random import randint
from django.core.management.base import BaseCommand
from ... import models
from django.contrib.auth import models as user_models


class Command(BaseCommand):
    help = "Fills the database with random values"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        for i in range(ratio):
            p = user_models.User(username=f'user-{i}', email=f'user-{i}@mail.ru', password='1234')
            p.save()

            u = models.User(nickname=f'nick-{i}', profile=p)
            u.save()

        for i in range(ratio):
            t = models.Tag(name=f'tag-{i}')
            t.save()

        for i in range(ratio * 10):
            rand = randint(0, ratio - 1)
            u = models.User.objects.get(id=models.User.objects.first().id + rand)
            q = models.Question(title=f'Question {i} by User {rand}', text=f'SIIIU! It is question by user {rand}',
                                creator=u)
            q.save()
            rand_tag = randint(1, ratio - 1)
            tag = models.Tag.objects.get(id=models.Tag.objects.first().id + rand_tag)
            q.tag.add(tag)
            q.save()

            for j in range(10):
                rand2 = randint(0, ratio - 1)
                u = models.User.objects.get(id=models.User.objects.first().id + rand2)
                a = models.Answer(text=f'Answer {j} for this question', question=q, creator=u)
                a.save()

        for i in range(ratio * 1000):
            rand_u = randint(0, ratio - 1)
            u = models.User.objects.get(id=models.User.objects.first().id + rand_u)
            rand_q = randint(0, ratio * 10 - 1)
            q = models.Question.objects.get(id=models.Question.objects.first().id + rand_q)
            rand_g = randint(0, 1)
            r = models.Ratings(is_question=True, is_good=rand_g, user=u, question=q)
            r.save()

        for i in range(ratio * 1000):
            rand_u = randint(0, ratio - 1)
            u = models.User.objects.get(id=models.User.objects.first().id + rand_u)
            rand_a = randint(0, ratio * 100 - 1)
            a = models.Answer.objects.get(id=models.Answer.objects.first().id + rand_a)
            rand_g = randint(0, 1)
            r = models.Ratings(is_question=True, is_good=rand_g, user=u, answer=a)
            r.save()
