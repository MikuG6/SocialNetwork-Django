from urllib import parse

from django.urls import reverse
from rest_framework import serializers

from service.models import User, Photo, Album, Friend, Dialog, Message


class PhotoSerializer(serializers.ModelSerializer):
    """ Сериализатор для фото """

    class Meta:
        model = Photo
        fields = ["uuid", "description", "time_creation"]


class AlbumSerializer(serializers.ModelSerializer):
    """ Сериализатор для альбомов с фото """
    photos = PhotoSerializer(many=True, )

    class Meta:
        model = Album
        fields = ["name", "time_creation", "photos"]


class UserProfileSerializer(serializers.ModelSerializer):
    """ Сериализатор для профиля кторый просматривает пользователь не являющимся другом """
    albums = AlbumSerializer(many=True, )
    custom_field = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["last_login", "username", "first_name", "last_name", "date_joined", "albums", "custom_field"]

    def get_custom_field(self, obj):
        return str(obj)


class LinkCreationDataSerializer(serializers.ModelSerializer):
    # Нужно допилить заявки в друзья и отображения для кнопок
    """ Сериализатор для отображения даты добавления в друзья """

    class Meta:
        model = Friend
        fields = ["time_creation"]


class FriendProfileSerializer(UserProfileSerializer):
    """ Сериализатор для отображения профиля друга """
    friends_to = LinkCreationDataSerializer(many=True, )

    def get_field_names(self, declared_fields, info):
        return self.Meta.fields + super().Meta.fields


class SelfProfileSerializer(UserProfileSerializer):
    """ Сериализатор для отображения профиля пользователя который аунтифицирован """
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if obj.avatar:
            return parse.urljoin(self.context.get('hostname'), obj.avatar.download_link)
        else:
            return None

    class Meta:
        model = User
        exclude = ["id", "is_superuser", "is_staff", "is_active", "groups", "user_permissions", "password"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    """ Сериализатор для изменения пароля """

    class Meta:
        model = User
        fields = ["password"]


class ChangeEmailSerializer(serializers.ModelSerializer):
    """ Сериализатор для изменения почты"""

    class Meta:
        model = User
        fields = ["email"]


class DialogsListSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и добавления диалогов"""

    class Meta:
        model = Dialog
        fields = ["dialogs", "name", "time_create"]


class MessageListSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра всех сообщений в диалоге"""
    class Meta:
        model = Message
        fields = ["text", "time_creation", "time_update", "text_changed"]


class RegistrationUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


class DialogSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)

    class Meta:
        model = Dialog
        fields = ["name", "time_create", "user"]


class MessageCreateSerializer(serializers.ModelSerializer):
    time_creation = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    text_changed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = ["text", "time_creation", "time_update", "text_changed", "user", "dialog"]


class SelfPhotoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    to_avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["uuid", "url", "to_avatar_url"]

    def get_url(self, obj):
        return parse.urljoin(self.context.get('hostname'), obj.download_link)

    def get_to_avatar_url(self, obj):
        return parse.urljoin(
            self.context.get('hostname'),
            f"{reverse('service:set-avatar', kwargs={'photo_uuid': obj.uuid})}"
        )
