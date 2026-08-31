"""Tests for crawl state persistence."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from dwz_crawler.state import (
    STATUS_DONE,
    STATUS_FAILED,
    STATUS_RETRY_PENDING,
    CrawlState,
    export_partien,
    export_spieler,
    export_turniere,
)
from dwz_crawler.api_client import Partie, Spieler, Turnier


class TestCrawlState:
    def test_new_turnier_is_due(self, tmp_path):
        state = CrawlState(tmp_path / "crawl_state.json")
        assert state.is_due("turnier-abc")

    def test_mark_done_not_due(self, tmp_path):
        state = CrawlState(tmp_path / "crawl_state.json")
        state.mark_done("turnier-abc")
        assert not state.is_due("turnier-abc")

    def test_mark_retry_pending_due_when_time_passed(self, tmp_path):
        state = CrawlState(tmp_path / "crawl_state.json")
        past = datetime.now(tz=timezone.utc) - timedelta(seconds=1)
        state.mark_retry_pending("t1", attempts=1, next_attempt_at=past, last_http_status=503)
        assert state.is_due("t1")

    def test_mark_retry_pending_not_due_yet(self, tmp_path):
        state = CrawlState(tmp_path / "crawl_state.json")
        future = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        state.mark_retry_pending("t1", attempts=1, next_attempt_at=future, last_http_status=503)
        assert not state.is_due("t1")

    def test_mark_failed(self, tmp_path):
        state = CrawlState(tmp_path / "crawl_state.json")
        state.mark_failed("t1", "Network error")
        entry = state.get_turnier_status("t1")
        assert entry["status"] == STATUS_FAILED

    def test_state_persisted_to_disk(self, tmp_path):
        path = tmp_path / "crawl_state.json"
        state = CrawlState(path)
        state.mark_done("t1")
        # Re-load from disk
        state2 = CrawlState(path)
        assert not state2.is_due("t1")

    def test_corrupt_state_file_starts_fresh(self, tmp_path):
        path = tmp_path / "crawl_state.json"
        path.write_text("not valid json", encoding="utf-8")
        state = CrawlState(path)
        assert state.is_due("any-id")


class TestCsvExport:
    def test_export_spieler(self, tmp_path):
        players = [
            Spieler("NU1", "Alice", dwz=1800, verein_id="F2810"),
            Spieler("NU2", "Bob", dwz=1600, verein_id="F2810"),
        ]
        path = export_spieler(players, tmp_path)
        lines = path.read_text(encoding="utf-8").splitlines()
        assert lines[0].startswith("spieler_id")
        assert "Alice" in lines[1]
        assert len(lines) == 3  # header + 2 data rows

    def test_export_turniere(self, tmp_path):
        turniere = [Turnier("t1", "Open Dresden", datum_von="2026-01-01")]
        path = export_turniere(turniere, tmp_path)
        lines = path.read_text(encoding="utf-8").splitlines()
        assert "t1" in lines[1]

    def test_export_partien(self, tmp_path):
        partien = [
            Partie(turnier_id="t1", runde=1, spieler_id="NU1",
                   gegner_id="NU2", farbe="W", ergebnis="1")
        ]
        path = export_partien(partien, tmp_path)
        lines = path.read_text(encoding="utf-8").splitlines()
        assert "NU1" in lines[1]
