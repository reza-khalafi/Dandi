from typing import Optional, List
from django.db.models import QuerySet, Count, Q
from apps.articles.models.category import Category
from apps.articles.enums.article_status import ArticleStatus


class CategoryRepository:
    """
    Database access layer for Category model.
    """

    @staticmethod
    def get_all_active() -> QuerySet[Category]:
        return Category.objects.filter(is_active=True).order_by('order', 'name')

    @staticmethod
    def get_with_published_counts() -> QuerySet[Category]:
        return Category.objects.filter(is_active=True).annotate(
            published_articles_count=Count(
                'articles',
                filter=Q(articles__status=ArticleStatus.PUBLISHED)
            )
        ).order_by('order', 'name')

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Category]:
        try:
            return Category.objects.get(slug=slug, is_active=True)
        except Category.DoesNotExist:
            return None

    @staticmethod
    def get_by_id(category_id: int) -> Optional[Category]:
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return None
