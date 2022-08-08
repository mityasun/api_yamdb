from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
