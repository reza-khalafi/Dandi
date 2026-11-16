from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from apps.articles.services.article_service import ArticleService


class ArticleSearchView(View):
    """
    API endpoint powering infinite scroll and asynchronous live article search.
    Returns rendered HTML snippets and pagination state.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.article_service = ArticleService()

    def get(self, request):
        query = request.GET.get('q', '').strip()
        category_slug = request.GET.get('category', '').strip()
        page = request.GET.get('page', 1)

        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1

        articles_page, total_count = self.article_service.get_articles_page(
            query=query,
            category_slug=category_slug,
            page=page,
            per_page=6
        )

        rendered_html = render_to_string(
            'articles/partials/article_list_partial.html',
            {'articles': articles_page.object_list},
            request=request
        )

        return JsonResponse({
            'html': rendered_html,
            'has_next': articles_page.has_next(),
            'next_page_number': articles_page.next_page_number() if articles_page.has_next() else None,
            'current_page': articles_page.number,
            'total_pages': articles_page.paginator.num_pages,
            'total_count': total_count,
        })
