# from auditlog.registry import auditlog
from django.db import models


class UserToDialog(models.Model):
    user = models.ForeignKey("User", related_name='dialogs_m2m', on_delete=models.CASCADE)
    dialog = models.ForeignKey("Dialog", related_name='users_m2m', on_delete=models.CASCADE)
    time_creation = models.DateTimeField(auto_now_add=True)


# auditlog.register(UserToDialog)