from django.core.management.base import BaseCommand
from app.models import Like, Tag, User, Profile, Question, Answer


class Command(BaseCommand):
    help = 'Clear database'

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Like.objects.all().delete()
        Question.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
