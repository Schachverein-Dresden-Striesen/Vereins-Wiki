"""Schachbund.de REST API client.

Endpoints based on:
  https://www.schachbund.de/rest-schnittstelle-des-wertungsportals.html
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from .http_client import HttpClient

LOGGER = logging.getLogger(__name__)

BASE_URL = "https://www.schachbund.de"


@dataclass
class Spieler:
    """A chess player with DWZ rating data."""

    spieler_id: str
    name: str
    dwz: Optional[int] = None
    fide_elo: Optional[int] = None
    verband: Optional[str] = None
    verein: Optional[str] = None
    verein_id: Optional[str] = None
    geburtsjahr: Optional[int] = None


@dataclass
class Turnier:
    """A chess tournament."""

    turnier_id: str
    name: str
    datum_von: Optional[str] = None
    datum_bis: Optional[str] = None
    ort: Optional[str] = None
    organisator: Optional[str] = None
    wertungs_id: Optional[str] = None


@dataclass
class Partie:
    """A single chess game within a tournament."""

    turnier_id: str
    runde: int
    spieler_id: str
    gegner_id: Optional[str]
    farbe: Optional[str]   # "W" or "B"
    ergebnis: Optional[str]  # "1", "0", "0.5", "+", "-", etc.
    gegner_name: Optional[str] = None


@dataclass
class VereinData:
    """Aggregated data fetched for one club."""

    verein_id: str
    spieler: list[Spieler] = field(default_factory=list)
    turniere: list[Turnier] = field(default_factory=list)
    partien: list[Partie] = field(default_factory=list)


class DwzApiClient:
    """Client for the Schachbund.de DWZ portal REST API.

    The public REST interface is documented at:
      https://www.schachbund.de/rest-schnittstelle-des-wertungsportals.html

    All endpoints return JSON.  Authentication (if required) is performed by
    passing ``DWZ_USERNAME`` / ``DWZ_PASSWORD`` environment variables which
    are forwarded to the login endpoint once and stored as a session cookie.
    """

    _API_BASE = f"{BASE_URL}/wertungsportal/api/v1"
    _LOGIN_URL = f"{BASE_URL}/anmelden.html"

    def __init__(self, http_client: Optional[HttpClient] = None) -> None:
        self._http = http_client or HttpClient()

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> None:
        """Authenticate against the Schachbund portal."""
        import requests as _requests

        session = _requests.Session()
        resp = session.post(
            self._LOGIN_URL,
            data={"username": username, "password": password},
            timeout=30,
            allow_redirects=True,
        )
        if resp.status_code not in (200, 302):
            raise RuntimeError(
                f"Login failed with HTTP {resp.status_code}"
            )
        LOGGER.info("Login successful (HTTP %d)", resp.status_code)
        # Re-use the authenticated session for subsequent API calls
        self._http = HttpClient(session=session)

    # ------------------------------------------------------------------
    # Verein (Club)
    # ------------------------------------------------------------------

    def get_vereinsspieler(self, verein_id: str) -> list[Spieler]:
        """Fetch all players of a club.

        Endpoint: GET /wertungsportal/api/v1/vereine/{verein_id}/mitglieder
        Falls back to scraping the public page if the JSON API returns 404.
        """
        url = f"{self._API_BASE}/vereine/{verein_id}/mitglieder"
        resp = self._http.get(url)
        if resp.status_code == 404:
            LOGGER.warning(
                "API endpoint %s not found, falling back to HTML scraping.", url
            )
            return self._scrape_vereinsspieler(verein_id)

        return self._parse_spielerliste(resp.json(), verein_id)

    def _scrape_vereinsspieler(self, verein_id: str) -> list[Spieler]:
        """Scrape player list from the public club HTML page."""
        from bs4 import BeautifulSoup

        url = f"{BASE_URL}/dwz-vereine/{verein_id}.html"
        resp = self._http.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        spieler_list: list[Spieler] = []
        table = soup.find("table", {"id": "dewisTable"})
        if not table:
            LOGGER.warning("No dewisTable found on %s", url)
            return spieler_list
        for row in table.select("tbody tr"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue
            link = cells[3].find("a")
            spieler_id = ""
            if link and link.get("href"):
                # href like /dwz-spieler/NU4241593.html
                href: str = link["href"]
                spieler_id = href.split("/")[-1].replace(".html", "")
            spieler_list.append(
                Spieler(
                    spieler_id=spieler_id,
                    name=cells[3].get_text(strip=True),
                    dwz=_safe_int(cells[4].get_text(strip=True)) if len(cells) > 4 else None,
                    verein_id=verein_id,
                )
            )
        return spieler_list

    def _parse_spielerliste(self, data: list[dict], verein_id: str) -> list[Spieler]:
        spieler_list: list[Spieler] = []
        for item in data:
            spieler_list.append(
                Spieler(
                    spieler_id=str(item.get("id", item.get("spielerId", ""))),
                    name=item.get("name", ""),
                    dwz=_safe_int(item.get("dwz")),
                    fide_elo=_safe_int(item.get("fideElo")),
                    verband=item.get("verband"),
                    verein=item.get("verein"),
                    verein_id=verein_id,
                    geburtsjahr=_safe_int(item.get("geburtsjahr")),
                )
            )
        return spieler_list

    # ------------------------------------------------------------------
    # Spieler (Player)
    # ------------------------------------------------------------------

    def get_spieler_turniere(self, spieler_id: str) -> list[Turnier]:
        """Fetch tournaments played by a specific player."""
        url = f"{self._API_BASE}/spieler/{spieler_id}/turniere"
        resp = self._http.get(url)
        if resp.status_code == 404:
            return self._scrape_spieler_turniere(spieler_id)
        return self._parse_turnierliste(resp.json())

    def _scrape_spieler_turniere(self, spieler_id: str) -> list[Turnier]:
        from bs4 import BeautifulSoup

        url = f"{BASE_URL}/dwz-spieler/{spieler_id}.html"
        resp = self._http.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        turniere: list[Turnier] = []
        table = soup.find("table", {"id": "dewisTable"})
        if not table:
            return turniere
        for row in table.select("tbody tr"):
            cells = row.find_all("td")
            if len(cells) < 3:
                continue
            link = cells[2].find("a")
            turnier_id = ""
            if link and link.get("href"):
                href: str = link["href"]
                # href like /dwz-turniere/<uuid>/<uuid>.html
                parts = href.rstrip("/").split("/")
                turnier_id = "/".join(parts[-2:]).replace(".html", "")
            turniere.append(
                Turnier(
                    turnier_id=turnier_id,
                    name=cells[2].get_text(strip=True),
                    datum_von=cells[0].get_text(strip=True) if cells else None,
                )
            )
        return turniere

    def _parse_turnierliste(self, data: list[dict]) -> list[Turnier]:
        result: list[Turnier] = []
        for item in data:
            result.append(
                Turnier(
                    turnier_id=str(item.get("id", item.get("turnierId", ""))),
                    name=item.get("name", ""),
                    datum_von=item.get("datumVon"),
                    datum_bis=item.get("datumBis"),
                    ort=item.get("ort"),
                    organisator=item.get("organisator"),
                    wertungs_id=item.get("wertungsId"),
                )
            )
        return result

    # ------------------------------------------------------------------
    # Turnier / Partien
    # ------------------------------------------------------------------

    def get_turnier_partien(self, spieler_id: str, turnier_id: str) -> list[Partie]:
        """Fetch all games of a player in a specific tournament."""
        url = f"{self._API_BASE}/spieler/{spieler_id}/turniere/{turnier_id}/partien"
        resp = self._http.get(url)
        if resp.status_code == 404:
            return self._scrape_turnier_partien(spieler_id, turnier_id)
        return self._parse_partien(resp.json(), spieler_id, turnier_id)

    def _scrape_turnier_partien(
        self, spieler_id: str, turnier_id: str
    ) -> list[Partie]:
        from bs4 import BeautifulSoup

        url = f"{BASE_URL}/dwz-turniere/{turnier_id}.html"
        resp = self._http.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        partien: list[Partie] = []
        for table in soup.select("table.table_responsiv"):
            for row in table.select("tbody tr"):
                cells = row.find_all("td")
                if len(cells) < 4:
                    continue
                runde_text = cells[0].get_text(strip=True)
                runde = _safe_int(runde_text) or 0
                gegner_cell = cells[1]
                gegner_link = gegner_cell.find("a")
                gegner_id = None
                gegner_name = None
                if gegner_link:
                    gegner_name = gegner_link.get_text(strip=True)
                    href: str = gegner_link.get("href", "")
                    gegner_id = href.split("/")[-1].replace(".html", "")
                farbe = cells[2].get_text(strip=True) if len(cells) > 2 else None
                ergebnis = cells[3].get_text(strip=True) if len(cells) > 3 else None
                partien.append(
                    Partie(
                        turnier_id=turnier_id,
                        runde=runde,
                        spieler_id=spieler_id,
                        gegner_id=gegner_id,
                        gegner_name=gegner_name,
                        farbe=farbe,
                        ergebnis=ergebnis,
                    )
                )
        return partien

    def _parse_partien(
        self, data: list[dict], spieler_id: str, turnier_id: str
    ) -> list[Partie]:
        result: list[Partie] = []
        for item in data:
            result.append(
                Partie(
                    turnier_id=turnier_id,
                    runde=int(item.get("runde", 0)),
                    spieler_id=spieler_id,
                    gegner_id=str(item.get("gegnerId", "")),
                    gegner_name=item.get("gegnerName"),
                    farbe=item.get("farbe"),
                    ergebnis=item.get("ergebnis"),
                )
            )
        return result


def _safe_int(value) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
