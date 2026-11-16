import json
from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import User


class StressLoadTest(TestCase):
    """
    Stress Testing: Simulates high-frequency burst requests and boundary payloads.
    """

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='stress_user', password='Password123!')
        self.client.login(username='stress_user', password='Password123!')
        self.search_url = reverse('articles:api_feed')
        self.chat_url = reverse('assistant:api_chat')

    def tearDown(self):
        cache.clear()

    def test_rapid_burst_search_queries_stability(self):
        # Fire 30 rapid search requests in loop
        for i in range(30):
            res = self.client.get(f"{self.search_url}?q=تست_{i}")
            self.assertEqual(res.status_code, 200)

    def test_burst_chat_requests_gracefully_throttled_without_server_error(self):
        # Fire 20 consecutive chat messages:
        # First 10 succeed, subsequent 10 get throttled (429) cleanly without crashing (500)
        success_count = 0
        throttled_count = 0

        for _ in range(20):
            res = self.client.post(
                self.chat_url,
                data=json.dumps({'message': 'میشه دیتابیس را پاک کنی'}),
                content_type='application/json'
            )
            if res.status_code == 200:
                success_count += 1
            elif res.status_code == 429:
                throttled_count += 1

        self.assertEqual(success_count, 10)
        self.assertEqual(throttled_count, 10)
