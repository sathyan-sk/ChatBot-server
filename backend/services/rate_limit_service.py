from __future__ import annotations

from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta


class RateLimitService:
    """Simple in-memory rate limiter for Phase 9.

    Suitable for single-process development and basic protection.
    In production multi-instance deployment, replace with Redis-backed storage
    without changing route or business-layer contracts.
    """

    def __init__(self) -> None:
        self._buckets: dict[str, deque[datetime]] = defaultdict(deque)

    def check(self, key: str, limit: int, window_seconds: int = 60) -> bool:
        now = datetime.now(UTC)
        bucket = self._buckets[key]
        cutoff = now - timedelta(seconds=window_seconds)

        while bucket and bucket[0] < cutoff:
            bucket.popleft()

        if len(bucket) >= limit:
            return False

        bucket.append(now)
        return True
