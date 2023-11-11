

from django.core.management import BaseCommand
from django.db import transaction

from service.models import User, Dialog, Message, Album, Photo


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        u1, created = User.objects.get_or_create(username="user1", email="user1@gmail.com")
        if created:
            u1.set_password("123456")
        u2, created = User.objects.get_or_create(username="user2", email="user2@gmail.com")
        if created:
            u2.set_password("123456")
        u3, created = User.objects.get_or_create(username="user3", email="user3@gmail.com")
        if created:
            u3.set_password("123456")

        d1 = Dialog.objects.get_or_create(name="dialog1")[0]
        d1.users.set([u1, u2])
        d2 = Dialog.objects.get_or_create(name="dialog2")[0]
        d2.users.set([u2, u3])

        m1 = Message.objects.get_or_create(text="text1", dialog=d1, user=u1)[0]
        m2 = Message.objects.get_or_create(text="text2", dialog=d2, user=u2)[0]

        a1 = Album.objects.get_or_create(name="album1", user=u1)[0]
        a2 = Album.objects.get_or_create(name="album2", user=u1)[0]

        p1 = Photo.objects.get_or_create(path="photo1", album=a1)[0]
        p2 = Photo.objects.get_or_create(path="photo2", album=a2)[0]

