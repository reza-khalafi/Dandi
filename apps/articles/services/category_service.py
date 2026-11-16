from typing import Optional, List
from django.db.models import QuerySet
from apps.articles.models.category import Category
from apps.articles.repositories.category_repository import CategoryRepository


class CategoryService:
    """
    Business logic layer for Category domain.
    """

    def __init__(self, category_repo: Optional[CategoryRepository] = None):
        self.category_repo = category_repo or CategoryRepository()

    def get_active_categories(self) -> QuerySet[Category]:
        return self.category_repo.get_all_active()

    def get_categories_with_counts(self) -> QuerySet[Category]:
        return self.category_repo.get_with_published_counts()

    def get_category_by_slug(self, slug: str) -> Optional[Category]:
        return self.category_repo.get_by_slug(slug)
