from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, GetToken, Signup,
                    TitleViewSet, UserViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', Signup),
    path('v1/auth/token/', GetToken),
]
