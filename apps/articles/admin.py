from django.contrib import admin
from apps.articles.models import Category, Tag, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'reading_time_minutes', 'views_count', 'is_featured', 'published_at')
    list_filter = ('status', 'is_featured', 'category', 'published_at')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)
