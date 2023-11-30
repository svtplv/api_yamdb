import re

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class APISignUp(APIView):

    @staticmethod
    def user_exists(errors):
        re_errors = re.findall("(?<=code=').*?(?=')", repr(errors))
        return re_errors == ['unique', 'unique']

    @staticmethod
    def send_code(email, user):
        confirmation_code = PasswordResetTokenGenerator().make_token(user)
        send_mail(
            'Регистрация',
            'aa@mail.ru',
            f'confirmation_code: {confirmation_code}',
            recipient_list=[email]
        )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = serializer.validated_data.get('email')
            self.send_code(email, user)
            return Response(serializer.data, HTTP_200_OK)
        if self.user_exists(serializer.errors):
            user = get_object_or_404(User, username=request.data['username'])
            self.send_code(request.data['email'], user)
            return Response(serializer.data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer


class APIToken(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        user = get_object_or_404(User, username=request.data['username'])
        code = request.data['confirmation_code']
        if PasswordResetTokenGenerator().check_token(user, code):
            jwt_token = AccessToken.for_user(user)
            return Response({'token': str(jwt_token)}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
