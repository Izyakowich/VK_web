from django.db import models
from django.contrib.auth import models as user_models


class QuestionManager(models.Manager):
    last_update = 0
    update_need = 100

    def update_all(self):
        for i in super().get_queryset().all():
            i.update_average_rating()

    def with_rating_order(self):
        questions = super().get_queryset()
        all_length = len(questions.all())
        if all_length > QuestionManager.last_update + QuestionManager.update_need:
            QuestionManager.last_update = all_length
            self.update_all()
        return questions.order_by("-summary_rating")

    def with_tag(self, tag):
        questions = super().get_queryset()
        all_length = len(questions.all())
        if all_length > QuestionManager.last_update + QuestionManager.update_need:
            QuestionManager.last_update = all_length
            self.update_all()
        return questions.filter(tag__name=tag)

    def with_new(self):
        questions = super().get_queryset()
        all_length = len(questions.all())
        if all_length > QuestionManager.last_update + QuestionManager.update_need:
            QuestionManager.last_update = all_length
            self.update_all()
        return questions.order_by("-id")

    def get_queryset(self):
        return super().get_queryset()


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class RatingsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class AnswerManager(models.Manager):
    def with_question(self, question_id):
        return self.get_queryset().filter(question_id=question_id)

    def get_queryset(self):
        return super().get_queryset()


class Ratings(models.Model):
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    is_question = models.BooleanField(default=True)
    question = models.ForeignKey("Question", on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE, null=True)
    is_good = models.BooleanField(default=True)

    objects = RatingsManager()


class Question(models.Model):
    title = models.CharField(max_length=127, unique=True)
    text = models.CharField(max_length=255, default="question text")
    creator = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField("Tag")
    summary_rating = models.IntegerField(null=True, blank=True, default=0)

    objects = QuestionManager()

    def update_average_rating(self):
        sum_rating = len(Ratings.objects.test(self).filter(is_good=True).all()) - len(
            Ratings.objects.test(self).filter(is_good=False).all()
        )
        self.summary_rating = sum_rating
        self.save()

    def __str__(self):
        return f'Question "{self.title}"'


class Answer(models.Model):
    text = models.CharField(max_length=255, default="answer text")
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    creator = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    summary_rating = models.IntegerField(null=True, blank=True, default=0)

    objects = AnswerManager()


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    color = models.CharField(max_length=31)

    def __str__(self):
        return f'Tag "{self.name}"'


class User(models.Model):
    profile = models.OneToOneField(user_models.User, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=31, unique=True)
    avatar = models.TextField(
        default="",
        max_length=500,
    )

    objects = UserManager()

    def __str__(self):
        return f'User "{self.nickname}"'
