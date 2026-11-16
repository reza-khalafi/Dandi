from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class FunctionalBusinessFeaturesTest(TestCase):
    """
    Functional Testing: Validates specific business features (12-item pagination, search, category filter).
    """

    def setUp(self):
        self.user = User.objects.create_user(username='func_author', password='Password123!')
        self.cat_tech = Category.objects.create(name='علم و فناوری', slug='tech')
        self.cat_art = Category.objects.create(name='هنر و معماری', slug='art')

        # Create 15 published articles
        for i in range(15):
            cat = self.cat_tech if i < 10 else self.cat_art
            Article.objects.create(
                title=f'جستار تخصصی دَندی شماره {i + 1}',
                slug=f'dandi-essay-{i + 1}',
                summary=f'چکیده کوتاه برای جستار شماره {i + 1}',
                content=f'متن کامل جستار {i + 1}',
                category=cat,
                author=self.user,
                reading_time_minutes=4 + (i % 5),
                status=ArticleStatus.PUBLISHED
            )

    def test_homepage_pagination_strictly_twelve_items(self):
        home_res = self.client.get(reverse('articles:home'))
        self.assertEqual(home_res.status_code, 200)

        # Ensure paginator pageSize is 12
        articles_page = home_res.context['articles_page']
        self.assertEqual(len(articles_page.object_list), 12)
        self.assertTrue(articles_page.has_next())

        # Page 2 has the remaining 3 articles
        page2_res = self.client.get(f"{reverse('articles:home')}?page=2")
        self.assertEqual(page2_res.status_code, 200)
        p2_articles = page2_res.context['articles_page']
        self.assertEqual(len(p2_articles.object_list), 3)

    def test_category_filtering_and_persian_heading(self):
        res = self.client.get(f"{reverse('articles:home')}?category=tech")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['selected_category_name'], 'علم و فناوری')
        self.assertEqual(res.context['total_count'], 10)

    def test_live_search_endpoint(self):
        api_feed_url = reverse('articles:api_feed')
        res = self.client.get(f"{api_feed_url}?q=شماره 1")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('html', data)
        self.assertIn('total_count', data)
