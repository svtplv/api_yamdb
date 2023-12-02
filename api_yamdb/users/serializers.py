from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from .models import User


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Имя пользователя не может быть me')
        return value


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


class TokenSerializer(ModelSerializer):

    confirmation_code = SerializerMethodField('get_token')

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def get_token(self, obj):
        return obj
    
