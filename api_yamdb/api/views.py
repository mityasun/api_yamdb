from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets
# Create your views here.
class CategoryViewsSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post"""
    pass
class GenreViewsSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post"""
    pass
class TitleViewsSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post"""
    pass