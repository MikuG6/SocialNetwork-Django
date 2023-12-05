from django.urls import path
from rest_framework import routers

from .views import db_check, UserProfileModelViewSet, SelfProfileModelViewSet, FriendProfileModelViewSet, \
    AlbumAPIView, PhotoAPIView, DialogsListAPIView, DialogAPIView, RegistrationUserAPIView, \
    MessageCreateAPIView, redirect_to_fs_upload, AddPhotoAPIView, PhotoViewSet

router = routers.SimpleRouter()
router.register(r'self_profile', SelfProfileModelViewSet)

urlpatterns = [
    path('check/', db_check),
    path('user_profile/<int:pk>', UserProfileModelViewSet.as_view({'get': 'retrieve'})),  # Просмотр любого профиля
    # path('self_profile', SelfProfileModelViewSet.as_view({'get': 'list'}), name="self_profile"),  # Просмотр Своего профился
    path('friend_profile/<int:pk>', FriendProfileModelViewSet.as_view()),  # Просмотр профился друга
    path('user_profile/album/<int:album_pk>', AlbumAPIView.as_view()),  # Просмотр Альбомов
    path('user_profile/album/photo/<int:pk>', PhotoAPIView.as_view()),  # Просмотр Фотографии
    path('self_profile/avatar/<str:photo_uuid>', AddPhotoAPIView.as_view(), name="set-avatar"),  # загрузка фото
    path('self_profile/photos', PhotoViewSet.as_view({'get': 'list'})),  # Просмотр Диалогов
    path('self_profile/dialogs', DialogsListAPIView.as_view()),  # Просмотр Диалогов
    path('self_profile/dialogs/<int:pk>', DialogAPIView.as_view()),  # Просмотр Диалога, Отправка, Изменение, сообщений
    path('self_profile/dialogs/create_message', MessageCreateAPIView.as_view()),  # Создание сообщений в диолог
    path('user_registration', RegistrationUserAPIView.as_view()),  # Регистрация
    path('photo/download/<str:photo_uuid>', redirect_to_fs_upload, name="photo-download"),  # загрузка фото
    # Просмотр фотографии
    #
]

urlpatterns += router.urls