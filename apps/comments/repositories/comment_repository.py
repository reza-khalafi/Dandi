from typing import Optional
from django.db.models import QuerySet
from django.contrib.auth.models import User
from apps.comments.models.comment import Comment
from apps.comments.enums.comment_status import CommentStatus
from apps.articles.models.article import Article


class CommentRepository:
    """
    Database access layer for Comment model.
    """

    @staticmethod
    def get_approved_by_article(article_id: int) -> QuerySet[Comment]:
        return (
            Comment.objects
            .filter(article_id=article_id, status=CommentStatus.APPROVED, parent__isnull=True)
            .select_related('author')
            .prefetch_related('replies__author')
            .order_by('-created_at')
        )

    @staticmethod
    def create(article: Article, author: User, content: str, parent: Optional[Comment] = None) -> Comment:
        return Comment.objects.create(
            article=article,
            author=author,
            content=content.strip(),
            status=CommentStatus.APPROVED,
            parent=parent
        )

    @staticmethod
    def get_by_id(comment_id: int) -> Optional[Comment]:
        try:
            return Comment.objects.select_related('author', 'article').get(pk=comment_id)
        except Comment.DoesNotExist:
            return None
