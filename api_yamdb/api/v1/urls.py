from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APISignUp, APIToken, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, 'user')
router_v1.register('titles', TitleViewSet, 'title')
router_v1.register('categories', CategoryViewSet, 'category')
router_v1.register('genres', GenreViewSet, 'genre')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews'
)

auth_urlpatterns = [
    path('signup/', APISignUp.as_view(), name='signup'),
    path('token/', APIToken.as_view(), name='token'),
]


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urlpatterns)),
]
