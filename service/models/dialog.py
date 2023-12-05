from django.db import models


class Dialog(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    time_create = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField("User", related_name="dialogs", through="UserToDialog")
