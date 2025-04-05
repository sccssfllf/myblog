from django.contrib import admin
from .models import ModelPost

# Register your models here.

@admin.register(ModelPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'published_date', 'created_at') # What to show in list
    list_filter = ('published', 'author', 'created_at') # Filters for display list
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_date',)
