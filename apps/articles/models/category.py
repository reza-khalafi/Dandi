from django.db import models
from apps.core.models.base_model import TimeStampedModel


class Category(TimeStampedModel):
    """
    Article Category model.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, verbose_name='نامک')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=50, default='bookmark', blank=True, verbose_name='آیکون')
    color_accent = models.CharField(max_length=30, default='violet', verbose_name='رنگ تم')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self) -> str:
        return self.name
