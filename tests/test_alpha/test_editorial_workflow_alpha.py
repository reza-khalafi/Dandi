from django.test import TestCase
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.tag import Tag
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus
from apps.assistant.agents.context import AssistantContext
from apps.assistant.tools.article_search_tool import search_dandi_articles
from unittest.mock import MagicMock


class AlphaEditorialWorkflowTest(TestCase):
    """
    Alpha Testing: Simulates internal editorial team acceptance criteria and content publishing workflows.
    """

    def setUp(self):
        self.editor = User.objects.create_user(username='editor_alpha', password='Password123!', is_staff=True)
        self.category = Category.objects.create(name='فلسفه علم', slug='philosophy-of-science')
        self.tag_ai = Tag.objects.create(name='هوش مصنوعی', slug='ai')
        self.tag_ethics = Tag.objects.create(name='اخلاق زیستی', slug='bioethics')

    def test_editorial_publishing_immediately_available_in_search_and_ai(self):
        # 1. Editor authors and publishes a new scholarly article
        new_article = Article.objects.create(
            title='تبارشناسی اخلاق در عصر ماشین‌های هوشمند',
            slug='genealogy-of-ethics-in-smart-machines',
            summary='بررسی رویکردهای کانت و فایده‌گرایی در کدگذاری هوش مصنوعی',
            content='محتوای مفصل فلسفی و اخلاقی در زمینه هوش مصنوعی...',
            category=self.category,
            author=self.editor,
            reading_time_minutes=12,
            status=ArticleStatus.PUBLISHED,
            is_featured=True
        )
        new_article.tags.add(self.tag_ai, self.tag_ethics)

        # 2. Verify publication in Dandi featured repository
        from apps.articles.repositories.article_repository import ArticleRepository
        featured_articles = ArticleRepository.get_featured(limit=5)
        self.assertIn(new_article, featured_articles)

        # 3. Verify immediate discoverability by Dandi AI Assistant tool
        ctx = AssistantContext(user_id=self.editor.id, username=self.editor.username)
        mock_run_ctx = MagicMock()
        mock_run_ctx.deps = ctx

        results = search_dandi_articles(mock_run_ctx, query='اخلاق ماشین‌های هوشمند')
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['id'], new_article.id)
        self.assertIn('genealogy-of-ethics-in-smart-machines', results[0]['url'])
