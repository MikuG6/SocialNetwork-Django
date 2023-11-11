# from auditlog.registry import auditlog
from django.db import models


class Photo(models.Model):
    path = models.CharField(max_length=32)
    description = models.CharField(max_length=255, null=True, blank=True)
    time_creation = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey("Album", on_delete=models.CASCADE, related_name="photos")
    message = models.ManyToManyField("Message", related_name="photos", blank=True)


# auditlog.register(Photo, m2m_fields={"message"})