from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year',  'genre', 'category', 'description')
    search_fields = ('name', 'description')
    list_filter = ('year',  'category', 'genre')
    empty_value_display = '-не указано-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'title', 'text', 'score', 'pub_date'
    )
    search_fields = ('title', 'text')
    list_filter = ('author', 'title', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'title', 'review', 'text', 'pub_date'
    )
    search_fields = ('title', 'text', 'review')
    list_filter = ('author', 'title', 'review', 'pub_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
