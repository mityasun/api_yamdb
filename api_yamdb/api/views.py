from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title
from users.models import User
from .serializers import (RegistrationSerializer, TokenSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerialiser, CommentSerializer)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Вьюсет для модели Category"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True, methods=['delete'])
    def delete(self, request, slug):
        title = self.get_object(slug)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Genre"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, slug):
        genre = Genre.objects.get(slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title"""

    serializer_class = TitleSerializer
    queryset = Title.objects.all()

    def delete(self, request, slug):
        title = self.get_object(slug)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='info@yamdb.ru',
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def get_review(self):
        pass

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        pass
