"""
Rate limiting utilities for the feedback agent.
Provides both in-memory and Redis-based rate limiting options.
"""

import time
from datetime import datetime, timedelta
from typing import Optional
import threading
import os

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class InMemoryRateLimiter:
    """In-memory rate limiter using threading locks."""

    def __init__(self, max_calls: int = 2, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
        self.lock = threading.Lock()

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        with self.lock:
            now = datetime.now()
            # Remove calls older than time_window
            self.calls = [call_time for call_time in self.calls
                         if now - call_time < timedelta(seconds=self.time_window)]

            if len(self.calls) >= self.max_calls:
                # Calculate wait time
                oldest_call = min(self.calls)
                wait_time = self.time_window - (now - oldest_call).total_seconds()
                if wait_time > 0:
                    time.sleep(wait_time)
                    # Clean up again after waiting
                    now = datetime.now()
                    self.calls = [call_time for call_time in self.calls
                                 if now - call_time < timedelta(seconds=self.time_window)]

            # Record this call
            self.calls.append(now)


class RedisRateLimiter:
    """Redis-based rate limiter for distributed systems."""

    def __init__(self, max_calls: int = 2, time_window: int = 60,
                 redis_url: Optional[str] = None, key_prefix: str = "feedback_agent"):
        self.max_calls = max_calls
        self.time_window = time_window
        self.key_prefix = key_prefix

        if not REDIS_AVAILABLE:
            raise ImportError("Redis is not available. Install with: pip install redis")

        if redis_url:
            self.redis_client = redis.from_url(redis_url)
        else:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0))
            )

    def wait_if_needed(self, identifier: str = "default"):
        """Wait if rate limit would be exceeded for the given identifier."""
        key = f"{self.key_prefix}:{identifier}"

        while True:
            # Use Redis pipeline for atomic operations
            pipe = self.redis_client.pipeline()
            now = time.time()

            # Remove expired entries
            pipe.zremrangebyscore(key, 0, now - self.time_window)

            # Count current entries
            pipe.zcard(key)

            # Execute pipeline
            results = pipe.execute()
            current_count = results[1]

            if current_count < self.max_calls:
                # Add current timestamp and set expiry
                pipe = self.redis_client.pipeline()
                pipe.zadd(key, {str(now): now})
                pipe.expire(key, self.time_window)
                pipe.execute()
                break
            else:
                # Get the oldest timestamp to calculate wait time
                oldest_entries = self.redis_client.zrange(key, 0, 0, withscores=True)
                if oldest_entries:
                    oldest_time = oldest_entries[0][1]
                    wait_time = self.time_window - (now - oldest_time)
                    if wait_time > 0:
                        time.sleep(min(wait_time, 1))  # Sleep max 1 second at a time
                    else:
                        break


def get_rate_limiter(max_calls: int = 2, time_window: int = 60,
                    use_redis: bool = False, **kwargs) -> InMemoryRateLimiter:
    """
    Factory function to get appropriate rate limiter.

    Args:
        max_calls: Maximum number of calls allowed
        time_window: Time window in seconds
        use_redis: Whether to use Redis-based rate limiter
        **kwargs: Additional arguments for Redis rate limiter

    Returns:
        Rate limiter instance
    """
    if use_redis and REDIS_AVAILABLE:
        return RedisRateLimiter(max_calls, time_window, **kwargs)
    else:
        return InMemoryRateLimiter(max_calls, time_window)