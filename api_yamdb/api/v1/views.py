from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import GenreCategoryMixin
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MyProfileSerializer,
                          ReviewSerializer, SignUpSerializer, TitleSerilizer,
                          TokenSerializer, UserSerializer)


class APISignUp(APIView):
    """APIView для регистрации пользоватей и выдачи кода подтверждения."""
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
        if user != email_user and (email_user or user.email):
            return Response(self.get_error(user), HTTP_400_BAD_REQUEST)
        user, _ = User.objects.get_or_create(
            **serializer.validated_data
        )
        self.send_message(user)
        return Response(serializer.data, HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели User."""
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
    """APIView для получения JWT-токена."""
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
        return Response({'token': str(jwt_token)}, HTTP_200_OK)


class GenreViewSet(GenreCategoryMixin):
    """ViewSet для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    """ViewSet для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerilizer
    http_method_names = settings.ALLOWED_METHODS
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorStaffOrReadOnly, )
    http_method_names = settings.ALLOWED_METHODS

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(
            author=self.request.user, review=review
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorStaffOrReadOnly,)
    http_method_names = settings.ALLOWED_METHODS

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title()
        )
