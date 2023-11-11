import logging

from auditlog.mixins import LogAccessMixin
from django.shortcuts import render, HttpResponse
from django.db import connection, DatabaseError
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from service.audit import change_log, add_log, delete_log
from service.models import User, Album, Photo, Dialog, Message
from service.paginations import StandardResultsSetPagination
from service.serializers import UserProfileSerializer, SelfProfileSerializer, FriendProfileSerializer, \
    ChangePasswordSerializer, ChangeEmailSerializer, ChangeUserInfoSerializer, AlbumSerializer, PhotoSerializer, \
    DialogsListSerializer, MessageListSerializer, RegistrationUserSerializer, MessageCreateSerializer


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

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class FriendProfileModelViewSet(generics.RetrieveAPIView):
    """ Как будет отображаться профиль друга """
    queryset = User.objects.all()
    serializer_class = FriendProfileSerializer


class ChangePasswordAPIView(generics.CreateAPIView):
    """ Представление для смены пароля """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):  # Разобрать эту функцию
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


class ChangeEmailAPIView(generics.UpdateAPIView):
    """ представление для изменения почты """
    queryset = User.objects.all()
    serializer_class = ChangeEmailSerializer

    def put(self, request, *args, **kwargs):
        try:
            logger.info("Изменение почты методом PUT", extra={"user": request.user})
            with change_log(request.user, request.user):
                logger.info("Успешное изменение почты", extra={"user": request.user})
                return super().put(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Почта не изменена {e}", extra={"user": request.user})

    def patch(self, request, *args, **kwargs):
        try:
            logger.info("Изменение почты методом PATCH", extra={"user": request.user})
            with change_log(request.user, request.user):
                logger.info("Успешное изменение почты", extra={"user": request.user})
                return super().patch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Почта не изменена {e}", extra={"user": request.user})


class ChangeUserInfoAPIView(generics.UpdateAPIView):
    """ представление для изменения личной информации пользователя """
    queryset = User.objects.all()
    serializer_class = ChangeUserInfoSerializer

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



class AlbumAPIView(LogAccessMixin, generics.RetrieveAPIView):
    """ представлени для просмотра альбома """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    lookup_url_kwarg = "album_pk"


class PhotoAPIView(generics.RetrieveAPIView):
    """Представление для отображения одной фотографии"""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class DialogsListAPIView(generics.ListCreateAPIView):
    """Представление для отображения списка диологов и создания новых"""
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


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination