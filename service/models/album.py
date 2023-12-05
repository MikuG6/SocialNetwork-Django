from django.db import models

from .user import User


class Album(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="albums", on_delete=models.CASCADE)
    time_creation = models.DateTimeField(auto_now_add=True)


