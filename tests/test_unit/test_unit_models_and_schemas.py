from django.test import TestCase
from django.contrib.auth.models import User
from pydantic import ValidationError
from apps.articles.models.category import Category
from apps.articles.models.tag import Tag
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus
from apps.assistant.schemas.article_item import ArticleItem
from apps.assistant.schemas.chat_request import ChatRequest
from apps.assistant.schemas.chat_response import ChatResponse


class UnitModelsAndSchemasTest(TestCase):
    """
    Unit Testing: Tests isolated domain models and Pydantic schemas without external dependencies.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='unituser', password='password123')
        self.category = Category.objects.create(name='فلسفه و اندیشه', slug='philosophy')
        self.tag = Tag.objects.create(name='خرد', slug='wisdom')

    def test_article_model_properties_and_methods(self):
        article = Article.objects.create(
            title='هنر تفکر نقادانه',
            slug='art-of-critical-thinking',
            summary='راهنمای تحلیل منطقی و تفکر نقادانه',
            content='متن تفصیلی...',
            category=self.category,
            author=self.user,
            reading_time_minutes=7,
            status=ArticleStatus.PUBLISHED
        )
        article.tags.add(self.tag)

        self.assertEqual(str(article), 'هنر تفکر نقادانه')
        self.assertEqual(article.get_absolute_url(), '/article/art-of-critical-thinking/')
        self.assertEqual(article.views_count, 0)
        self.assertEqual(article.tags.count(), 1)

    def test_article_item_pydantic_schema_validation(self):
        item = ArticleItem(
            id=1,
            title='هوش مصنوعی',
            slug='ai',
            summary='خلاصه',
            reading_time=5,
            category_name='علم',
            author_name='نویسنده',
            url='/article/ai/',
            cover_image_url='/media/cover.jpg'
        )
        self.assertEqual(item.id, 1)
        self.assertEqual(item.title, 'هوش مصنوعی')

        # Invalid item missing required title
        with self.assertRaises(ValidationError):
            ArticleItem(id=2, slug='test')  # type: ignore

    def test_chat_request_schema_validation(self):
        req = ChatRequest(message='سلام دَندی')
        self.assertEqual(req.message, 'سلام دَندی')
        self.assertIsNone(req.conversation_id)

        # Empty message validation
        with self.assertRaises(ValidationError):
            ChatRequest(message='')

        # Exceeding length limit (2000 chars)
        with self.assertRaises(ValidationError):
            ChatRequest(message='a' * 2001)

    def test_chat_response_schema_serialization(self):
        resp = ChatResponse(reply='پاسخ تست', suggested_articles=[])
        data = resp.model_dump()
        self.assertIn('reply', data)
        self.assertEqual(data['reply'], 'پاسخ تست')
        self.assertEqual(data['suggested_articles'], [])
