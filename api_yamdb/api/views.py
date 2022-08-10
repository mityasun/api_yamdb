from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from reviews.models import Title
from .serializers import CommentSerializer, ReviewSerialiser


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialiser

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def get_queryset(self):
        title = self.get_title()
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
