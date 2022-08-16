from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, get_token,
                    UserViewSet, register_user)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

# я тут упростил regex по подсказкам пайчарма
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
