"""Schachbund.de HTML scraper.

Data is fetched from the public DWZ portal HTML pages:
  - Verein:  https://www.schachbund.de/dwz-vereine/{verein_id}.html
  - Spieler: https://www.schachbund.de/dwz-spieler/{spieler_id}.html
  - Turnier: https://www.schachbund.de/dwz-turniere/{uuid1}/{uuid2}.html

No REST API is used; all data is parsed from HTML tables.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from bs4 import BeautifulSoup

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
    farbe: Optional[str]  # "W" or "B"
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
    """Scraper for Schachbund.de public DWZ HTML pages.

    All data is fetched by parsing HTML tables; the previously available
    REST API (``/wertungsportal/api/v1/…``) is no longer used.

    Page patterns
    -------------
    Club members:
        ``/dwz-vereine/{verein_id}.html``
        Table ``#dewisTable`` — columns vary by page, but player links are
        in the column whose ``<a>`` href matches ``/dwz-spieler/…``

    Player tournaments:
        ``/dwz-spieler/{spieler_id}.html``
        Table ``#dewisTable`` — tournament links have href matching
        ``/dwz-turniere/…``

    Tournament games (per player):
        ``/dwz-turniere/{uuid1}/{uuid2}.html``
        Tables with class ``table_responsiv`` — one table per player section;
        columns: Runde | Gegner | Farbe | Ergebnis
    """

    def __init__(self, http_client: Optional[HttpClient] = None) -> None:
        self._http = http_client or HttpClient()

    # ------------------------------------------------------------------
    # Verein (Club)
    # ------------------------------------------------------------------

    def get_vereinsspieler(self, verein_id: str) -> list[Spieler]:
        """Scrape all players listed on the club page.

        URL: ``/dwz-vereine/{verein_id}.html``
        """
        url = f"{BASE_URL}/dwz-vereine/{verein_id}.html"
        resp = self._http.get(url)
        resp.raise_for_status()
        return _parse_vereinsspieler(resp.text, verein_id, url)

    # ------------------------------------------------------------------
    # Spieler (Player)
    # ------------------------------------------------------------------

    def get_spieler_turniere(self, spieler_id: str) -> list[Turnier]:
        """Scrape all tournaments listed on a player's page.

        URL: ``/dwz-spieler/{spieler_id}.html``
        """
        url = f"{BASE_URL}/dwz-spieler/{spieler_id}.html"
        resp = self._http.get(url)
        resp.raise_for_status()
        return _parse_spieler_turniere(resp.text, url)

    # ------------------------------------------------------------------
    # Turnier / Partien
    # ------------------------------------------------------------------

    def get_turnier_partien(self, spieler_id: str, turnier_id: str) -> list[Partie]:
        """Scrape all games of a player from a tournament page.

        ``turnier_id`` is the path segment after ``/dwz-turniere/``, e.g.
        ``434ecfd3-821d-410a-9d9f-d4ea01872f90/79824ba5-3fa2-48ca-8a2d-f9be68e55809``

        URL: ``/dwz-turniere/{turnier_id}.html``
        """
        url = f"{BASE_URL}/dwz-turniere/{turnier_id}.html"
        resp = self._http.get(url)
        resp.raise_for_status()
        return _parse_turnier_partien(resp.text, spieler_id, turnier_id, url)


# ---------------------------------------------------------------------------
# Pure HTML-parsing helpers (no I/O; easily unit-tested with fixture HTML)
# ---------------------------------------------------------------------------


def _parse_vereinsspieler(html: str, verein_id: str, source_url: str = "") -> list[Spieler]:
    """Parse the ``#dewisTable`` on a ``/dwz-vereine/…`` page.

    Expected column layout (0-indexed):
        0: Lfd. Nr.
        1: DWZ-Ausweis-Nr
        2: Nat.
        3: Name  ← link to /dwz-spieler/{id}.html
        4: DWZ (current rating)
        5: DWZ-Index
        6: FIDE-Elo  (optional)
        7: Geburtsjahr (optional)
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "dewisTable"})
    if not table:
        LOGGER.warning("No #dewisTable found on %s", source_url)
        return []

    # Detect column positions dynamically from the header row
    header_cells = table.select("thead tr th")
    col: dict[str, int] = {}
    for i, th in enumerate(header_cells):
        text = th.get_text(strip=True).lower()
        if "name" in text:
            col["name"] = i
        elif text == "dwz":
            # Exact match: only the plain "DWZ" rating column, not "DWZ-Ausweis-Nr." etc.
            col["dwz"] = i
        elif "elo" in text:
            col["fide_elo"] = i
        elif "geburt" in text or "jg" in text:
            col["geburtsjahr"] = i

    spieler_list: list[Spieler] = []
    for row in table.select("tbody tr"):
        cells = row.find_all("td")
        if not cells:
            continue

        # Find the cell containing the player link
        spieler_id = ""
        name = ""
        link_cell_idx = col.get("name")
        if link_cell_idx is not None and link_cell_idx < len(cells):
            link = cells[link_cell_idx].find("a")
        else:
            # Fallback: find the first <a> pointing to /dwz-spieler/
            link = None
            for cell in cells:
                a = cell.find("a", href=lambda h: h and "/dwz-spieler/" in h)
                if a:
                    link = a
                    break

        if link:
            name = link.get_text(strip=True)
            href: str = link.get("href", "")
            spieler_id = href.rstrip("/").split("/")[-1].replace(".html", "")

        if not spieler_id:
            continue

        dwz_col = col.get("dwz")
        dwz = _safe_int(cells[dwz_col].get_text(strip=True)) if dwz_col is not None and dwz_col < len(cells) else None

        fide_col = col.get("fide_elo")
        fide_elo = _safe_int(cells[fide_col].get_text(strip=True)) if fide_col is not None and fide_col < len(cells) else None

        gj_col = col.get("geburtsjahr")
        geburtsjahr = _safe_int(cells[gj_col].get_text(strip=True)) if gj_col is not None and gj_col < len(cells) else None

        spieler_list.append(
            Spieler(
                spieler_id=spieler_id,
                name=name,
                dwz=dwz,
                fide_elo=fide_elo,
                verein_id=verein_id,
                geburtsjahr=geburtsjahr,
            )
        )

    LOGGER.info("Parsed %d players from %s", len(spieler_list), source_url)
    return spieler_list


def _parse_spieler_turniere(html: str, source_url: str = "") -> list[Turnier]:
    """Parse the ``#dewisTable`` on a ``/dwz-spieler/…`` page.

    Expected column layout (0-indexed):
        0: Datum / Von
        1: Datum / Bis  (optional — may be merged)
        2: Turniername  ← link to /dwz-turniere/<uuid>/<uuid>.html
        3: Ort          (optional)
        4: Organisator  (optional)
        5: Wertungs-ID  (optional)
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "dewisTable"})
    if not table:
        LOGGER.warning("No #dewisTable found on %s", source_url)
        return []

    # Detect column positions from header
    header_cells = table.select("thead tr th")
    col: dict[str, int] = {}
    for i, th in enumerate(header_cells):
        text = th.get_text(strip=True).lower()
        if "von" in text or (i == 0 and "datum" in text):
            col["datum_von"] = i
        elif "bis" in text:
            col["datum_bis"] = i
        elif "turnier" in text or "name" in text:
            col["name"] = i
        elif "ort" in text:
            col["ort"] = i
        elif "organisat" in text:
            col["organisator"] = i
        elif "wertung" in text:
            col["wertungs_id"] = i

    turniere: list[Turnier] = []
    for row in table.select("tbody tr"):
        cells = row.find_all("td")
        if not cells:
            continue

        # Find the cell with the tournament link
        name_col = col.get("name")
        link = None
        if name_col is not None and name_col < len(cells):
            link = cells[name_col].find("a")
        if not link:
            for cell in cells:
                a = cell.find("a", href=lambda h: h and "/dwz-turniere/" in h)
                if a:
                    link = a
                    break

        turnier_id = ""
        name = ""
        if link:
            name = link.get_text(strip=True)
            href: str = link.get("href", "")
            # href: /dwz-turniere/<uuid1>/<uuid2>.html
            parts = href.rstrip("/").replace(".html", "").split("/")
            # Keep the two UUID path segments
            turnier_id = "/".join(parts[-2:]) if len(parts) >= 2 else parts[-1]

        if not turnier_id:
            continue

        dv_col = col.get("datum_von", 0)
        datum_von = cells[dv_col].get_text(strip=True) if dv_col < len(cells) else None

        db_col = col.get("datum_bis")
        datum_bis = cells[db_col].get_text(strip=True) if db_col is not None and db_col < len(cells) else None

        ort_col = col.get("ort")
        ort = cells[ort_col].get_text(strip=True) if ort_col is not None and ort_col < len(cells) else None

        org_col = col.get("organisator")
        organisator = cells[org_col].get_text(strip=True) if org_col is not None and org_col < len(cells) else None

        wid_col = col.get("wertungs_id")
        wertungs_id = cells[wid_col].get_text(strip=True) if wid_col is not None and wid_col < len(cells) else None

        turniere.append(
            Turnier(
                turnier_id=turnier_id,
                name=name,
                datum_von=datum_von,
                datum_bis=datum_bis,
                ort=ort,
                organisator=organisator,
                wertungs_id=wertungs_id,
            )
        )

    LOGGER.info("Parsed %d tournaments from %s", len(turniere), source_url)
    return turniere


def _parse_turnier_partien(
    html: str, spieler_id: str, turnier_id: str, source_url: str = ""
) -> list[Partie]:
    """Parse game tables on a ``/dwz-turniere/…`` page.

    Each ``table.table_responsiv`` block contains one player's results.
    Expected column layout (0-indexed):
        0: Runde
        1: Gegner name ← <a href="/dwz-spieler/{id}.html">
        2: Farbe  (W/B or w/s)
        3: Ergebnis (1 / 0 / ½ / + / -)
    """
    soup = BeautifulSoup(html, "html.parser")
    partien: list[Partie] = []

    for table in soup.select("table.table_responsiv"):
        for row in table.select("tbody tr"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            runde = _safe_int(cells[0].get_text(strip=True)) or 0

            gegner_link = cells[1].find("a")
            gegner_id: Optional[str] = None
            gegner_name: Optional[str] = None
            if gegner_link:
                gegner_name = gegner_link.get_text(strip=True)
                href: str = gegner_link.get("href", "")
                gegner_id = href.rstrip("/").split("/")[-1].replace(".html", "")
            else:
                gegner_name = cells[1].get_text(strip=True) or None

            farbe = cells[2].get_text(strip=True) or None
            ergebnis = cells[3].get_text(strip=True) or None

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

    LOGGER.info("Parsed %d games from %s", len(partien), source_url)
    return partien


def _safe_int(value) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None

