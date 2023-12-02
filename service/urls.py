from django.urls import path
from .views import db_check, UserProfileModelViewSet, SelfProfileModelViewSet, FriendProfileModelViewSet, \
    ChangePasswordAPIView, ChangeEmailAPIView, ChangeUserInfoAPIView, AlbumAPIView, PhotoAPIView, DialogsListAPIView, \
    DialogAPIView, RegistrationUserAPIView, MessageCreateAPIView, redirect_to_fs_upload

urlpatterns = [
    path('check/', db_check),
    path('user_profile/<int:pk>', UserProfileModelViewSet.as_view({'get': 'retrieve'})),  # Просмотр любого профиля
    path('self_profile', SelfProfileModelViewSet.as_view({'get': 'list'}), name="self_profile"),  # Просмотр Своего профился
    path('friend_profile/<int:pk>', FriendProfileModelViewSet.as_view()),  # Просмотр профился друга
    path('self_profile/change_password', ChangePasswordAPIView.as_view()),  # Изменение пароля
    path('self_profile/change_email/<int:pk>', ChangeEmailAPIView.as_view()),  # Изменение почты
    path('self_profile/change_info/<int:pk>', ChangeUserInfoAPIView.as_view()),  # Изменение информации профиля
    path('user_profile/album/<int:album_pk>', AlbumAPIView.as_view()),  # Просмотр Альбомов
    path('user_profile/album/photo/<int:pk>', PhotoAPIView.as_view()),  # Просмотр Фотографии
    path('self_profile/dialogs', DialogsListAPIView.as_view()),  # Просмотр Диалогов
    path('self_profile/dialogs/<int:pk>', DialogAPIView.as_view()),  # Просмотр Диалога, Отправка, Изменение, сообщений
    path('self_profile/dialogs/create_message', MessageCreateAPIView.as_view()),  # Создание сообщений в диолог
    path('user_registration', RegistrationUserAPIView.as_view()),  # Регистрация
    path('photo/download/<str:uuid_slug>', redirect_to_fs_upload, name="photo-download"),  #

    # Просмотр фотографии
    #
]
