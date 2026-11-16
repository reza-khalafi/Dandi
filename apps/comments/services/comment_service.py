from typing import Optional
from django.db.models import QuerySet
from django.contrib.auth.models import User
from apps.comments.models.comment import Comment
from apps.comments.repositories.comment_repository import CommentRepository
from apps.articles.models.article import Article


class CommentService:
    """
    Business logic layer for Comments.
    """

    def __init__(self, comment_repo: Optional[CommentRepository] = None):
        self.comment_repo = comment_repo or CommentRepository()

    def get_approved_comments_for_article(self, article_id: int) -> QuerySet[Comment]:
        return self.comment_repo.get_approved_by_article(article_id=article_id)

    def add_comment(self, article: Article, author: User, content: str, parent_id: Optional[int] = None) -> Comment:
        parent_comment = None
        if parent_id:
            parent_comment = self.comment_repo.get_by_id(parent_id)

        return self.comment_repo.create(
            article=article,
            author=author,
            content=content,
            parent=parent_comment
        )
