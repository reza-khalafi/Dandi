from django.db import models


class ArticleStatus(models.TextChoices):
    """
    Lifecycle status enumeration for articles.
    """
    DRAFT = 'draft', 'پیش‌نویس'
    PUBLISHED = 'published', 'منتشر شده'
    ARCHIVED = 'archived', 'بایگانی شده'
