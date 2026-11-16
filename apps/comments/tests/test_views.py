from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.articles.models import Category, Article
from apps.comments.models import Comment


class CommentViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='comment_view_user', password='password123')
        self.category = Category.objects.create(name='معماری', slug='architecture')
        self.article = Article.objects.create(
            title='توسعه پایدار',
            slug='sustainable-dev',
            summary='خلاصه',
            content='محتوا',
            category=self.category,
            author=self.user
        )

    def test_create_comment_anonymous_redirects_to_login(self):
        url = reverse('comments:create', kwargs={'article_id': self.article.pk})
        response = self.client.post(url, {'content': 'دیدگاه کاربر مهمان'})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_create_comment_authenticated_success(self):
        self.client.login(username='comment_view_user', password='password123')
        url = reverse('comments:create', kwargs={'article_id': self.article.pk})
        response = self.client.post(url, {'content': 'دیدگاه کاربر لاگین شده'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(author=self.user, article=self.article).exists())

    def test_create_comment_ajax(self):
        self.client.login(username='comment_view_user', password='password123')
        url = reverse('comments:create', kwargs={'article_id': self.article.pk})
        response = self.client.post(
            url,
            {'content': 'دیدگاه ارسال شده از طریق ایجکس', 'is_ajax': '1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('comment_html', data)
