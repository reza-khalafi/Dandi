from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from apps.articles.repositories.article_repository import ArticleRepository
from apps.comments.forms.comment_form import CommentForm
from apps.comments.services.comment_service import CommentService


class CreateCommentView(LoginRequiredMixin, View):
    """
    Handles creating comments for articles. Requires authentication.
    """
    login_url = 'accounts:login'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comment_service = CommentService()
        self.article_repo = ArticleRepository()

    def post(self, request, article_id: int):
        article = get_object_or_404(self.article_repo.get_published(), pk=article_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            parent_id = request.POST.get('parent_id')
            parent_id = int(parent_id) if parent_id and parent_id.isdigit() else None

            comment = self.comment_service.add_comment(
                article=article,
                author=request.user,
                content=content,
                parent_id=parent_id
            )

            # Support AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('is_ajax') == '1':
                comment_html = render_to_string(
                    'articles/partials/comment_item_partial.html',
                    {'comment': comment},
                    request=request
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'دیدگاه شما با موفقیت ثبت شد.',
                    'comment_html': comment_html
                })

            messages.success(request, 'دیدگاه شما با موفقیت ثبت شد.')
            return redirect('articles:detail', slug=article.slug)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('is_ajax') == '1':
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        messages.error(request, 'خطایی در ثبت دیدگاه رخ داد. لطفاً متن دیدگاه را بررسی کنید.')
        return redirect('articles:detail', slug=article.slug)
