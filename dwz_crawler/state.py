"""Crawl state persistence and CSV export."""

import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .api_client import Partie, Spieler, Turnier

LOGGER = logging.getLogger(__name__)

STATUS_PENDING = "pending"
STATUS_DONE = "done"
STATUS_FAILED = "failed"
STATUS_RETRY_PENDING = "retry_pending"


class CrawlState:
    """Persist and resume crawl progress using a JSON file.

    Schema of ``crawl_state.json``::

        {
          "dwz": {
            "<turnier_id>": {
              "status": "done" | "retry_pending" | "failed",
              "attempts": 2,
              "next_attempt_at": "2026-08-26T18:15:00Z",
              "last_http_status": 503
            }
          }
        }
    """

    def __init__(self, state_file: Path = Path("output/crawl_state.json")) -> None:
        self._file = state_file
        self._state: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if self._file.exists():
            try:
                with open(self._file, encoding="utf-8") as fh:
                    return json.load(fh)
            except json.JSONDecodeError:
                LOGGER.warning("Corrupt crawl_state.json – starting fresh.")
        return {"dwz": {}}

    def save(self) -> None:
        self._file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._file, "w", encoding="utf-8") as fh:
            json.dump(self._state, fh, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    def get_turnier_status(self, turnier_id: str) -> Optional[dict]:
        return self._state["dwz"].get(turnier_id)

    def mark_done(self, turnier_id: str) -> None:
        self._state["dwz"][turnier_id] = {"status": STATUS_DONE}
        self.save()

    def mark_retry_pending(
        self,
        turnier_id: str,
        attempts: int,
        next_attempt_at: datetime,
        last_http_status: int,
    ) -> None:
        self._state["dwz"][turnier_id] = {
            "status": STATUS_RETRY_PENDING,
            "attempts": attempts,
            "next_attempt_at": next_attempt_at.isoformat(),
            "last_http_status": last_http_status,
        }
        self.save()

    def mark_failed(self, turnier_id: str, reason: str) -> None:
        self._state["dwz"][turnier_id] = {
            "status": STATUS_FAILED,
            "reason": reason,
        }
        self.save()

    def is_due(self, turnier_id: str) -> bool:
        """Return True if the turnier should be (re-)crawled now."""
        entry = self.get_turnier_status(turnier_id)
        if entry is None:
            return True
        if entry["status"] == STATUS_DONE:
            return False
        if entry["status"] == STATUS_RETRY_PENDING:
            next_at_str: Optional[str] = entry.get("next_attempt_at")
            if next_at_str:
                next_at = datetime.fromisoformat(next_at_str)
                return datetime.now(tz=timezone.utc) >= next_at
        return True


def _csv_path(output_dir: Path, name: str) -> Path:
    return output_dir / f"{name}.csv"


def export_spieler(spieler_list: list[Spieler], output_dir: Path) -> Path:
    path = _csv_path(output_dir, "players")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "spieler_id",
                "name",
                "dwz",
                "fide_elo",
                "verband",
                "verein",
                "verein_id",
                "geburtsjahr",
            ],
        )
        writer.writeheader()
        for s in spieler_list:
            writer.writerow(
                {
                    "spieler_id": s.spieler_id,
                    "name": s.name,
                    "dwz": s.dwz,
                    "fide_elo": s.fide_elo,
                    "verband": s.verband,
                    "verein": s.verein,
                    "verein_id": s.verein_id,
                    "geburtsjahr": s.geburtsjahr,
                }
            )
    LOGGER.info("Exported %d players to %s", len(spieler_list), path)
    return path


def export_turniere(turniere: list[Turnier], output_dir: Path) -> Path:
    path = _csv_path(output_dir, "tournaments")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "turnier_id",
                "name",
                "datum_von",
                "datum_bis",
                "ort",
                "organisator",
                "wertungs_id",
            ],
        )
        writer.writeheader()
        for t in turniere:
            writer.writerow(
                {
                    "turnier_id": t.turnier_id,
                    "name": t.name,
                    "datum_von": t.datum_von,
                    "datum_bis": t.datum_bis,
                    "ort": t.ort,
                    "organisator": t.organisator,
                    "wertungs_id": t.wertungs_id,
                }
            )
    LOGGER.info("Exported %d tournaments to %s", len(turniere), path)
    return path


def export_partien(partien: list[Partie], output_dir: Path) -> Path:
    path = _csv_path(output_dir, "games")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "turnier_id",
                "runde",
                "spieler_id",
                "gegner_id",
                "gegner_name",
                "farbe",
                "ergebnis",
            ],
        )
        writer.writeheader()
        for p in partien:
            writer.writerow(
                {
                    "turnier_id": p.turnier_id,
                    "runde": p.runde,
                    "spieler_id": p.spieler_id,
                    "gegner_id": p.gegner_id,
                    "gegner_name": p.gegner_name,
                    "farbe": p.farbe,
                    "ergebnis": p.ergebnis,
                }
            )
    LOGGER.info("Exported %d games to %s", len(partien), path)
    return path
