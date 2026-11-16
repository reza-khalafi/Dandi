from django.db import models
from apps.core.models.base_model import TimeStampedModel
from apps.assistant.models.conversation import Conversation


class ChatMessage(TimeStampedModel):
    """
    Stores an individual message within an assistant conversation.
    """
    class SenderChoices(models.TextChoices):
        USER = 'user', 'کاربر'
        ASSISTANT = 'assistant', 'دستیار'

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='نشست'
    )
    sender = models.CharField(
        max_length=10,
        choices=SenderChoices.choices,
        verbose_name='فرستنده'
    )
    content = models.TextField(
        verbose_name='متن پیام'
    )
    suggested_articles_data = models.JSONField(
        default=list,
        blank=True,
        verbose_name='داده‌های مقالات پیشنهادی'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'پیام گفتگو'
        verbose_name_plural = 'پیام‌های گفتگو'

    def __str__(self) -> str:
        return f"[{self.sender}] {self.content[:40]}..."
