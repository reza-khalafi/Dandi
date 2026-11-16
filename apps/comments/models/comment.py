from django.db import models
from django.contrib.auth.models import User
from apps.core.models.base_model import TimeStampedModel
from apps.comments.enums.comment_status import CommentStatus
from apps.articles.models.article import Article


class Comment(TimeStampedModel):
    """
    Comment entity representing reader feedback on articles.
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='مقاله'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='نویسنده دیدگاه'
    )
    content = models.TextField(
        max_length=1500,
        verbose_name='متن دیدگاه'
    )
    status = models.CharField(
        max_length=20,
        choices=CommentStatus.choices,
        default=CommentStatus.APPROVED,
        db_index=True,
        verbose_name='وضعیت دیدگاه'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='پاسخ به'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه‌ها'

    def __str__(self) -> str:
        return f'{self.author.username} - {self.article.title[:30]}'
