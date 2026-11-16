import json
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.assistant.schemas.chat_response import ChatResponse
from apps.assistant.schemas.article_item import ArticleItem
from apps.assistant.services.assistant_service import RateLimitExceededException


class AssistantViewsTest(TestCase):
    """
    Test suite for Assistant web page and JSON API views.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='dandiuser', password='password123')
        self.chat_url = reverse('assistant:chat')
        self.api_url = reverse('assistant:api_chat')
        self.new_chat_url = reverse('assistant:api_new_chat')

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_authenticated_user_can_access_chat_page(self):
        self.client.login(username='dandiuser', password='password123')
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/chat.html')
        self.assertIn('sample_prompts', response.context)
        self.assertIn('existing_messages', response.context)

    def test_api_chat_requires_authentication(self):
        response = self.client.post(
            self.api_url,
            data=json.dumps({'message': 'hello'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)

    @patch('apps.assistant.services.assistant_service.AssistantService.process_chat_message')
    def test_api_chat_success_returns_json(self, mock_process):
        self.client.login(username='dandiuser', password='password123')

        mock_process.return_value = ChatResponse(
            reply='این پاسخ تست است.',
            suggested_articles=[
                ArticleItem(
                    id=10,
                    title='تست مقاله',
                    slug='test-article',
                    summary='خلاصه تست',
                    reading_time=5,
                    category_name='فلسفه',
                    author_name='ادمین',
                    url='/articles/test-article/',
                    cover_image_url=None
                )
            ]
        )

        response = self.client.post(
            self.api_url,
            data=json.dumps({'message': 'مقاله تست را معرفی کن'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['reply'], 'این پاسخ تست است.')
        self.assertEqual(len(data['suggested_articles']), 1)
        self.assertEqual(data['suggested_articles'][0]['title'], 'تست مقاله')

    @patch('apps.assistant.services.assistant_service.AssistantService.process_chat_message')
    def test_api_chat_rate_limit_returns_429(self, mock_process):
        self.client.login(username='dandiuser', password='password123')
        mock_process.side_effect = RateLimitExceededException(retry_after=45)

        response = self.client.post(
            self.api_url,
            data=json.dumps({'message': 'اسپم'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 429)
        self.assertEqual(response['Retry-After'], '45')
        self.assertIn('سقف مصرف مجاز', response.json()['error'])

    def test_api_new_chat_creates_new_session(self):
        self.client.login(username='dandiuser', password='password123')
        response = self.client.post(self.new_chat_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('conversation_id', data)
