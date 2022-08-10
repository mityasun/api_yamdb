from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from . import views 

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
#router_v1.register(r'genres/(?P<slug>[-a-zA-Z0-9_]+)/$', GenreDestroy, basename='genre_del')
router_v1.register('titles', TitleViewSet, basename='titles')
# удаление по слаг, не ид 

urlpatterns = [
    #re_path(r'^v1/genres/(?P<slug>[-a-zA-Z0-9_]+)/$', views.hallo, name='genre_destroy' ),
    path('v1/', include(router_v1.urls)),
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

# делит не работает на 2 моделях, нужно сделать  эндпоинт удаление по слаг 
# пагинация,  поиск пермишны
# 1 модели нужно ли переоперделять поля? 
#rating убрать из модели,  обработка на уровне сериализера 
#сериализер титле категория и жанры и апдейт