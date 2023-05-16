from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, gettoken,
                    ReviewViewSet, signup, TitleViewSet, UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', gettoken),
]
