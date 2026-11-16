from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.articles.models.category import Category
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class SystemEndToEndTest(TestCase):
    """
    System Testing: Validates the complete system workflow as experienced by end users.
    """

    def setUp(self):
        self.category = Category.objects.create(name='اندیشه و علم', slug='science-thought')
        self.author = User.objects.create_user(username='author1', password='Password123!')
        self.article = Article.objects.create(
            title='کاوش در سامانه‌های هوشمند',
            slug='exploring-smart-systems',
            summary='چکیده مقاله سامانه‌ها',
            content='متن تفصیلی در ساحت مهندسی و اندیشه...',
            category=self.category,
            author=self.author,
            reading_time_minutes=6,
            status=ArticleStatus.PUBLISHED,
            is_featured=True
        )

    def test_complete_user_lifecycle(self):
        # Step 1: Guest visits homepage
        home_res = self.client.get(reverse('articles:home'))
        self.assertEqual(home_res.status_code, 200)
        self.assertContains(home_res, 'دَندی')
        self.assertContains(home_res, 'کاوش در سامانه‌های هوشمند')

        # Step 2: Guest reads article detail
        detail_res = self.client.get(reverse('articles:detail', kwargs={'slug': self.article.slug}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, 'کاوش در سامانه‌های هوشمند')

        # Step 3: Register a new account
        register_url = reverse('accounts:register')
        reg_data = {
            'username': 'newreader',
            'email': 'reader@dandi.ir',
            'password': 'ComplexPassword123!',
            'password_confirm': 'ComplexPassword123!'
        }
        reg_res = self.client.post(register_url, data=reg_data)
        # Should redirect after successful registration
        self.assertEqual(reg_res.status_code, 302)

        # Step 4: Logout and Login to test authentication flow
        self.client.logout()
        login_url = reverse('accounts:login')
        login_res = self.client.post(login_url, data={
            'username': 'newreader',
            'password': 'ComplexPassword123!'
        })
        self.assertEqual(login_res.status_code, 302)

        # Step 5: Access Assistant Chat & Guide as authenticated user
        chat_res = self.client.get(reverse('assistant:chat'))
        self.assertEqual(chat_res.status_code, 200)
        self.assertContains(chat_res, 'دستیار هوشمند دَندی')

        guide_res = self.client.get(reverse('assistant:guide'))
        self.assertEqual(guide_res.status_code, 200)
        self.assertContains(guide_res, 'راهنمای جامع دستیار هوشمند دَندی')
