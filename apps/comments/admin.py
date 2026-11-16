from django.contrib import admin
from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('author__username', 'article__title', 'content')
    raw_id_fields = ('author', 'article', 'parent')
