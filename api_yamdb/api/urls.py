from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    register_user, get_token)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', register_user, name='register_user'),
    path('v1/auth/token/', get_token, name='token'),
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
