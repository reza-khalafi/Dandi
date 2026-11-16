from django.test import TestCase
from django.contrib.auth.models import User
from apps.articles.models import Category, Article
from apps.articles.enums import ArticleStatus
from apps.articles.services import ArticleService, CategoryService


class ArticleServiceTests(TestCase):
    def setUp(self):
        self.article_service = ArticleService()
        self.category_service = CategoryService()

        self.user = User.objects.create_user(username='srv_author', password='pwd')
        self.category = Category.objects.create(name='هوش مصنوعی', slug='ai')

        self.article = Article.objects.create(
            title='مبانی شبکه عصبی',
            slug='neural-networks-basics',
            summary='خلاصه مبانی',
            content='متن شبکه های عصبی',
            category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )

    def test_category_service(self):
        cats = self.category_service.get_active_categories()
        self.assertEqual(cats.count(), 1)
        found = self.category_service.get_category_by_slug('ai')
        self.assertIsNotNone(found)

    def test_article_service_pagination(self):
        page_obj, total = self.article_service.get_articles_page(page=1, per_page=5)
        self.assertEqual(total, 1)
        self.assertEqual(len(page_obj.object_list), 1)

    def test_article_service_detail_and_track_view(self):
        initial_views = self.article.views_count
        art = self.article_service.get_article_detail_and_track_view('neural-networks-basics')
        self.assertIsNotNone(art)
        self.assertEqual(art.views_count, initial_views + 1)
