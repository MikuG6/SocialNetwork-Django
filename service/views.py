import logging

import requests
from django.db import connection, DatabaseError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404
from django.utils.decorators import classonlymethod
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from service.audit import change_log, add_log, delete_log
from service.models import User, Album, Photo, Dialog, Message
from service.serializers import UserProfileSerializer, SelfProfileSerializer, FriendProfileSerializer, \
    ChangePasswordSerializer, ChangeEmailSerializer, AlbumSerializer, PhotoSerializer, \
    DialogsListSerializer, MessageListSerializer, RegistrationUserSerializer, MessageCreateSerializer, \
    SelfPhotoSerializer

logger = logging.getLogger(__name__)


def db_check(request):
    """ Проверка подключения к БД """
    output = "Connected to DB"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            logger.info(output, extra={"user": request.user})
    except DatabaseError:
        output = "Disconnected to DB"
        logger.info(output, extra={"user": request.user})
    return HttpResponse(f"Hello World! {output}")


class UserProfileModelViewSet(viewsets.ModelViewSet):
    """ Как будет отображаться профиль пользователя """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SelfProfileModelViewSet(viewsets.ModelViewSet):
    """ Как будет отображаться свой профиль пользователя """
    queryset = User.objects.all()
    serializer_class = SelfProfileSerializer

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        print(actions)
        return super().as_view(actions=actions, **initkwargs)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            "hostname": self.request.build_absolute_uri('/')
        }

    @action(methods=["post"], detail=False, serializer_class=ChangePasswordSerializer)
    def change_password(self, request, *args, **kwargs):
        try:
            logger.info("Изменение пароля", extra={"user": request.user})
            with change_log(request.user, request.user):
                serializer = self.get_serializer(data=request.data)
                logger.info("Сериализация данных прошла успешно", extra={"user": request.user})
                serializer.is_valid(raise_exception=True)
                logger.info("Сериализированные данные успешно провалидированы", extra={"user": request.user})
                data = serializer.data
                request.user.set_password(data["password"])
                logger.info("Установка захэшированного пароля", extra={"user": request.user})
                request.user.save(update_fields=["password"])
                logger.info("Сохронение захэшированного пароля", extra={"user": request.user})
                headers = self.get_success_headers(serializer.data)
                logger.info("Успешное изменение пароля", extra={"user": request.user})
                return Response(status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Пароль не изменён {e}", extra={"user": request.user})

    @action(methods=["put"], detail=False, serializer_class=ChangeEmailSerializer)
    def change_email(self, request, *args, **kwargs):
        try:
            logger.info("Изменение почты методом PUT", extra={"user": request.user})
            with change_log(request.user, request.user):
                logger.info("Успешное изменение почты", extra={"user": request.user})
                return super().put(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Почта не изменена {e}", extra={"user": request.user})

    def put(self, request, *args, **kwargs):
        try:
            logger.info("Изменение данных пользователя методом PUT", extra={"user": request.user})
            with change_log(request.user, request.user):
                logger.info("Успешное изменение данных пользователя", extra={"user": request.user})
                return super().put(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Данные пользователя не изменены {e}", extra={"user": request.user})

    def patch(self, request, *args, **kwargs):
        try:
            logger.info("Изменение данных пользователя методом PATCH", extra={"user": request.user})
            with change_log(request.user, request.user):
                logger.info("Успешное изменение данных пользователя", extra={"user": request.user})
                return super().patch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Данные пользователя не изменены {e}", extra={"user": request.user})


class FriendProfileModelViewSet(generics.RetrieveAPIView):
    """Как будет отображаться профиль друга"""
    queryset = User.objects.all()
    serializer_class = FriendProfileSerializer


class AlbumAPIView(generics.RetrieveAPIView):
    """Представление для просмотра альбома"""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    lookup_url_kwarg = "album_pk"


class PhotoAPIView(generics.RetrieveAPIView):
    """Представление для отображения одной фотографии"""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class DialogsListAPIView(generics.ListCreateAPIView):
    """Представление для отображения списка диалогов и создания новых"""
    queryset = Dialog.objects.all()
    serializer_class = DialogsListSerializer

    def get_queryset(self):
        return Dialog.objects.filter(users__username="admin")

    def post(self, request, *args, **kwargs):
        try:
            logger.info("Создание диалога", extra={"user": request.user})
            serializer = self.get_serializer(data=request.data)
            logger.info("Сериализация данных прошла успешно", extra={"user": request.user})
            serializer.is_valid(raise_exception=True)
            logger.info("Сериализированные данные успешно провалидированы", extra={"user": request.user})
            self.perform_create(serializer)
            logger.info("Сохранение сериализированных данных", extra={"user": request.user})
            headers = self.get_success_headers(serializer.data)
            add_log(request.user, serializer.instance)
            logger.info("Успешное cоздание диалога", extra={"user": request.user})
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Диалог не изменён {e}", extra={"user": request.user})


class DialogAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для отображения, изменения и удаления конкретного диалога"""
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer

    def patch(self, request, *args, **kwargs):
        try:
            logger.info("Изменение данных диалога методом PATCH", extra={"user": request.user})
            with change_log(request.user, request.user):
                logger.info("Успешное изменение диалога", extra={"user": request.user})
                return super().patch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Диалог не изменён {e}", extra={"user": request.user})

    def delete(self, request, *args, **kwargs):
        try:
            logger.info("Удаление диалога", extra={"user": request.user})
            delete_log(request.user, self.get_object())
            logger.info("Успешное удаление диалога", extra={"user": request.user})
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Диалог не удалён {e}", extra={"user": request.user})


class RegistrationUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            logger.info("Регистрация пользователя", extra={"user": request.user})
            serializer = self.get_serializer(data=request.data)
            logger.info("Сериализация данных прошла успешно", extra={"user": request.user})
            serializer.is_valid(raise_exception=True)
            logger.info("Сериализированные данные успешно провалидированы", extra={"user": request.user})
            self.perform_create(serializer)
            logger.info("Сохранение сериализированных данных", extra={"user": request.user})
            headers = self.get_success_headers(serializer.data)
            add_log(request.user, serializer.instance)
            Album.objects.create(name="Default Album", user=serializer.instance)
            logger.info("Default Album был создан", extra={"user": request.user})
            logger.info("Регистрация прошла успешно", extra={"user": request.user})
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Регистрация провалилась {e}", extra={"user": request.user})


class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer

    def post(self, request, *args, **kwargs):
        try:
            logger.info("Создание сообщения", extra={"user": request.user})
            serializer = self.get_serializer(data=request.data)
            logger.info("Сериализация данных прошла успешно", extra={"user": request.user})
            serializer.is_valid(raise_exception=True)
            logger.info("Сериализированные данные успешно провалидированы", extra={"user": request.user})
            self.perform_create(serializer)
            logger.info("Сохранение сериализированных данных", extra={"user": request.user})
            headers = self.get_success_headers(serializer.data)
            add_log(request.user, serializer.instance)
            logger.info("Сообщение удачно созданно", extra={"user": request.user})
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Сообщение не создано {e}", extra={"user": request.user})


def redirect_to_fs_upload(request, photo_uuid):
    return HttpResponse(
        content=requests.get(f"http://localhost:8010/download/{photo_uuid}").content,
        headers={"Content-Disposition": f'attachment; filename="{photo_uuid}.png"'}
    )


class AddPhotoAPIView(APIView):
    def post(self, request, photo_uuid, *args, **kwargs):
        photo = get_object_or_404(Photo, uuid=photo_uuid)
        if photo.album.user != request.user:
            return JsonResponse({"err_msg": "Cannot set photo to other user"}, status=403)
        request.user.avatar = photo
        request.user.save()
        return JsonResponse({"status": "OK"}, status=200)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = SelfPhotoSerializer

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            "hostname": self.request.build_absolute_uri('/')
        }
