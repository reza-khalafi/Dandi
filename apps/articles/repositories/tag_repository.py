from typing import Optional
from django.db.models import QuerySet
from apps.articles.models.tag import Tag


class TagRepository:
    """
    Database access layer for Tag model.
    """

    @staticmethod
    def get_all() -> QuerySet[Tag]:
        return Tag.objects.all().order_by('name')

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Tag]:
        try:
            return Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            return None

    @staticmethod
    def get_or_create(name: str, slug: str) -> Tag:
        tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
        return tag
