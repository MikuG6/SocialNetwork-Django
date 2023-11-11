import uuid
from calendar import timegm
from datetime import datetime

import jwt
import pytest
from django.conf import settings as api_settings
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from SocialNetwork import settings
from service.models import User


@pytest.fixture
def test_password():
    return '123456'


@pytest.fixture(scope="function")
def create_user(db, django_user_model, test_password):
    return django_user_model.objects.create_user()


@pytest.fixture(name="user")
def user_fixture(db):
    return User.objects.create_superuser(
        username="test",
        email="test@test",
        password="test",
    )


@pytest.fixture
def api_client(user):
    client = APIClient()
    user.set_password("test")
    user.save()
    client.login(username="test", password="test")
    return client


@pytest.fixture
def auth_bearer_token(db):
    user = User.objects.get(username="test")
    token = TokenObtainPairSerializer().get_token(user).access_token  # noqa
    return str(token)
