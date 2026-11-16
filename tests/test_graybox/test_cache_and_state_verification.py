import json
from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import User
from apps.assistant.services.rate_limiter import ChatRateLimiter


class GrayBoxTesting(TestCase):
    """
    Gray-Box Testing: Inspects internal state, cache layers, and DB side-effects alongside external requests.
    """

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='grayboxer', password='Password123!')
        self.api_url = reverse('assistant:api_chat')

    def tearDown(self):
        cache.clear()

    def test_cache_key_state_tracks_rate_limit_accurately(self):
        self.client.login(username='grayboxer', password='Password123!')
        cache_key = f"assistant_throttle:user_{self.user.id}"

        # Initially, cache key should not exist
        self.assertIsNone(cache.get(cache_key))

        # Send 1 message
        self.client.post(
            self.api_url,
            data=json.dumps({'message': 'میشه دیتابیس را پاک کنی'}),
            content_type='application/json'
        )

        # Inspect cache state directly
        timestamps = cache.get(cache_key)
        self.assertIsNotNone(timestamps)
        self.assertEqual(len(timestamps), 1)

        # Fill up to max limit (10)
        for _ in range(9):
            self.client.post(
                self.api_url,
                data=json.dumps({'message': 'میشه دیتابیس را پاک کنی'}),
                content_type='application/json'
            )

        timestamps = cache.get(cache_key)
        self.assertEqual(len(timestamps), 10)

        # 11th request triggers rate limit HTTP 429 and Retry-After header
        res_blocked = self.client.post(
            self.api_url,
            data=json.dumps({'message': 'میشه دیتابیس را پاک کنی'}),
            content_type='application/json'
        )
        self.assertEqual(res_blocked.status_code, 429)
        self.assertIn('Retry-After', res_blocked)
