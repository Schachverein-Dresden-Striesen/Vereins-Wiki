"""Main crawler orchestrator."""

import logging
import os
from pathlib import Path
from typing import Optional

from .api_client import DwzApiClient, Partie, Spieler, Turnier
from .http_client import CircuitOpenError, HttpClient, MaxRetriesExceededError
from .state import (
    CrawlState,
    export_partien,
    export_spieler,
    export_turniere,
)

LOGGER = logging.getLogger(__name__)

DEFAULT_VEREIN_ID = "F2810"
DEFAULT_OUTPUT_DIR = Path("output")


class DwzCrawler:
    """Crawl DWZ data for a chess club and export to CSV.

    Usage::

        crawler = DwzCrawler(verein_id="F2810", output_dir=Path("output"))
        crawler.run()

    Crawl state is persisted in ``output/crawl_state.json`` so that the
    crawler can be resumed after a failure or throttling event.
    """

    def __init__(
        self,
        verein_id: str = DEFAULT_VEREIN_ID,
        output_dir: Path = DEFAULT_OUTPUT_DIR,
        api_client: Optional[DwzApiClient] = None,
        state: Optional[CrawlState] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self._verein_id = verein_id
        self._output_dir = output_dir
        self._client = api_client or DwzApiClient()
        self._state = state or CrawlState(output_dir / "crawl_state.json")
        self._username = username or os.getenv("DWZ_USERNAME", "")
        self._password = password or os.getenv("DWZ_PASSWORD", "")

    def run(self) -> None:
        """Run the full crawl: players → tournaments → games → CSV export."""
        if self._username and self._password:
            try:
                self._client.login(self._username, self._password)
            except Exception as exc:
                LOGGER.warning("Login failed (%s) – continuing as anonymous.", exc)

        LOGGER.info("Fetching players for Verein %s", self._verein_id)
        spieler_list = self._fetch_spieler()
        export_spieler(spieler_list, self._output_dir)

        all_turniere: list[Turnier] = []
        all_partien: list[Partie] = []

        for spieler in spieler_list:
            LOGGER.info("Processing player %s (%s)", spieler.name, spieler.spieler_id)
            try:
                turniere = self._client.get_spieler_turniere(spieler.spieler_id)
            except (MaxRetriesExceededError, CircuitOpenError) as exc:
                LOGGER.error(
                    "Could not fetch tournaments for %s: %s", spieler.spieler_id, exc
                )
                continue

            for turnier in turniere:
                if turnier not in all_turniere:
                    all_turniere.append(turnier)

                if not self._state.is_due(turnier.turnier_id):
                    LOGGER.debug(
                        "Skipping already-crawled tournament %s", turnier.turnier_id
                    )
                    continue

                try:
                    partien = self._client.get_turnier_partien(
                        spieler.spieler_id, turnier.turnier_id
                    )
                    all_partien.extend(partien)
                    self._state.mark_done(turnier.turnier_id)
                except CircuitOpenError as exc:
                    LOGGER.error("Circuit open: %s", exc)
                    # Save progress and abort to avoid hammering the API
                    break
                except MaxRetriesExceededError as exc:
                    LOGGER.error(
                        "Max retries for tournament %s: %s",
                        turnier.turnier_id,
                        exc,
                    )
                    self._state.mark_failed(turnier.turnier_id, str(exc))
                except Exception as exc:
                    LOGGER.error(
                        "Unexpected error for tournament %s: %s",
                        turnier.turnier_id,
                        exc,
                    )
                    self._state.mark_failed(turnier.turnier_id, str(exc))

        export_turniere(all_turniere, self._output_dir)
        export_partien(all_partien, self._output_dir)
        LOGGER.info("Crawl complete.")

    def _fetch_spieler(self) -> list[Spieler]:
        try:
            return self._client.get_vereinsspieler(self._verein_id)
        except (MaxRetriesExceededError, CircuitOpenError) as exc:
            LOGGER.error("Could not fetch players: %s", exc)
            return []
