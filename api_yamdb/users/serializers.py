from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import User


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


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


class MyProfileSerializer(ModelSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
