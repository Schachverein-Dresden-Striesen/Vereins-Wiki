"""HTTP client with exponential backoff, jitter, and circuit breaker."""

import logging
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

LOGGER = logging.getLogger(__name__)

# Retry configuration
RETRY_DELAYS = [30, 120, 300, 900, 1800]  # seconds: 30s, 2m, 5m, 15m, 30m
JITTER_FACTOR = 0.20
MAX_RETRY_AFTER = 2 * 60 * 60  # 2 hours hard cap

# HTTP status codes that trigger a retry
RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}

# Circuit breaker
CIRCUIT_FAILURE_THRESHOLD = 3
CIRCUIT_COOLDOWN_SECONDS = 15 * 60  # 15 minutes


class CircuitOpenError(Exception):
    """Raised when the circuit breaker is open and requests are blocked."""


class MaxRetriesExceededError(Exception):
    """Raised when all retry attempts have been exhausted."""


class CircuitBreaker:
    """Simple circuit breaker: opens after *threshold* consecutive failures."""

    def __init__(
        self,
        failure_threshold: int = CIRCUIT_FAILURE_THRESHOLD,
        cooldown_seconds: float = CIRCUIT_COOLDOWN_SECONDS,
    ) -> None:
        self._threshold = failure_threshold
        self._cooldown = timedelta(seconds=cooldown_seconds)
        self._failures = 0
        self._open_since: Optional[datetime] = None

    @property
    def is_open(self) -> bool:
        if self._open_since is None:
            return False
        if datetime.now(tz=timezone.utc) - self._open_since >= self._cooldown:
            LOGGER.info("Circuit breaker: cooldown elapsed, entering half-open state.")
            return False
        return True

    def record_success(self) -> None:
        self._failures = 0
        self._open_since = None

    def record_failure(self) -> None:
        self._failures += 1
        if self._failures >= self._threshold:
            if self._open_since is None:
                self._open_since = datetime.now(tz=timezone.utc)
                LOGGER.warning(
                    "Circuit breaker OPEN after %d consecutive failures.",
                    self._failures,
                )

    def reset(self) -> None:
        self._failures = 0
        self._open_since = None


def _parse_retry_after(header_value: str) -> Optional[float]:
    """Parse a Retry-After header (seconds or HTTP-date)."""
    try:
        return float(header_value)
    except ValueError:
        pass
    try:
        from email.utils import parsedate_to_datetime

        retry_dt = parsedate_to_datetime(header_value)
        delta = (retry_dt - datetime.now(tz=timezone.utc)).total_seconds()
        return max(0.0, delta)
    except Exception:
        return None


def _jittered_delay(base: float, jitter_factor: float = JITTER_FACTOR) -> float:
    jitter = random.uniform(0, base * jitter_factor)
    return base + jitter


class HttpClient:
    """Requests wrapper with retry + circuit breaker."""

    BASE_URL = "https://www.schachbund.de"

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        retry_delays: list[float] = RETRY_DELAYS,
        circuit_breaker: Optional[CircuitBreaker] = None,
        timeout: float = 30.0,
    ) -> None:
        self._session = session or requests.Session()
        self._retry_delays = retry_delays
        self._cb = circuit_breaker or CircuitBreaker()
        self._timeout = timeout

    def get(self, url: str, **kwargs) -> requests.Response:
        """Perform a GET request with retry and circuit breaker protection."""
        kwargs.setdefault("timeout", self._timeout)
        last_exc: Optional[Exception] = None

        for attempt, delay in enumerate([0.0] + list(self._retry_delays)):
            if self._cb.is_open:
                raise CircuitOpenError(
                    "Circuit breaker is open – DWZ API temporarily unavailable."
                )

            if delay > 0:
                sleep_time = _jittered_delay(delay)
                LOGGER.info(
                    "Retry %d/%d: waiting %.1f s before retrying %s",
                    attempt,
                    len(self._retry_delays),
                    sleep_time,
                    url,
                )
                time.sleep(sleep_time)

            try:
                response = self._session.get(url, **kwargs)
            except requests.exceptions.RequestException as exc:
                LOGGER.warning("Network error on attempt %d: %s", attempt + 1, exc)
                self._cb.record_failure()
                last_exc = exc
                continue

            if response.status_code == 200:
                self._cb.record_success()
                return response

            if response.status_code not in RETRYABLE_STATUS:
                LOGGER.error(
                    "Non-retryable HTTP %d for %s", response.status_code, url
                )
                return response

            # Retryable error
            self._cb.record_failure()
            LOGGER.warning(
                "HTTP %d on attempt %d for %s", response.status_code, url, attempt + 1
            )

            # Honour Retry-After if present
            retry_after_header = response.headers.get("Retry-After")
            if retry_after_header:
                server_delay = _parse_retry_after(retry_after_header)
                if server_delay is not None:
                    if attempt + 1 < len([0.0] + list(self._retry_delays)):
                        # Override next delay in list by sleeping now
                        sleep_time = min(server_delay, MAX_RETRY_AFTER)
                        LOGGER.info(
                            "Honouring Retry-After: sleeping %.1f s", sleep_time
                        )
                        time.sleep(sleep_time)
                        # Skip the normal delay on next iteration
                        self._retry_delays = list(self._retry_delays)
                        if attempt < len(self._retry_delays):
                            self._retry_delays[attempt] = 0

            last_exc = None  # response object available

        if last_exc:
            raise MaxRetriesExceededError(
                f"All retries exhausted for {url}"
            ) from last_exc
        raise MaxRetriesExceededError(f"All retries exhausted for {url}")
