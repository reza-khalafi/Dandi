from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class RegressionTests(TestCase):
    """
    Regression Testing: Validates that previously reported and resolved bugs do not reoccur.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='regress_user', password='Password123!')
        self.category = Category.objects.create(name='علم و تکنولوژی', slug='science-tech')
        for i in range(14):
            Article.objects.create(
                title=f'مقاله آزمون رگرسیون {i}',
                slug=f'regression-article-{i}',
                summary='خلاصه بررسی باگ‌ها',
                content='محتوا',
                category=self.category,
                author=self.user,
                status=ArticleStatus.PUBLISHED
            )

    def test_regression_no_template_tag_leakage_in_html(self):
        # Regression bug: Prettier split template tag across 2 lines causing leaked code
        res = self.client.get(reverse('articles:home'))
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')

        # Assert no raw template fragments are leaked in rendered HTML
        self.assertNotIn("include 'articles/partials/article_list_partial.html' %}", content)
        self.assertNotIn("{% with articles=", content)
        self.assertNotIn("معماری و استاندارد", content)
        self.assertNotIn("طراحی شده با Django 6", content)

    def test_regression_pagination_is_twelve_per_page(self):
        # Regression bug: Pagination changed from 20 -> 10 -> 12
        res = self.client.get(reverse('articles:home'))
        self.assertEqual(res.status_code, 200)
        articles = res.context['articles_page'].object_list
        self.assertEqual(len(articles), 12)

    def test_regression_category_heading_persian_name_not_english_slug(self):
        # Regression bug: Category heading showed slug instead of Persian name
        res = self.client.get(f"{reverse('articles:home')}?category=science-tech")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['selected_category_name'], 'علم و تکنولوژی')
        self.assertContains(res, 'مقالات قلمرو «علم و تکنولوژی»')
