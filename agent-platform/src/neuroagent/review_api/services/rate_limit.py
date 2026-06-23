"""In-process throttle for failed authentication attempts.

The reviewer code is a bearer secret reachable over a public tunnel, so we
slow down brute-force guessing: after too many failed attempts from one client
within a window, that client is locked out for a cooldown period and gets 429s.

Keyed on the real client IP — behind Cloudflare we honour ``CF-Connecting-IP``
/ ``X-Forwarded-For`` (the direct ``request.client`` is just the tunnel).
State is per-process and in-memory, which is sufficient for the single-uvicorn
Raspberry-Pi deployment; pair with a Cloudflare WAF rule for defence in depth.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict

from fastapi import Request


class AuthRateLimiter:
    def __init__(
        self,
        max_failures: int = 10,
        window_seconds: float = 300.0,
        lockout_seconds: float = 900.0,
    ) -> None:
        self._max_failures = max_failures
        self._window = window_seconds
        self._lockout = lockout_seconds
        self._failures: dict[str, list[float]] = defaultdict(list)
        self._locked_until: dict[str, float] = {}
        self._lock = threading.Lock()

    @staticmethod
    def client_key(request: Request) -> str:
        """Best-effort real client identity, Cloudflare-aware."""
        cf = request.headers.get("cf-connecting-ip")
        if cf:
            return cf.strip()
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def retry_after(self, key: str) -> int | None:
        """Seconds remaining on a lockout, or None if not locked."""
        with self._lock:
            until = self._locked_until.get(key)
            if until is None:
                return None
            remaining = until - time.monotonic()
            if remaining <= 0:
                self._locked_until.pop(key, None)
                return None
            return int(remaining) + 1

    def record_failure(self, key: str) -> None:
        now = time.monotonic()
        with self._lock:
            hits = [t for t in self._failures[key] if now - t < self._window]
            hits.append(now)
            self._failures[key] = hits
            if len(hits) >= self._max_failures:
                self._locked_until[key] = now + self._lockout
                self._failures[key] = []

    def record_success(self, key: str) -> None:
        with self._lock:
            self._failures.pop(key, None)
            self._locked_until.pop(key, None)
