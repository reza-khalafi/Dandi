from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from apps.articles.services.article_service import ArticleService
from apps.comments.services.comment_service import CommentService
from apps.comments.forms.comment_form import CommentForm


class ArticleDetailView(View):
    """
    Renders article full content, metadata, related posts, and interactive comment section.
    """
    template_name = 'articles/detail.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.article_service = ArticleService()
        self.comment_service = CommentService()

    def get(self, request, slug: str):
        article = self.article_service.get_article_detail_and_track_view(slug=slug)
        if not article:
            raise Http404('مقاله مورد نظر یافت نشد یا در حالت پیش‌نویس است.')

        comments = self.comment_service.get_approved_comments_for_article(article_id=article.pk)
        related_articles = self.article_service.get_related_articles(article=article, limit=3)
        comment_form = CommentForm()

        context = {
            'article': article,
            'comments': comments,
            'related_articles': related_articles,
            'comment_form': comment_form,
        }
        return render(request, self.template_name, context)
