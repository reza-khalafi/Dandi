from django.db import models
from django.contrib.auth.models import User
from apps.core.models.base_model import TimeStampedModel


class Conversation(TimeStampedModel):
    """
    Represents an ongoing or archived chat session between a user and Dandi Assistant.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assistant_conversations',
        verbose_name='کاربر'
    )
    title = models.CharField(
        max_length=255,
        default='گفتگوی جدید',
        verbose_name='عنوان گفتگو'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='نشست فعال'
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'نشست گفتگو'
        verbose_name_plural = 'نشست‌های گفتگو'

    def __str__(self) -> str:
        return f"{self.user.username} - {self.title} ({self.created_at.strftime('%Y-%m-%d')})"
