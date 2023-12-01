from rest_framework.fields import CharField
from rest_framework.serializers import (ModelSerializer, Serializer,
                                        ValidationError)

from .models import User


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Имя пользователя не может быть me')
        return value


class TokenSerializer(Serializer):

    username = CharField(required=True)
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

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Имя пользователя не может быть me')
        return value


class MyProfileSerializer(ModelSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
