import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from service.models import User


class JWTAuthenticationMiddleware:
    unauthorized_urls = [
        "/admin",
        "/auth/token",
        "/user_registration",
        "/list_user",
        "/photo/download",
        "/swagger"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if self.is_need_to_validate_auth(request):
                if payload := self.validate_auth(request):
                    self.set_user(request, payload)
        except (AuthenticationFailed, NotAuthenticated):
            return JsonResponse(data={}, status=401)
        except Exception as e:
            print(f"Ty dolbaeb: {e}")
        return self.get_response(request)

    def is_need_to_validate_auth(self, request):
        return not any([
            request.path.startswith(path) for path in self.unauthorized_urls
        ])

    def validate_auth(self, request):
        if not (token := self.get_token_from_request(request)):
            raise NotAuthenticated()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.DecodeError:
            raise AuthenticationFailed()
        return payload

    @staticmethod
    def set_user(request, payload):
        try:
            request.user = User.objects.get(pk=payload["user_id"])
        except Exception as e:
            raise AuthenticationFailed()

    def get_token_from_request(self, request):
        try:
            return request.headers.get("Authorization")[7:]
        except Exception as e:
            print(e)
        return None

    def build_unauthorized_response(self, request):
        if request.build_absolute_uri("?") != "http://127.0.0.1:8000/api/token/":
            return redirect("http://127.0.0.1:8000/api/token/")

