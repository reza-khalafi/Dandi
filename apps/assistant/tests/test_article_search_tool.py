from unittest.mock import MagicMock
from django.test import TestCase
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus
from apps.assistant.agents.context import AssistantContext
from apps.assistant.tools.article_search_tool import search_dandi_articles


class ArticleSearchToolTest(TestCase):
    """
    Test suite for Dandi Assistant article search tool.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testwriter', password='password123')
        self.category = Category.objects.create(name='فناوری و کوانتوم', slug='tech-quantum')
        self.article = Article.objects.create(
            title='رایانش کوانتومی و هوش مصنوعی',
            slug='quantum-computing-ai',
            summary='بررسی جامع مرزهای فیزیک و محاسبات کوانتومی مدرن',
            content='محتوای مفصل درباره کیوبیت و فیزیک کوانتوم...',
            status=ArticleStatus.PUBLISHED,
            category=self.category,
            author=self.user,
            reading_time_minutes=8,
        )

    def test_search_dandi_articles_matches_title(self):
        ctx = AssistantContext(user_id=self.user.id, username=self.user.username)
        mock_run_ctx = MagicMock()
        mock_run_ctx.deps = ctx

        results = search_dandi_articles(mock_run_ctx, query='کوانتوم')

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['slug'], 'quantum-computing-ai')
        self.assertEqual(len(ctx.recommended_articles), 1)
        self.assertEqual(ctx.recommended_articles[0].id, self.article.id)

    def test_search_dandi_articles_empty_query(self):
        ctx = AssistantContext(user_id=self.user.id, username=self.user.username)
        mock_run_ctx = MagicMock()
        mock_run_ctx.deps = ctx

        results = search_dandi_articles(mock_run_ctx, query='')
        self.assertEqual(len(results), 0)
        self.assertEqual(len(ctx.recommended_articles), 0)
