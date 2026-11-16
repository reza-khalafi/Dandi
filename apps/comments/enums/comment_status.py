from django.db import models


class CommentStatus(models.TextChoices):
    """
    Status enumeration for user comments moderation.
    """
    PENDING = 'pending', 'در انتظار بررسی'
    APPROVED = 'approved', 'تایید شده'
    REJECTED = 'rejected', 'رد شده'
