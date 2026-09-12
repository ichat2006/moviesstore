from django.contrib import admin
from .models import Movie, Review
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
class ReviewAdmin(admin.ModelAdmin):
    list_show = [
        'id',
        'movie',
        'user',
        'date',
        'reported',
    ]
    list_filter = [
        'reported',
    ]
    search_fields = [
        'comment',
        'user_username',
        'movie_name',
    ]
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
