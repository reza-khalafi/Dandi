from typing import Optional, Tuple
from django.core.paginator import Paginator, Page
from django.db.models import QuerySet
from apps.articles.models.article import Article
from apps.articles.repositories.article_repository import ArticleRepository


class ArticleService:
    """
    Business logic layer for Article domain.
    """

    def __init__(self, article_repo: Optional[ArticleRepository] = None):
        self.article_repo = article_repo or ArticleRepository()

    def get_articles_page(
        self,
        query: str = '',
        category_slug: str = '',
        page: int = 1,
        per_page: int = 6
    ) -> Tuple[Page, int]:
        """
        Retrieves filtered and paginated articles.
        Returns a tuple of (Page object, total count).
        """
        queryset = self.article_repo.search(query=query, category_slug=category_slug)
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        return page_obj, paginator.count

    def get_article_detail_and_track_view(self, slug: str) -> Optional[Article]:
        """
        Finds article by slug and safely increments view counter.
        """
        article = self.article_repo.get_by_slug(slug)
        if article:
            self.article_repo.increment_views(article.pk)
            # Update local instance view count to reflect immediate change
            article.views_count += 1
        return article

    def get_featured_articles(self, limit: int = 3) -> QuerySet[Article]:
        return self.article_repo.get_featured(limit=limit)

    def get_related_articles(self, article: Article, limit: int = 3) -> QuerySet[Article]:
        """
        Returns other published articles from the same category.
        """
        return (
            self.article_repo.get_published()
            .filter(category=article.category)
            .exclude(pk=article.pk)[:limit]
        )
