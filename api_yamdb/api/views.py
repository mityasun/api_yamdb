from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .mixins import ListCreateDestroyGenericViewSet
from .permissions import (IsAdmin, IsAdminModeratorAuthorOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitlePostSerializer,
                          TitleSerializer, TokenSerializer, UserEditSerializer,
                          UserSerializer)


class CategoryViewSet(ListCreateDestroyGenericViewSet):
    """Вьюсет для модели Category"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(ListCreateDestroyGenericViewSet):
    """Вьюсет для модели Genre"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title"""

    ACTIONS = ['create', 'partial_update']
    serializer_class = TitlePostSerializer
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action in self.ACTIONS:
            return TitlePostSerializer
        return TitleSerializer


@api_view(['POST'])
def register_user(request):
    """Функция регистрации user, генерации и отправки кода на почту"""

    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        raise ValidationError('username или email заняты!')
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    """Функция выдачи токена"""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = RefreshToken.for_user(user)
        return Response(
            {'access': str(token.access_token)}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'

    @action(
        methods=['get', 'patch'],
        detail=False, url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def get_edit_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment"""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)
