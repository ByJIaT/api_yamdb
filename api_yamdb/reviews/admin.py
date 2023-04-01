from django.contrib import admin

from reviews.models import Title, Review, Category, Genre, Comment, GenreTitle


class GenreTitleInLine(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreTitleInLine,)
    list_display = (
        'pk', 'name', 'year', 'description', 'category', 'get_genre',
    )
    search_fields = ('name',)
    list_filter = ('category', 'genre', 'name', 'year')
    empty_value_display = '-пусто-'

    @admin.display(description='Жанр')
    def get_genre(self, obj):
        return '\n'.join([genre.name for genre in obj.genre.all()])


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = (GenreTitleInLine,)
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'score', 'pub_date')
    search_fields = ('author',)
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    search_fields = ('author',)
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'
