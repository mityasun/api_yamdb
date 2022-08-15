from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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

    filter_backends = [filters.SearchFilter]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]


class APICategoryDelete(APIView):
    """Реализация метода DELETE для модели Category"""

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(ListCreateDestroyGenericViewSet):
    """Вьюсет для модели Genre"""

    filter_backends = (filters.SearchFilter,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]


class APIGenreDelete(APIView):
    """Реализация метода DELETE для модели Genre"""

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title"""

    http_method_names = ['get', 'post', 'patch', 'delete']
    ACTIONS = ['create', 'partial_update']
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

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
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация в проекте YaMDb.',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        print(f"Ошибка username или email уже заняты: {error}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if request.method == 'GET' or 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review"""

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment"""

    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        title = self.get_title()
        review = self.get_review()
        serializer.save(title=title, review=review, author=self.request.user)
