import re

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import (MyProfileSerializer, SignUpSerializer,
                          TokenSerializer, UserSerializer)


class APISignUp(APIView):

    @staticmethod
    def user_exists(errors):
        re_errors = re.findall("(?<=code=').*?(?=')", repr(errors))
        return re_errors == ['unique', 'unique']

    @staticmethod
    def send_message(recipient):
        confirmation_code = PasswordResetTokenGenerator().make_token(recipient)
        message = EmailMessage(
            subject='Регистрация',
            body=f'Ваш код подтверждения: {confirmation_code}',
            to=(recipient.email,)
        )
        message.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_message(user)
            return Response(serializer.data, HTTP_200_OK)
        if self.user_exists(serializer.errors):
            user = get_object_or_404(User, username=request.data['username'])
            self.send_message(user)
            return Response(serializer.data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'delete', 'patch')

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
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден'}, HTTP_404_NOT_FOUND
            )
        code = request.data['confirmation_code']
        if PasswordResetTokenGenerator().check_token(user, code):
            jwt_token = AccessToken.for_user(user)
            return Response({'token': str(jwt_token)}, HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Некорректный код'}, HTTP_400_BAD_REQUEST
        )
