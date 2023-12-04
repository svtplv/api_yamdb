from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from .models import User
from .serializers import (MyProfileSerializer, SignUpSerializer,
                          TokenSerializer, UserSerializer)


class APISignUp(APIView):

    @staticmethod
    def send_message(recipient):
        confirmation_code = default_token_generator.make_token(recipient)
        message = EmailMessage(
            subject='Регистрация',
            body=f'Ваш код подтверждения: {confirmation_code}',
            to=(recipient.email,)
        )
        message.send()

    @staticmethod
    def get_error(user):
        USERNAME_TAKEN = {
            'username': [
                'Пользователь с таким username уже существует.'
            ]
        }
        EMAIL_TAKEN = {'email': ['Пользователь с таким email уже существует.']}
        return (
            USERNAME_TAKEN if user and user.email else EMAIL_TAKEN
        )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(username=request.data['username']).first()
        email_user = User.objects.filter(email=request.data['email']).first()
        if any((
            user == email_user,
            not email_user and user and not user.email,
        )):
            if not email_user:
                user, _ = User.objects.update_or_create(
                    **serializer.validated_data
                )
            self.send_message(user)
            return Response(serializer.data, HTTP_200_OK)
        return Response(self.get_error(user), HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = settings.ALLOWED_METHODS

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='my_profile',
        permission_classes=(IsAuthenticated,),
        serializer_class=MyProfileSerializer,
    )
    def check_personal_info(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
        else:
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, HTTP_200_OK)


class APIToken(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])
        code = request.data['confirmation_code']
        if not default_token_generator.check_token(user, code):
            return Response(
                {'confirmation_code': 'Некорректный код'}, HTTP_400_BAD_REQUEST
            )
        jwt_token = AccessToken.for_user(user)
        return Response({'token': str(jwt_token)}, HTTP_201_CREATED)
