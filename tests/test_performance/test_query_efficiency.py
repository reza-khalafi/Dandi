from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class PerformanceQueryEfficiencyTest(TestCase):
    """
    Performance Testing: Asserts database query counts (no N+1 queries) and selects related models.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='perf_user', password='Password123!')
        self.category = Category.objects.create(name='فناوری', slug='tech')

        # Create 12 articles
        for i in range(12):
            Article.objects.create(
                title=f'مقاله عملکردی {i}',
                slug=f'perf-article-{i}',
                summary='خلاصه',
                content='متن',
                category=self.category,
                author=self.user,
                status=ArticleStatus.PUBLISHED
            )

    def test_homepage_database_query_budget(self):
        # Homepage renders categories, featured articles, and 12-item feed with select_related & prefetch_related
        # Query count should remain low and constant regardless of article count (strictly no N+1):
        # 1. Count published articles
        # 2. Categories with article counts
        # 3. Featured articles (select_related category & author)
        # 4. Paginated articles feed (select_related category & author)
        # 5. Prefetched tags
        with self.assertNumQueries(5):
            res = self.client.get(reverse('articles:home'))
            self.assertEqual(res.status_code, 200)

    def test_article_detail_database_query_budget(self):
        article = Article.objects.first()
        # Query budget for full article detail (strictly bounded and no N+1):
        # 1. Fetch article with category & author
        # 2. Prefetch article tags
        # 3. Increment views_count
        # 4. Comments count
        # 5. Comments list with author select_related
        # 6. Related articles (3 items) with category & author
        # 7. Prefetch related articles tags
        with self.assertNumQueries(7):
            res = self.client.get(reverse('articles:detail', kwargs={'slug': article.slug}))
            self.assertEqual(res.status_code, 200)
