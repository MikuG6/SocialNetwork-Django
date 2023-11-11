from django.contrib import admin
from django.contrib.admin.models import LogEntry

from service.models import User, Album, Dialog, Friend, Message, Photo, Role, UserToDialog

# Register your models here.

admin.site.register(User)
admin.site.register(Album)
admin.site.register(Dialog)
admin.site.register(Friend)
admin.site.register(Message)
admin.site.register(Photo)
admin.site.register(Role)
admin.site.register(UserToDialog)
admin.site.register(LogEntry)
