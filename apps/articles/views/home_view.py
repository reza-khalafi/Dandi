from django.views import View
from django.shortcuts import render
from apps.articles.services.article_service import ArticleService
from apps.articles.services.category_service import CategoryService


class HomeView(View):
    """
    Renders the Dandi homepage with hero section, live search, categories, and articles feed.
    """
    template_name = 'articles/home.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.article_service = ArticleService()
        self.category_service = CategoryService()

    def get(self, request):
        query = request.GET.get('q', '').strip()
        category_slug = request.GET.get('category', '').strip()
        page = request.GET.get('page', 1)

        categories = self.category_service.get_categories_with_counts()
        articles_page, total_count = self.article_service.get_articles_page(
            query=query,
            category_slug=category_slug,
            page=page,
            per_page=10
        )
        featured_articles = self.article_service.get_featured_articles(limit=3)

        paginator = articles_page.paginator
        try:
            elided_page_range = paginator.get_elided_page_range(
                number=articles_page.number,
                on_each_side=2,
                on_ends=1
            )
        except Exception:
            elided_page_range = paginator.page_range

        context = {
            'categories': categories,
            'articles_page': articles_page,
            'elided_page_range': elided_page_range,
            'featured_articles': featured_articles,
            'selected_category': category_slug,
            'search_query': query,
            'total_count': total_count,
        }
        return render(request, self.template_name, context)
