"""Crawler: fetches one player and all data for one of their tournaments."""

import logging
import os
from pathlib import Path
from typing import Optional

from .api_client import DwzApiClient, Partie, Spieler, Turnier
from .http_client import CircuitOpenError, MaxRetriesExceededError
from .state import (
    CrawlState,
    export_partien,
    export_spieler,
    export_turniere,
)

LOGGER = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = Path("output")


class DwzCrawler:
    """Crawl one player and one of their tournaments, then export to CSV.

    Usage::

        crawler = DwzCrawler(
            spieler_id="NU4241593",
            output_dir=Path("output"),
        )
        crawler.run()

    The first tournament listed on the player page is crawled unless
    *turnier_index* (0-based) is specified.  Crawl state is persisted in
    ``output/crawl_state.json`` so a previously completed tournament is not
    re-fetched.

    Output files
    ------------
    output/players.csv      – one row for the player
    output/tournaments.csv  – one row for the tournament
    output/games.csv        – one row per game in that tournament
    output/crawl_state.json – resume state
    """

    def __init__(
        self,
        spieler_id: str,
        output_dir: Path = DEFAULT_OUTPUT_DIR,
        turnier_index: int = 0,
        api_client: Optional[DwzApiClient] = None,
        state: Optional[CrawlState] = None,
    ) -> None:
        self._spieler_id = spieler_id
        self._output_dir = output_dir
        self._turnier_index = turnier_index
        self._client = api_client or DwzApiClient()
        self._state = state or CrawlState(output_dir / "crawl_state.json")

    # ------------------------------------------------------------------

    def run(self) -> None:
        """Fetch player + one tournament + games, then write CSVs."""
        spieler = self._fetch_spieler()
        if spieler is None:
            LOGGER.error("Could not retrieve player %s – aborting.", self._spieler_id)
            return

        turnier = self._pick_turnier(spieler)
        if turnier is None:
            LOGGER.error(
                "No tournament found at index %d for player %s.",
                self._turnier_index,
                self._spieler_id,
            )
            return

        partien = self._fetch_partien(turnier)

        export_spieler([spieler], self._output_dir)
        export_turniere([turnier], self._output_dir)
        export_partien(partien, self._output_dir)
        LOGGER.info("Done. Output written to %s/", self._output_dir)

    # ------------------------------------------------------------------

    def _fetch_spieler(self) -> Optional[Spieler]:
        """Return a stub Spieler for the configured spieler_id.

        The player name is not available without fetching the player page; the
        stub uses the ID as the name.  This avoids a redundant HTTP request
        because ``_pick_turnier`` will fetch the same page anyway.
        """
        return Spieler(spieler_id=self._spieler_id, name=self._spieler_id)

    def _pick_turnier(self, spieler: Spieler) -> Optional[Turnier]:
        """Fetch the player's tournament list and return the chosen one."""
        try:
            turniere = self._client.get_spieler_turniere(spieler.spieler_id)
        except (MaxRetriesExceededError, CircuitOpenError) as exc:
            LOGGER.error("Could not fetch tournament list: %s", exc)
            return None

        if not turniere:
            LOGGER.warning("Player %s has no tournaments.", spieler.spieler_id)
            return None

        if self._turnier_index >= len(turniere):
            LOGGER.warning(
                "turnier_index=%d is out of range (player has %d tournaments); "
                "using the first one.",
                self._turnier_index,
                len(turniere),
            )
            return turniere[0]

        return turniere[self._turnier_index]

    def _fetch_partien(self, turnier: Turnier) -> list[Partie]:
        """Fetch games for the tournament, respecting crawl state."""
        if not self._state.is_due(turnier.turnier_id):
            LOGGER.info(
                "Tournament %s already crawled – skipping.", turnier.turnier_id
            )
            return []

        try:
            partien = self._client.get_turnier_partien(
                self._spieler_id, turnier.turnier_id
            )
            self._state.mark_done(turnier.turnier_id)
            return partien
        except CircuitOpenError as exc:
            LOGGER.error("Circuit breaker open: %s", exc)
        except MaxRetriesExceededError as exc:
            LOGGER.error("Max retries exceeded for tournament %s: %s", turnier.turnier_id, exc)
            self._state.mark_failed(turnier.turnier_id, str(exc))
        except Exception as exc:
            LOGGER.error("Unexpected error for tournament %s: %s", turnier.turnier_id, exc)
            self._state.mark_failed(turnier.turnier_id, str(exc))
        return []

