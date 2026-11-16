from typing import Any
from pydantic_ai import RunContext
from django.db.models import Q
from apps.articles.repositories.article_repository import ArticleRepository
from apps.assistant.agents.context import AssistantContext
from apps.assistant.schemas.article_item import ArticleItem


MAX_RECOMMENDED_ARTICLES = 3


def search_dandi_articles(ctx: RunContext[AssistantContext], query: str, limit: int = 3) -> list[dict[str, Any]]:
    """
    Search published articles in Dandi magazine database by topic, keywords, or title.
    Returns 2 to 3 most relevant articles to recommend to the reader.
    """
    clean_query = query.strip()
    if not clean_query:
        return []

    # Enforce global turn limit (2 to 4 articles max)
    if len(ctx.deps.recommended_articles) >= MAX_RECOMMENDED_ARTICLES:
        return []

    # 1. Primary search using existing repository method
    articles_qs = ArticleRepository.search(query=clean_query)

    # 2. Fallback: If exact multi-word phrase returned 0, search with individual significant words
    if not articles_qs.exists() and len(clean_query.split()) > 1:
        words = [w for w in clean_query.split() if len(w) > 2]
        if words:
            word_q = Q()
            for word in words:
                word_q |= (
                    Q(title__icontains=word) |
                    Q(summary__icontains=word) |
                    Q(content__icontains=word) |
                    Q(tags__name__icontains=word) |
                    Q(category__name__icontains=word)
                )
            articles_qs = ArticleRepository.get_published().filter(word_q).distinct()

    remaining_slots = MAX_RECOMMENDED_ARTICLES - len(ctx.deps.recommended_articles)
    effective_limit = min(limit, remaining_slots)
    articles = list(articles_qs[:effective_limit])

    result_data: list[dict[str, Any]] = []
    seen_ids = {a.id for a in ctx.deps.recommended_articles}

    for article in articles:
        if len(ctx.deps.recommended_articles) >= MAX_RECOMMENDED_ARTICLES:
            break

        category_name = article.category.name if article.category else 'عمومی'
        author_name = article.author.username if article.author else 'تحریریه دَندی'
        url = article.get_absolute_url()
        cover_url = article.image.url if article.image else None

        item = ArticleItem(
            id=article.id,
            title=article.title,
            slug=article.slug,
            summary=article.summary,
            reading_time=article.reading_time_minutes,
            category_name=category_name,
            author_name=author_name,
            url=url,
            cover_image_url=cover_url,
        )

        if item.id not in seen_ids:
            ctx.deps.recommended_articles.append(item)
            seen_ids.add(item.id)

        result_data.append({
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            'summary': article.summary,
            'reading_time': article.reading_time_minutes,
            'category': category_name,
            'author': author_name,
            'url': url,
            'image_url': cover_url,
        })

    return result_data
