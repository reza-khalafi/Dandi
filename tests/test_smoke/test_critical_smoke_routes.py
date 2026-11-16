from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class SmokeTests(TestCase):
    """
    Smoke Testing: Rapid sanity checks ensuring critical routes load with HTTP 200 without fatal crashes.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='smoke_user', password='Password123!')
        self.category = Category.objects.create(name='عمومی', slug='general')
        self.article = Article.objects.create(
            title='مقاله اسموک تست',
            slug='smoke-test-article',
            summary='خلاصه',
            content='محتوا',
            category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )

    def test_smoke_public_routes_healthy(self):
        routes = [
            reverse('articles:home'),
            reverse('articles:detail', kwargs={'slug': self.article.slug}),
            reverse('accounts:login'),
            reverse('accounts:register'),
        ]
        for route in routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Smoke test failed on public route: {route}")

    def test_smoke_authenticated_routes_healthy(self):
        self.client.login(username='smoke_user', password='Password123!')
        auth_routes = [
            reverse('assistant:chat'),
            reverse('assistant:guide'),
        ]
        for route in auth_routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Smoke test failed on auth route: {route}")
