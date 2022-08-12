import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import Category, Genre, GenreTitle, Title, Review, Comment
from users.models import User


class ReviewSerialiser(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True, default=serializers.CurrentUserDefault()
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
        slug_field='username', read_only=True, default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации User"""

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Ник "me" нельзя регистрировать!')
        return username

    class Meta:
        model = User
        fields = ['username', 'email']


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор токена"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class UserEditSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для get и patch"""

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
        read_only_fields = ['role']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    
    class Meta:
        fields = ('name', 'slug',)
        model = Category
    
    def __str__(self):
        return self.name


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    
    class Meta:
        fields = ('name', 'slug',)
        model = Genre

    def __str__(self):
        return self.name 


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""

    class GenSer(GenreSerializer):
        name = StringRelatedField(read_only=True)

    class CatSer(CategorySerializer):
        name = StringRelatedField(read_only=True)

    genre = GenSer(many=True)
    category = CatSer(many=False)
    rating = serializers.SerializerMethodField(required=False)
    description = serializers.CharField(required=False)
    
    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
        read_only_fields = ('id', 'rating',)
 
    def create(self, validated_data):
        genre = validated_data.pop('genre')
        #category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        for i in genre:
            current_genre = Genre.objects.get(slug=genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title

    # def update 

    def get_rating(self, obj):
        return Review.objects.filter(title=obj.id).aggregate(Avg('score'))['score__avg']

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Такой год еще не наступил.')
        return value