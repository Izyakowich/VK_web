from django.core.management.base import BaseCommand
from .generate import fill


class Command(BaseCommand):
    help = 'Filling in the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            ratio = int(options["ratio"][0])
        except ValueError:
            self.stdout.write("Неверный тип передаваемого параметра")
            return
        except IndexError:
            self.stdout.write("Отсутвует необходимый параметр")
            return
        except Exception as err:
            self.stdout.write(str(err))
            return
        fill(ratio)
        self.stdout.write("OK")
