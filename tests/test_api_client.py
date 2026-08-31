"""Tests for HTML scraping helpers in dwz_crawler/api_client.py.

All tests run against static HTML fixtures — no network access required.
"""

from pathlib import Path

import pytest

from dwz_crawler.api_client import (
    _parse_spieler_turniere,
    _parse_turnier_partien,
    _parse_vereinsspieler,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def _load(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# _parse_vereinsspieler
# ---------------------------------------------------------------------------


class TestParseVereinsspieler:
    def test_returns_two_players(self):
        html = _load("verein_F2810.html")
        players = _parse_vereinsspieler(html, "F2810")
        assert len(players) == 2

    def test_spieler_id_extracted(self):
        html = _load("verein_F2810.html")
        players = _parse_vereinsspieler(html, "F2810")
        assert players[0].spieler_id == "NU4241593"
        assert players[1].spieler_id == "NU4241600"

    def test_name_extracted(self):
        html = _load("verein_F2810.html")
        players = _parse_vereinsspieler(html, "F2810")
        assert players[0].name == "Mustermann, Max"

    def test_dwz_extracted(self):
        html = _load("verein_F2810.html")
        players = _parse_vereinsspieler(html, "F2810")
        assert players[0].dwz == 1854
        assert players[1].dwz == 1620

    def test_fide_elo_extracted(self):
        html = _load("verein_F2810.html")
        players = _parse_vereinsspieler(html, "F2810")
        assert players[0].fide_elo == 0   # 0 in fixture
        assert players[1].fide_elo == 1610

    def test_geburtsjahr_extracted(self):
        html = _load("verein_F2810.html")
        players = _parse_vereinsspieler(html, "F2810")
        assert players[0].geburtsjahr == 1985

    def test_verein_id_set(self):
        html = _load("verein_F2810.html")
        players = _parse_vereinsspieler(html, "F2810")
        assert all(p.verein_id == "F2810" for p in players)

    def test_missing_table_returns_empty(self):
        result = _parse_vereinsspieler("<html><body></body></html>", "F2810")
        assert result == []


# ---------------------------------------------------------------------------
# _parse_spieler_turniere
# ---------------------------------------------------------------------------


class TestParseSpielerTurniere:
    def test_returns_two_tournaments(self):
        html = _load("spieler_NU4241593.html")
        turniere = _parse_spieler_turniere(html)
        assert len(turniere) == 2

    def test_turnier_id_contains_both_uuids(self):
        html = _load("spieler_NU4241593.html")
        turniere = _parse_spieler_turniere(html)
        assert (
            turniere[0].turnier_id
            == "434ecfd3-821d-410a-9d9f-d4ea01872f90/79824ba5-3fa2-48ca-8a2d-f9be68e55809"
        )

    def test_name_extracted(self):
        html = _load("spieler_NU4241593.html")
        turniere = _parse_spieler_turniere(html)
        assert turniere[0].name == "Dresdner Stadtmeisterschaft 2025"

    def test_datum_von_extracted(self):
        html = _load("spieler_NU4241593.html")
        turniere = _parse_spieler_turniere(html)
        assert turniere[0].datum_von == "2025-11-01"

    def test_datum_bis_extracted(self):
        html = _load("spieler_NU4241593.html")
        turniere = _parse_spieler_turniere(html)
        assert turniere[0].datum_bis == "2025-11-03"

    def test_ort_extracted(self):
        html = _load("spieler_NU4241593.html")
        turniere = _parse_spieler_turniere(html)
        assert turniere[0].ort == "Dresden"

    def test_missing_table_returns_empty(self):
        result = _parse_spieler_turniere("<html><body></body></html>")
        assert result == []


# ---------------------------------------------------------------------------
# _parse_turnier_partien
# ---------------------------------------------------------------------------

TURNIER_ID = (
    "434ecfd3-821d-410a-9d9f-d4ea01872f90/"
    "79824ba5-3fa2-48ca-8a2d-f9be68e55809"
)
SPIELER_ID = "NU4241593"


class TestParseTurnierPartien:
    def test_returns_three_games(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert len(partien) == 3

    def test_runde_extracted(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert [p.runde for p in partien] == [1, 2, 3]

    def test_gegner_id_extracted(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert partien[0].gegner_id == "NU4241600"
        assert partien[1].gegner_id == "NU9999999"

    def test_gegner_name_extracted(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert partien[0].gegner_name == "Musterfrau, Erika"

    def test_farbe_extracted(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert partien[0].farbe == "W"
        assert partien[1].farbe == "B"

    def test_ergebnis_extracted(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert partien[0].ergebnis == "1"
        assert partien[1].ergebnis == "0.5"
        assert partien[2].ergebnis == "+"

    def test_spieler_id_set_on_all_games(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert all(p.spieler_id == SPIELER_ID for p in partien)

    def test_turnier_id_set_on_all_games(self):
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert all(p.turnier_id == TURNIER_ID for p in partien)

    def test_bye_row_no_gegner_id(self):
        """Row 3 has an empty Gegner cell (bye/walkover) – gegner_id must be None."""
        html = _load("turnier_partien.html")
        partien = _parse_turnier_partien(html, SPIELER_ID, TURNIER_ID)
        assert partien[2].gegner_id is None

    def test_no_tables_returns_empty(self):
        result = _parse_turnier_partien("<html><body></body></html>", SPIELER_ID, TURNIER_ID)
        assert result == []
