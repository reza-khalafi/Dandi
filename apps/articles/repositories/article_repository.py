from typing import Optional
from django.db.models import QuerySet, Q, F
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class ArticleRepository:
    """
    Database access layer for Article model.
    """

    @staticmethod
    def get_published() -> QuerySet[Article]:
        return (
            Article.objects
            .filter(status=ArticleStatus.PUBLISHED)
            .select_related('category', 'author')
            .prefetch_related('tags')
            .order_by('-published_at', '-created_at')
        )

    @staticmethod
    def get_featured(limit: int = 3) -> QuerySet[Article]:
        return (
            Article.objects
            .filter(status=ArticleStatus.PUBLISHED, is_featured=True)
            .select_related('category', 'author')
            .prefetch_related('tags')
            .order_by('-published_at')[:limit]
        )

    @staticmethod
    def get_by_category_slug(category_slug: str) -> QuerySet[Article]:
        return (
            ArticleRepository.get_published()
            .filter(category__slug=category_slug)
        )

    @staticmethod
    def search(query: str = '', category_slug: str = '') -> QuerySet[Article]:
        qs = ArticleRepository.get_published()

        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        if query:
            clean_query = query.strip()
            qs = qs.filter(
                Q(title__icontains=clean_query) |
                Q(summary__icontains=clean_query) |
                Q(content__icontains=clean_query) |
                Q(tags__name__icontains=clean_query) |
                Q(category__name__icontains=clean_query)
            ).distinct()

        return qs

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Article]:
        try:
            return (
                Article.objects
                .select_related('category', 'author')
                .prefetch_related('tags')
                .get(slug=slug, status=ArticleStatus.PUBLISHED)
            )
        except Article.DoesNotExist:
            return None

    @staticmethod
    def get_by_id(article_id: int) -> Optional[Article]:
        try:
            return (
                Article.objects
                .select_related('category', 'author')
                .prefetch_related('tags')
                .get(pk=article_id)
            )
        except Article.DoesNotExist:
            return None

    @staticmethod
    def increment_views(article_id: int) -> None:
        Article.objects.filter(pk=article_id).update(views_count=F('views_count') + 1)
