# from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDERS = (
        ('m', 'Мужчина'),
        ('f', 'Женщина'),
    )
    genders = models.CharField('Пол', max_length=1, choices=GENDERS, default='m')


# auditlog.register(User)