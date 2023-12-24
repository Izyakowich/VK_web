from django.db import models
from django.db.models import Manager, Count
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class ProfileManager(Manager):
    def best(self):
        return Profile.objects.annotate(count_question=Count("questions")).order_by("-count_question")[:10]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="profile")
    avatar = models.ImageField(upload_to="static/img/avatar", default="static/img/default-avatar.jpg")

    def __str__(self):
        return f"{self.user.username[-1]} {self.user.first_name} {self.user.last_name} {self.id=}"

    objects = ProfileManager()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"


class Like(models.Model):
    from_whom = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="likes")
    question = models.ForeignKey("Question", on_delete=models.PROTECT, blank=True, null=True, related_name="likes")
    answer = models.ForeignKey("Answer", on_delete=models.PROTECT, blank=True, null=True, related_name="likes")
    date = models.DateTimeField(auto_now_add=True)
    choice = [
        ("+", "like"),
        ("-", "dislike"),
    ]
    event = models.CharField(max_length=1, choices=choice)

    class Meta:
        unique_together = [('from_whom', 'question'), ('from_whom', 'answer')]

    def __str__(self):
        return f"{dict(self.choice)[self.event]} from {self.from_whom.user.username} to \
            {'Q'+str(self.question) if self.question is not None else 'A' + str(self.answer)}"


class QuestionManager(Manager):
    def get_by_id(self, id: int):
        return Question.objects.get(id=id)
    def get_questions_all(self):
        return Question.objects.order_by("date")

    def by_tag(self, tag_name: str):
        return Tag.objects.get(name=tag_name).questions.all().order_by("date")

    def hot_questions(self):
        return Question.objects.filter(date__gte=timezone.now() - timedelta(days=7))\
            .annotate(count_answers=Count("answers"))


class Question(models.Model):
    author = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", related_name="questions")

    objects = QuestionManager()

    def __str__(self):
        return f"{self.title} from {self.author.user.username} {self.id=}"

    def count_like(self):
        return len(self.likes.filter(event="+"))

    def count_dislike(self):
        return len(self.likes.filter(event="-"))

    def count_answer(self):
        return len(self.answers.all())


class AnswerManage(Manager):
    def answers_to_question(self, question):
        return Question.objects.get(id=question).answers


class Answer(models.Model):
    author = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="answers")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

    objects = AnswerManage()

    def __str__(self):
        return f"{self.author.user.username} {self.id=}"

    def count_like(self):
        return len(self.likes.filter(event="+"))

    def count_dislike(self):
        return len(self.likes.filter(event="-"))
