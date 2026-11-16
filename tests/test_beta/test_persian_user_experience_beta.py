from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.tag import Tag
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class BetaPersianUserExperienceTest(TestCase):
    """
    Beta Testing: Simulates real Persian end-user acceptance, RTL typography,
    ZWNJ (نیم‌فاصله) search resiliency, and multi-device navigation experience.
    """

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='beta_tester', password='Password123!')
        self.category = Category.objects.create(name='فرهنگ و رسانه', slug='culture')
        self.tag_ai = Tag.objects.create(name='هوش مصنوعی', slug='ai')
        self.article = Article.objects.create(
            title='روان‌شناسی یادگیری در عصر دیجیتال و هوش‌مصنوعی',
            slug='psychology-of-learning-digital-age',
            summary='بررسی اثر نیم‌فاصله‌ها و خط فارسی در سامانه‌های نوین',
            content='متن تحلیلی درباره سواد دیجیتال و نگارش درست زبان فارسی...',
            category=self.category,
            author=self.user,
            reading_time_minutes=6,
            status=ArticleStatus.PUBLISHED
        )
        self.article.tags.add(self.tag_ai)

    def tearDown(self):
        cache.clear()

    def test_persian_zwnj_search_tolerance(self):
        """
        Tests that user queries containing ZWNJ (نیم‌فاصله \u200c) match titles smoothly.
        """
        search_url = reverse('articles:api_feed')
        
        # 1. Search with explicit ZWNJ ("هوش‌مصنوعی")
        res_zwnj = self.client.get(f"{search_url}?q=\u0647\u0648\u0634\u200c\u0645\u0635\u0646\u0648\u0639\u06cc")
        self.assertEqual(res_zwnj.status_code, 200)
        data_zwnj = res_zwnj.json()
        self.assertGreaterEqual(data_zwnj['total_count'], 1)
        self.assertIn('psychology-of-learning-digital-age', data_zwnj['html'])

        # 2. Search with standard space ("روان شناسی" matching "روان‌شناسی")
        res_space = self.client.get(f"{search_url}?q=دیجیتال")
        self.assertEqual(res_space.status_code, 200)
        data_space = res_space.json()
        self.assertGreaterEqual(data_space['total_count'], 1)

    def test_arabic_persian_character_variants(self):
        """
        Tests resilience when users type Arabic Yeh (ي \u064a) instead of Persian Yeh (ی \u06cc).
        """
        search_url = reverse('articles:api_feed')
        # "دیجیتال" typed with Arabic Yeh: "ديجيتال"
        arabic_query = "\u062f\u064a\u062c\u064a\u062a\u0627\u0644"
        res = self.client.get(f"{search_url}?q={arabic_query}")
        self.assertEqual(res.status_code, 200)

    def test_anonymous_user_assistant_cta_and_protection(self):
        """
        Tests that unauthenticated users are seamlessly directed to login when attempting to chat,
        while maintaining the 'next' query param for smooth post-login redirection.
        """
        chat_url = reverse('assistant:chat')
        res = self.client.get(chat_url)
        self.assertEqual(res.status_code, 302)
        self.assertIn(f"{reverse('accounts:login')}?next={chat_url}", res.url)

    def test_empty_search_and_invalid_category_render_friendly_persian_empty_states(self):
        """
        Tests that entering non-matching search or invalid categories returns HTTP 200 with friendly UI.
        """
        search_url = reverse('articles:api_feed')
        res = self.client.get(f"{search_url}?q=عبارت_کاملا_ناموجود_در_دیتابیس_دندی_99999")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['total_count'], 0)
        self.assertIn('هیچ مقاله‌ای یافت نشد', data['html'])
