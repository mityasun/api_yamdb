import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import Comment, Review, User


from reviews.models import Category, Genre, GenreTitle, Title, Review
from reviews.models import User


class ReviewSerialiser(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Никнейм "me" нельзя регистрировать!'
            )
        return username

    class Meta:
        model = User
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""

    slug = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title
        read_only_fields = ('id', 'rating',)

    def create(self, validated_data):
        genre = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        for i in genre:
            current_genre = Genre.objects.get(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title

    def get_rating(self, obj):
        return Review.objects.filter(title=obj).aggregate(Avg('score'))

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Такой год еще не наступил.')
        return value
