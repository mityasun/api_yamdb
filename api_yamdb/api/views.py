from django_filters import rest_framework as flt
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .mixins import ListCreateGenericViewSet
from .permissions import (IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly,
                          IsAdmin)
from .serializers import (RegistrationSerializer, TokenSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerialiser, CommentSerializer, UserSerializer,
                          UserEditSerializer, TitlePostSerializer)


class CategoryViewSet(ListCreateGenericViewSet):
    """Вьюсет для модели Category"""

    filter_backends = (filters.SearchFilter,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]


class APICategoryDelete(APIView):
    """Реализация метода DELETE для модели Category"""

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, slug):
        # переписано category = Category.objects.get(slug=slug)
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(ListCreateGenericViewSet):
    """Вьюсет для модели Genre"""

    filter_backends = (filters.SearchFilter,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]


class APIGenreDelete(APIView):
    """Реализация метода DELETE для модели Genre"""

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, slug):
        # переписано genre = Genre.objects.get(slug=slug)
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleFilter(flt.FilterSet):
    name = flt.CharFilter(field_name='name', lookup_expr='icontains')
    year = flt.NumberFilter(field_name='year')
    category = flt.CharFilter(field_name='category__slug')
    genre = flt.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title"""

    ACTIONS = ['create', 'update', 'partial_update']
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in self.ACTIONS:
            return TitlePostSerializer
        return TitleSerializer

    def perform_destroy(self, serializer):
        # переписано title_id = self.kwargs.get('id')
        # переписано title = Title.objects.get(id=title_id)
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        title.delete()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Функция регистрации user, генерации и отправки кода на почту"""

    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User, username=serializer.data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='info@yamdb.ru',
        recipient_list=[serializer.validated_data['email']]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
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
    permission_classes = [IsAdmin]
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False, url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def get_edit_user(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review"""

    serializer_class = ReviewSerialiser
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_title(self):
        # переписано title_id = self.kwargs.get('title_id')
        # переписано title = get_object_or_404(Title, id=title_id)
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))
        # переписано return title

    def get_queryset(self):
        # переписано title = self.get_title()
        # переписано new_queryset = title.reviews.all()
        return self.get_title().reviews.all()
        # переписано return new_queryset

    def perform_create(self, serializer):
        # переписано title = self.get_title()
        # переписано serializer.save(title=title, author=self.request.user)
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment"""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_title(self):
        # переписано title_id = self.kwargs.get('title_id')
        # переписано title = get_object_or_404(Title, id=title_id)
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))
        # переписано return title

    def get_review(self):
        # переписано  title = self.get_title()
        review_id = self.kwargs.get('review_id')
        # переписано review = get_object_or_404(Review, title=self.get_title(), id=review_id)
        return get_object_or_404(Review, title=self.get_title(), id=review_id)
        # переписано  return review

    def get_queryset(self):
        # переписано  review = self.get_review()
        # переписано  new_queryset = review.comments.all()
        return self.get_review().comments.all()
        # переписано  return new_queryset

    def perform_create(self, serializer):
        # переписано title = self.get_title()
        # переписано review = self.get_review()
        # переписано serializer.save(title=title, review=review, author=self.request.user)
        serializer.save(
            title=self.get_title(),
            review=self.get_review(),
            author=self.request.user
        )
