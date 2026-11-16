from django.test import TestCase
from django.contrib.auth.models import User
from apps.articles.models import Category, Tag, Article
from apps.articles.enums import ArticleStatus
from apps.articles.repositories import CategoryRepository, TagRepository, ArticleRepository


class ArticleRepositoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='repo_author', password='pwd')
        self.category = Category.objects.create(name='برنامه‌نویسی', slug='programming')
        self.tag = Tag.objects.create(name='جنگو', slug='django')

        self.article_pub = Article.objects.create(
            title='آموزش جامع جنگو',
            slug='django-guide',
            summary='خلاصه آموزش',
            content='محتوای مفصل درباره فریم‌ورک پایتونی جنگو',
            category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )
        self.article_pub.tags.add(self.tag)

        self.article_draft = Article.objects.create(
            title='مقاله پیش‌نویس',
            slug='draft-article',
            summary='خلاصه پیش نویس',
            content='متن پیش نویس',
            category=self.category,
            author=self.user,
            status=ArticleStatus.DRAFT
        )

    def test_category_repository(self):
        cats = CategoryRepository.get_all_active()
        self.assertEqual(cats.count(), 1)

        counts = CategoryRepository.get_with_published_counts()
        self.assertEqual(counts[0].published_articles_count, 1)

        found = CategoryRepository.get_by_slug('programming')
        self.assertIsNotNone(found)
        self.assertEqual(found.pk, self.category.pk)

    def test_tag_repository(self):
        tag = TagRepository.get_or_create(name='پایتون', slug='python')
        self.assertEqual(tag.name, 'پایتون')
        found_tag = TagRepository.get_by_slug('django')
        self.assertEqual(found_tag.pk, self.tag.pk)

    def test_article_repository_published_only(self):
        published = ArticleRepository.get_published()
        self.assertEqual(published.count(), 1)
        self.assertEqual(published.first().pk, self.article_pub.pk)

    def test_article_repository_search(self):
        # Search by title keyword
        results = ArticleRepository.search(query='جنگو')
        self.assertEqual(results.count(), 1)

        # Search by tag
        results_tag = ArticleRepository.search(query='جنگو')
        self.assertEqual(results_tag.count(), 1)

        # Search non-matching query
        results_none = ArticleRepository.search(query='جاوااسکریپت')
        self.assertEqual(results_none.count(), 0)

    def test_article_repository_increment_views(self):
        ArticleRepository.increment_views(self.article_pub.pk)
        self.article_pub.refresh_from_db()
        self.assertEqual(self.article_pub.views_count, 1)
