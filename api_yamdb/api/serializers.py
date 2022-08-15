import datetime as dt

from django.conf import settings
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from users.validators import ValidateUsername


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review"""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate_score(self, value):
        if not (settings.MIN_SCORE <= value <= settings.MAX_SCORE):
            raise serializers.ValidationError(
                'Вы можете поставить оценку от 1 до 10'
            )
        return value

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
        read_only_fields = ('title', 'review')


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    """Сериализатор модели User"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = ('username',)


class RegistrationSerializer(UserSerializer, ValidateUsername):
    """Сериализатор регистрации User"""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(UserSerializer, ValidateUsername):
    """Сериализатор токена"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
    # я тут мету не удалил, потому что без нее валится тест,
    # требует в филдах конфирмэйшен код


class UserEditSerializer(UserSerializer, ValidateUsername):
    """Сериализатор модели User для get и patch"""

    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title
    (предназначенный для чтения данных)
    """

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        ]

    def get_rating(self, obj):
        return Review.objects.filter(
            title=obj.id).aggregate(Avg('score'))['score__avg']


class TitlePostSerializer(TitleSerializer):
    """
    Сериализатор для модели Title
    (предназначенный для записи данных)
    """

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Такой год еще не наступил.')
        return value
