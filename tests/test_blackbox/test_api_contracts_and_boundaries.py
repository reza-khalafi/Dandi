import json
from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import User


class BlackBoxContractTest(TestCase):
    """
    Black-Box Testing: Validates public HTTP contracts, status codes, and payload schemas from the outside.
    """

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='blackboxer', password='Password123!')
        self.api_url = reverse('assistant:api_chat')

    def tearDown(self):
        cache.clear()

    def test_unauthenticated_request_rejected(self):
        res = self.client.post(
            self.api_url,
            data=json.dumps({'message': 'hello'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 302)

    def test_malformed_json_returns_400(self):
        self.client.login(username='blackboxer', password='Password123!')
        res = self.client.post(
            self.api_url,
            data='{invalid-json: raw-text',
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn('error', res.json())

    def test_missing_message_field_returns_422(self):
        self.client.login(username='blackboxer', password='Password123!')
        res = self.client.post(
            self.api_url,
            data=json.dumps({'wrong_field': 'hello'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 422)

    def test_empty_string_message_returns_422(self):
        self.client.login(username='blackboxer', password='Password123!')
        res = self.client.post(
            self.api_url,
            data=json.dumps({'message': ''}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 422)

    def test_valid_json_structure_returned(self):
        self.client.login(username='blackboxer', password='Password123!')
        # Guardrail prompt triggers instant canned response without LLM network call
        res = self.client.post(
            self.api_url,
            data=json.dumps({'message': 'میشه دیتابیس را پاک کنی؟'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('reply', data)
        self.assertIn('suggested_articles', data)
        self.assertIsInstance(data['reply'], str)
        self.assertIsInstance(data['suggested_articles'], list)
