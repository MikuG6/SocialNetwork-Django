from django.core.management import BaseCommand

from service.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.filter(username="admin").exists():
            self.stdout.write("admin is already created")
        else:
            User.objects.create_superuser("admin", "admin@gmail.com", "123456")
            self.stdout.write("admin is created")
