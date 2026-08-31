"""Tests for dwz_crawler HTTP client (retry + circuit breaker)."""

import time
from unittest.mock import MagicMock, patch

import pytest
import requests

from dwz_crawler.http_client import (
    RETRYABLE_STATUS,
    CircuitBreaker,
    CircuitOpenError,
    HttpClient,
    MaxRetriesExceededError,
    _jittered_delay,
    _parse_retry_after,
)


# ---------------------------------------------------------------------------
# CircuitBreaker
# ---------------------------------------------------------------------------


class TestCircuitBreaker:
    def test_initially_closed(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=60)
        assert not cb.is_open

    def test_opens_after_threshold(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=3600)
        for _ in range(3):
            cb.record_failure()
        assert cb.is_open

    def test_does_not_open_before_threshold(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=3600)
        cb.record_failure()
        cb.record_failure()
        assert not cb.is_open

    def test_closes_after_cooldown(self):
        cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=0)
        cb.record_failure()
        # cooldown is 0 seconds → should be closed immediately
        assert not cb.is_open

    def test_reset_closes_circuit(self):
        cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=3600)
        cb.record_failure()
        assert cb.is_open
        cb.reset()
        assert not cb.is_open

    def test_success_resets_failures(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=3600)
        cb.record_failure()
        cb.record_failure()
        cb.record_success()
        cb.record_failure()
        # Only 1 failure after the reset — should stay closed
        assert not cb.is_open


# ---------------------------------------------------------------------------
# _parse_retry_after
# ---------------------------------------------------------------------------


class TestParseRetryAfter:
    def test_numeric_seconds(self):
        assert _parse_retry_after("120") == 120.0

    def test_float_seconds(self):
        assert _parse_retry_after("45.5") == 45.5

    def test_invalid_returns_none(self):
        assert _parse_retry_after("not-a-date-or-number") is None


# ---------------------------------------------------------------------------
# _jittered_delay
# ---------------------------------------------------------------------------


class TestJitteredDelay:
    def test_delay_within_bounds(self):
        for _ in range(50):
            d = _jittered_delay(30.0)
            assert 30.0 <= d <= 30.0 * 1.20 + 0.001

    def test_zero_base(self):
        assert _jittered_delay(0.0) == 0.0


# ---------------------------------------------------------------------------
# HttpClient
# ---------------------------------------------------------------------------


def _mock_response(status_code: int, headers: dict | None = None) -> MagicMock:
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.headers = headers or {}
    return resp


class TestHttpClient:
    def _make_client(self, responses: list, delays: list | None = None):
        """Build an HttpClient whose session.get returns *responses* in sequence.

        The circuit breaker threshold is set very high so it never interferes
        with retry-exhaustion tests; circuit-breaker behaviour is covered by
        dedicated TestCircuitBreaker tests.
        """
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = responses
        cb = CircuitBreaker(failure_threshold=1000, cooldown_seconds=3600)
        return HttpClient(
            session=session,
            retry_delays=delays if delays is not None else [0, 0, 0, 0, 0],
            circuit_breaker=cb,
            timeout=5,
        )

    def test_success_on_first_attempt(self):
        client = self._make_client([_mock_response(200)])
        resp = client.get("http://example.com")
        assert resp.status_code == 200

    def test_retries_on_503_then_succeeds(self):
        client = self._make_client(
            [_mock_response(503), _mock_response(503), _mock_response(200)]
        )
        resp = client.get("http://example.com")
        assert resp.status_code == 200
        assert client._session.get.call_count == 3

    def test_raises_after_all_retries_exhausted(self):
        responses = [_mock_response(503)] * 6  # initial + 5 retries
        client = self._make_client(responses)
        with pytest.raises(MaxRetriesExceededError):
            client.get("http://example.com")

    def test_no_retry_on_404(self):
        client = self._make_client([_mock_response(404)])
        resp = client.get("http://example.com")
        assert resp.status_code == 404
        assert client._session.get.call_count == 1

    def test_circuit_breaker_blocks_after_threshold(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=3600)
        # Fill circuit breaker to the threshold
        for _ in range(3):
            cb.record_failure()

        session = MagicMock(spec=requests.Session)
        client = HttpClient(session=session, retry_delays=[0, 0], circuit_breaker=cb)

        with pytest.raises(CircuitOpenError):
            client.get("http://example.com")

        # Session should never have been called
        session.get.assert_not_called()

    def test_network_error_triggers_retry(self):
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = [
            requests.exceptions.ConnectionError("timeout"),
            _mock_response(200),
        ]
        client = HttpClient(session=session, retry_delays=[0, 0, 0], timeout=5)
        resp = client.get("http://example.com")
        assert resp.status_code == 200

    def test_all_retryable_codes_trigger_retry(self):
        for code in RETRYABLE_STATUS:
            session = MagicMock(spec=requests.Session)
            session.get.side_effect = [_mock_response(code), _mock_response(200)]
            client = HttpClient(session=session, retry_delays=[0, 0, 0], timeout=5)
            resp = client.get("http://example.com")
            assert resp.status_code == 200, f"Expected retry for {code}"
