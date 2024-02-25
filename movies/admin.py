from django.contrib import admin
from .models import Movie, Category, Comment, Rating


# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'actors', 'uploaded_by', 'release_date', 'category', 'created', 'updated']
    list_display_links = ['release_date']
    list_editable = ['name', 'uploaded_by', 'category', 'actors']
    # prepopulated_fields = {'slug':('name',)}
    list_per_page = 20
admin.site.register(Movie, MovieAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'movie', 'user']
    list_display_links = ['movie', 'user']
    list_editable = ['content']
admin.site.register(Comment, CommentAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ['value', 'movie', 'user']
    list_display_links = ['movie', 'user']
    list_editable = ['value']
admin.site.register(Rating, RatingAdmin)
