from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from reviews.models import Category, Genre, GenreTitle, Title, Review
import datetime as dt

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    # req = True  
    
    slug = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    #slug = serializers.SlugRelatedField(queryset=Genre.objects.all(), slug_field='slug')

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.SerializerMethodField()
    # КАК ВЛОЖИТЬ 1 ОБЪЕКТ В ЗАПРОС?  КАТЕГОРИ 

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
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

    # def update 

    def get_rating(self, obj):
        return Review.objects.filter(title=obj).aggregate(Avg('score'))

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Такой год еще не наступил.')
        return value
