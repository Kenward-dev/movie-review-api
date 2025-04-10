from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'imdb_rating')
    list_filter = ('year', 'genre')
    search_fields = ('title', 'director', 'actors')
    ordering = ('title',)