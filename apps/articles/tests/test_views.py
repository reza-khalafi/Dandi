from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.articles.models import Category, Article
from apps.articles.enums import ArticleStatus


class ArticleViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='view_author', password='pwd')
        self.category = Category.objects.create(name='اندیشه', slug='thought')

        self.article = Article.objects.create(
            title='جستاری در باب زمان',
            slug='essay-on-time',
            summary='خلاصه جستار در باب زمان',
            content='محتوای کامل و مفصل جستار در باب زمان برای تست سیستم',
            category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )

    def test_home_view_get(self):
        response = self.client.get(reverse('articles:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/home.html')
        self.assertIn('categories', response.context)
        self.assertIn('articles_page', response.context)

    def test_home_view_with_search(self):
        response = self.client.get(reverse('articles:home') + '?q=زمان')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_query'], 'زمان')

    def test_article_detail_view_success(self):
        response = self.client.get(reverse('articles:detail', kwargs={'slug': 'essay-on-time'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/detail.html')
        self.assertEqual(response.context['article'].pk, self.article.pk)

    def test_article_detail_view_not_found(self):
        response = self.client.get(reverse('articles:detail', kwargs={'slug': 'non-existent-article'}))
        self.assertEqual(response.status_code, 404)

    def test_article_api_feed_json(self):
        response = self.client.get(reverse('articles:api_feed') + '?page=1')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('html', data)
        self.assertIn('has_next', data)
        self.assertIn('total_count', data)
        self.assertEqual(data['total_count'], 1)
