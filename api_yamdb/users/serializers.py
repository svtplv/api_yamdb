from django.conf import settings
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import User
from .validators import validate_username


class SignUpSerializer(Serializer):

    username = CharField(
        max_length=settings.MAX_USERS_NAME,
        required=True,
        validators=(validate_username,)
    )
    email = EmailField(max_length=settings.MAX_EMAIL, required=True)


class TokenSerializer(Serializer):

    username = CharField(max_length=settings.MAX_USERS_NAME, required=True)
    confirmation_code = CharField(required=True)


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MyProfileSerializer(ModelSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
