from django.db import models
from apps.core.models.base_model import TimeStampedModel


class Tag(TimeStampedModel):
    """
    Article Tag micro-model for granular taxonomy.
    """
    name = models.CharField(max_length=60, unique=True, verbose_name='عنوان تگ')
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True, verbose_name='نامک تگ')

    class Meta:
        ordering = ['name']
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'

    def __str__(self) -> str:
        return f'#{self.name}'
