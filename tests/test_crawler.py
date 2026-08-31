"""Integration test for DwzCrawler – no network, uses HTML fixtures."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

from dwz_crawler.api_client import DwzApiClient, _parse_spieler_turniere, _parse_turnier_partien
from dwz_crawler.crawler import DwzCrawler
from dwz_crawler.state import CrawlState

FIXTURE_DIR = Path(__file__).parent / "fixtures"

SPIELER_ID = "NU4241593"
TURNIER_ID = (
    "434ecfd3-821d-410a-9d9f-d4ea01872f90/"
    "79824ba5-3fa2-48ca-8a2d-f9be68e55809"
)


def _mock_http_for_spieler(turnier_index: int = 0):
    """Return a DwzApiClient whose HTTP calls are replaced by fixture reads."""
    spieler_html = (FIXTURE_DIR / "spieler_NU4241593.html").read_text(encoding="utf-8")
    partien_html = (FIXTURE_DIR / "turnier_partien.html").read_text(encoding="utf-8")

    def fake_get(url, **kwargs):
        resp = MagicMock(spec=requests.Response)
        resp.status_code = 200
        if "/dwz-spieler/" in url:
            resp.text = spieler_html
        elif "/dwz-turniere/" in url:
            resp.text = partien_html
        else:
            resp.text = "<html></html>"
        resp.raise_for_status = lambda: None
        return resp

    http = MagicMock()
    http.get.side_effect = fake_get
    return DwzApiClient(http_client=http)


class TestDwzCrawlerRun:
    def test_csv_files_created(self, tmp_path):
        client = _mock_http_for_spieler()
        crawler = DwzCrawler(
            spieler_id=SPIELER_ID,
            output_dir=tmp_path,
            api_client=client,
            state=CrawlState(tmp_path / "crawl_state.json"),
        )
        crawler.run()

        assert (tmp_path / "players.csv").exists()
        assert (tmp_path / "tournaments.csv").exists()
        assert (tmp_path / "games.csv").exists()

    def test_games_csv_has_three_rows(self, tmp_path):
        client = _mock_http_for_spieler()
        crawler = DwzCrawler(
            spieler_id=SPIELER_ID,
            output_dir=tmp_path,
            api_client=client,
            state=CrawlState(tmp_path / "crawl_state.json"),
        )
        crawler.run()

        lines = (tmp_path / "games.csv").read_text(encoding="utf-8").splitlines()
        assert len(lines) == 4  # header + 3 games

    def test_tournaments_csv_has_one_row(self, tmp_path):
        client = _mock_http_for_spieler()
        crawler = DwzCrawler(
            spieler_id=SPIELER_ID,
            output_dir=tmp_path,
            api_client=client,
            state=CrawlState(tmp_path / "crawl_state.json"),
        )
        crawler.run()

        lines = (tmp_path / "tournaments.csv").read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2  # header + 1 tournament

    def test_second_run_skips_crawled_tournament(self, tmp_path):
        client = _mock_http_for_spieler()
        state = CrawlState(tmp_path / "crawl_state.json")
        crawler = DwzCrawler(
            spieler_id=SPIELER_ID,
            output_dir=tmp_path,
            api_client=client,
            state=state,
        )
        crawler.run()

        first_call_count = client._http.get.call_count

        # Second run: tournament is already done → games endpoint not called again
        crawler2 = DwzCrawler(
            spieler_id=SPIELER_ID,
            output_dir=tmp_path,
            api_client=client,
            state=state,
        )
        crawler2.run()

        assert client._http.get.call_count == first_call_count + 1  # only player page re-fetched

    def test_turnier_index_selects_second_tournament(self, tmp_path):
        client = _mock_http_for_spieler(turnier_index=1)
        crawler = DwzCrawler(
            spieler_id=SPIELER_ID,
            output_dir=tmp_path,
            turnier_index=1,
            api_client=client,
            state=CrawlState(tmp_path / "crawl_state.json"),
        )
        crawler.run()

        content = (tmp_path / "tournaments.csv").read_text(encoding="utf-8")
        assert "c20ee10e" in content
