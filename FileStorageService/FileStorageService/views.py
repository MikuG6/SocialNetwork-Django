import os
import uuid

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View


class FileStorageUploadView(View):
    def post(self, request):
        _uuid = uuid.uuid4()
        filename = f"{_uuid}.png"
        image = request.FILES["image"].read()
        with open(os.path.join(settings.IMAGES_DIR, filename), "wb") as f:
            f.write(image)
        return JsonResponse({"uuid": _uuid})


class FileStorageDownloadView(View):
    def get(self, request, uuid_slug):
        filename = f"{uuid_slug}.png"
        with open(os.path.join(settings.IMAGES_DIR, filename), "rb") as f:
            binary_image = f.read()
            return HttpResponse(content=binary_image, headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            })
