from django.test import TestCase
from django.core.cache import cache
from apps.assistant.services.rate_limiter import ChatRateLimiter


class ChatRateLimiterTest(TestCase):
    """
    Test suite for ChatRateLimiter sliding window mechanism.
    """

    def setUp(self):
        cache.clear()

    def test_rate_limiter_permits_under_limit(self):
        user_id = 999
        for _ in range(5):
            allowed, retry_after = ChatRateLimiter.check_rate_limit(user_id, max_requests=10, window_seconds=60)
            self.assertTrue(allowed)
            self.assertEqual(retry_after, 0)

    def test_rate_limiter_blocks_when_limit_exceeded(self):
        user_id = 888
        for _ in range(3):
            allowed, _ = ChatRateLimiter.check_rate_limit(user_id, max_requests=3, window_seconds=60)
            self.assertTrue(allowed)

        # 4th request must be blocked
        allowed, retry_after = ChatRateLimiter.check_rate_limit(user_id, max_requests=3, window_seconds=60)
        self.assertFalse(allowed)
        self.assertGreater(retry_after, 0)
