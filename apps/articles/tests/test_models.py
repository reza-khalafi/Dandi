from django.test import TestCase
from django.contrib.auth.models import User
from apps.articles.models import Category, Tag, Article
from apps.articles.enums import ArticleStatus


class ArticleModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author1', password='pass')
        self.category = Category.objects.create(
            name='فناوری',
            slug='tech',
            description='درباره فناوری'
        )
        self.tag = Tag.objects.create(name='وب', slug='web')

    def test_category_creation_and_str(self):
        self.assertEqual(str(self.category), 'فناوری')
        self.assertTrue(self.category.is_active)

    def test_tag_creation_and_str(self):
        self.assertEqual(str(self.tag), '#وب')

    def test_article_creation_and_defaults(self):
        article = Article.objects.create(
            title='مقاله اول',
            slug='first-article',
            summary='خلاصه مقاله اول',
            content='متن کامل مقاله اول برای تست سیستم',
            category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )
        article.tags.add(self.tag)

        self.assertEqual(str(article), 'مقاله اول')
        self.assertEqual(article.views_count, 0)
        self.assertEqual(article.reading_time_minutes, 3)
        self.assertEqual(article.tags.count(), 1)
