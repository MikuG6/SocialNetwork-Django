from django.db import models


class Message(models.Model):
    dialog = models.ForeignKey("Dialog", related_name="dialogs", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="messages", on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False)
    time_creation = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    text_changed = models.BooleanField(default=False)

