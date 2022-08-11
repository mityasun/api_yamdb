from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)

class GenreTitleInline(admin.TabularInline):
    model = Title.genre.through

class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year',   'category', 'description') 
    search_fields = ('name', 'description')
    list_filter = ('year',  'category', 'genre')
    empty_value_display = '-не указано-'
    inlines = [GenreTitleInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
