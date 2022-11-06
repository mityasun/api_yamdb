from django.conf import settings
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import ValidateUsername

from api_yamdb.settings import EMAIL, USERNAME_NAME


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review"""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        min_value=settings.MIN_SCORE, max_value=settings.MAX_SCORE
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                author=self.context['request'].user,
                title=self.context['view'].kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment"""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    """Сериализатор модели User"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = ('username',)


class RegistrationSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор регистрации User"""

    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    email = serializers.EmailField(required=True, max_length=EMAIL)


class TokenSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор токена"""

    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    confirmation_code = serializers.CharField(required=True)


class UserEditSerializer(UserSerializer):
    """Сериализатор модели User для get и patch"""

    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title (предназначенный для чтения данных)."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title (предназначенный для записи данных)"""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'genre', 'category', 'rating'
        )
        read_only_fields = ('id', 'rating')

    def to_representation(self, value):
        return TitleSerializer(value, context=self.context).data
