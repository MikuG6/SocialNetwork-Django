# from auditlog.registry import auditlog
from django.db import models
from .user import User


class Role(models.Model):
    MOD = "MOD"
    USR = "USR"
    ADM = "ADM"
    ROLES = (
        (MOD, "Модератор"),
        (USR, "Пользователь"),
        (ADM, "Администратор"),
    )
    name = models.CharField("Роль", max_length=3, choices=ROLES, default=USR)
    users = models.ManyToManyField(User, related_name="roles")