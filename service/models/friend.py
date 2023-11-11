# from auditlog.registry import auditlog
from django.db import models


class Friend(models.Model):
    user_from = models.ForeignKey("User", related_name='friends_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey("User", related_name='friends_to', on_delete=models.CASCADE)
    time_creation = models.DateTimeField(auto_now_add=True)


# auditlog.register(Friend)