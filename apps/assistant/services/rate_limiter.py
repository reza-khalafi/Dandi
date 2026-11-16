import time
from typing import Tuple
from django.core.cache import cache


class ChatRateLimiter:
    """
    Sliding window rate limiter to protect AI endpoints against DoS, spam, and API exhaustion.
    """
    DEFAULT_MAX_REQUESTS = 10
    DEFAULT_WINDOW_SECONDS = 60

    @classmethod
    def check_rate_limit(
        cls,
        user_id: int,
        max_requests: int = DEFAULT_MAX_REQUESTS,
        window_seconds: int = DEFAULT_WINDOW_SECONDS
    ) -> Tuple[bool, int]:
        """
        Determines whether the user is permitted to send an assistant message.
        Returns: (is_allowed: bool, retry_after: int)
        """
        cache_key = f"assistant_throttle:user_{user_id}"
        now = time.time()
        cutoff = now - window_seconds

        # Retrieve request timestamps from cache
        timestamps: list[float] = cache.get(cache_key, [])

        # Filter out timestamps outside the active window
        valid_timestamps = [t for t in timestamps if t > cutoff]

        if len(valid_timestamps) >= max_requests:
            oldest_request = valid_timestamps[0]
            retry_after = max(1, int(window_seconds - (now - oldest_request)))
            return False, retry_after

        # Record this request
        valid_timestamps.append(now)
        cache.set(cache_key, valid_timestamps, timeout=window_seconds + 10)

        return True, 0
