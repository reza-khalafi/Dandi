from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.core.models.base_model import TimeStampedModel
from apps.articles.enums.article_status import ArticleStatus
from apps.articles.models.category import Category
from apps.articles.models.tag import Tag


class Article(TimeStampedModel):
    """
    Main Article entity representing published publications and stories.
    """
    title = models.CharField(max_length=255, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=280, unique=True, allow_unicode=True, verbose_name='نامک')
    summary = models.TextField(max_length=500, verbose_name='چکیده مقاله')
    content = models.TextField(verbose_name='متن کامل مقاله')

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='articles',
        verbose_name='دسته‌بندی'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles',
        verbose_name='برچسب‌ها'
    )
    image = models.ImageField(
        upload_to='articles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='تصویر شاخص'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='نویسنده'
    )
    status = models.CharField(
        max_length=20,
        choices=ArticleStatus.choices,
        default=ArticleStatus.PUBLISHED,
        db_index=True,
        verbose_name='وضعیت انتشار'
    )
    reading_time_minutes = models.PositiveIntegerField(
        default=3,
        verbose_name='زمان تقریبی مطالعه (دقیقه)'
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد بازدید'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='مقاله ویژه'
    )
    published_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name='تاریخ انتشار'
    )

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله‌ها'
        indexes = [
            models.Index(fields=['status', '-published_at']),
        ]

    def __str__(self) -> str:
        return self.title
