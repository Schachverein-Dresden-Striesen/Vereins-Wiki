---
layout: single
title: "Mitmachen im Vereins-Wiki – Schritt-für-Schritt"
sidebar:
  nav: "main"
---

Willkommen! Diese Anleitung erklärt Ihnen Schritt für Schritt, wie Sie Inhalte im Vereins-Wiki des Schachvereins Dresden-Striesen beitragen können – ganz ohne Vorkenntnisse in Programmierung oder Webentwicklung.

## Zielgruppe und Zweck

Diese Anleitung richtet sich an **alle Vereinsmitglieder**, die:

- Neuigkeiten, Berichte oder Ergebnisse auf der Vereinswebsite veröffentlichen möchten,
- bestehende Inhalte korrigieren oder ergänzen wollen,
- noch keine Erfahrung mit GitHub oder Markdown haben.

Das Vereins-Wiki basiert auf [GitHub Pages](https://pages.github.com/) und [Jekyll](https://jekyllrb.com/). Alle Inhalte werden als einfache Textdateien (Markdown) gepflegt und über GitHub verwaltet. Änderungen werden nach einer kurzen Prüfung automatisch auf der Website veröffentlicht.

---

## Schritt 1 – GitHub verstehen

### Was ist GitHub?

[GitHub](https://github.com) ist eine Plattform zur gemeinsamen Bearbeitung von Dateien und Projekten. Stellen Sie sich GitHub wie einen gemeinsamen Ordner in der Cloud vor, in dem alle Änderungen nachvollziehbar gespeichert werden.

### Wichtige Begriffe

| Begriff | Bedeutung |
|---|---|
| **Repository (Repo)** | Der zentrale Ordner des Projekts – hier liegen alle Dateien des Wikis. |
| **Branch** | Eine separate Arbeitskopie des Repos, in der Sie Änderungen vorbereiten, ohne das Original zu verändern. |
| **Commit** | Eine gespeicherte Änderung mit einer kurzen Beschreibung (z. B. „Turnierergebnis April hinzugefügt"). |
| **Pull Request (PR)** | Eine Anfrage, Ihre Änderungen in den Haupt-Branch zu übernehmen – zur Kontrolle vor der Veröffentlichung. |
| **Fork** | Eine persönliche Kopie eines Repositories, in der Sie frei arbeiten können. |
| **Merge** | Das Zusammenführen von Änderungen aus einem Branch/Fork in den Haupt-Branch. |

### Die GitHub-Oberfläche auf einen Blick

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub.com  [Suche]           [Benachrichtigungen] [Profil] │
├─────────────────────────────────────────────────────────────┤
│  Repository: Schachverein-Dresden-Striesen / Vereins-Wiki    │
│                                                             │
│  [< > Code]  [Issues]  [Pull Requests]  [Actions]           │
│                                                             │
│  Branch: website  ▼                    [Datei bearbeiten]   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 📁 pages/        Inhaltsseiten der Website          │    │
│  │ 📁 files/        Bilder und Dokumente               │    │
│  │ 📄 index.md      Startseite                         │    │
│  │ 📄 _config.yml   Konfiguration                      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

Das **Vereins-Wiki Repository** finden Sie hier:
[→ github.com/Schachverein-Dresden-Striesen/Vereins-Wiki](https://github.com/Schachverein-Dresden-Striesen/Vereins-Wiki)

---

## Schritt 2 – GitHub-Konto anlegen und konfigurieren

### 2.1 Konto erstellen

1. Öffnen Sie [github.com](https://github.com) im Browser.
2. Klicken Sie auf **„Sign up"** (oben rechts).
3. Geben Sie eine E-Mail-Adresse, einen Benutzernamen und ein Passwort ein.
4. Bestätigen Sie Ihre E-Mail-Adresse über den Bestätigungslink.

> **Tipp:** Wählen Sie einen Benutzernamen, der Ihren echten Namen widerspiegelt (z. B. `max-mustermann`), damit andere Vereinsmitglieder Sie leicht erkennen können.

### 2.2 Zugang zum Vereins-Repository beantragen

Da das Vereins-Wiki ein privates/öffentliches Repository unter der Organisation ist, bitten Sie einen der Repository-Administratoren, Sie als **Contributor** hinzuzufügen. Schreiben Sie dazu eine kurze Nachricht an:

- Die Vereins-E-Mail: [info@sv-dresden-striesen.de](mailto:info@sv-dresden-striesen.de)

### 2.3 Profil einrichten (optional)

- Laden Sie ein Profilbild hoch.
- Tragen Sie Ihren echten Namen ein (unter *Settings → Profile*), damit Ihre Beiträge klar zugeordnet werden können.

---

## Schritt 3 – Markdown-Syntax lernen

Alle Inhalte des Wikis werden in **Markdown** geschrieben – einem einfachen Textformat, das ohne besondere Software lesbar ist und von GitHub automatisch in schön formatierten HTML-Code umgewandelt wird.

### Die wichtigsten Formatierungen

#### Überschriften

```markdown
# Überschrift 1 (Seitentitel)
## Überschrift 2 (Hauptabschnitt)
### Überschrift 3 (Unterabschnitt)
#### Überschrift 4 (Detail)
```

#### Textformatierung

```markdown
**Fett gedruckter Text**
*Kursiver Text*
~~Durchgestrichener Text~~
```

#### Listen

```markdown
- Erster Punkt
- Zweiter Punkt
  - Eingerückter Unterpunkt

1. Nummerierter erster Punkt
2. Nummerierter zweiter Punkt
```

#### Links und Bilder

```markdown
[Linktext](https://www.beispiel.de)
[→ Interne Seite](/pages/archiv/)

![Bildbeschreibung](/files/mein-bild.jpg)
```

#### Tabellen

```markdown
| Spalte 1 | Spalte 2 | Spalte 3 |
|---|---|---|
| Wert A   | Wert B   | Wert C   |
| Wert D   | Wert E   | Wert F   |
```

**Ergebnis:**

| Spalte 1 | Spalte 2 | Spalte 3 |
|---|---|---|
| Wert A   | Wert B   | Wert C   |
| Wert D   | Wert E   | Wert F   |

#### Zitate und Hinweise

```markdown
> Dies ist ein hervorgehobener Hinweis oder ein Zitat.
```

#### Horizontale Linie (Trennlinie)

```markdown
---
```

### Jekyll Front Matter

Jede Seite im Wiki beginnt mit einem **Front Matter**-Block, der Metadaten für Jekyll enthält:

```markdown
---
layout: single
title: "Titel der Seite"
sidebar:
  nav: "main"
---

Hier beginnt der eigentliche Inhalt der Seite...
```

Dieser Block muss **immer am Anfang der Datei** stehen und von `---` eingeschlossen sein.

### Weitere Markdown-Ressourcen

- [Offizielle Markdown-Dokumentation](https://www.markdownguide.org/basic-syntax/) (Englisch)
- [GitHub Markdown-Übersicht](https://docs.github.com/de/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (Deutsch verfügbar)

---

## Schritt 4 – Pull-Request-Workflow verstehen

Der **Pull-Request-Workflow** ist der Standardweg, um Änderungen zu einem Repository beizutragen. Er stellt sicher, dass alle Änderungen vor der Veröffentlichung überprüft werden können.

### Wie funktioniert der Workflow?

```
Ihr Fork/Branch          Haupt-Repository
      │                        │
      │  1. Fork erstellen     │
      │ ◄──────────────────────┤
      │                        │
      │  2. Änderungen machen  │
      │    (Commit)            │
      │                        │
      │  3. Pull Request       │
      │    erstellen           │
      ├───────────────────────►│
      │                        │
      │  4. Überprüfung        │
      │    durch Admin         │
      │                        │
      │  5. Merge &            │
      │    Veröffentlichung    │
      │ ◄──────────────────────┤
```

### Die einzelnen Schritte erklärt

1. **Fork erstellen**: Sie erstellen eine eigene Kopie des Repos (nur beim ersten Mal nötig, wenn Sie kein direkter Contributor sind).
2. **Änderungen vornehmen**: Sie bearbeiten Dateien in Ihrem Fork oder Branch.
3. **Commit erstellen**: Sie speichern Ihre Änderungen mit einer beschreibenden Nachricht.
4. **Pull Request öffnen**: Sie beantragen, dass Ihre Änderungen in das Haupt-Repository übernommen werden.
5. **Überprüfung**: Ein Administrator oder ein anderes Vereinsmitglied prüft Ihre Änderungen.
6. **Merge**: Nach der Genehmigung werden Ihre Änderungen in den Haupt-Branch übernommen und automatisch veröffentlicht.

---

## Schritt 5 – Beispiel-Durchlauf: Turnierergebnis hinzufügen

Hier ist ein vollständiger Durchlauf, wie Sie z. B. ein neues Turnierergebnis direkt über die GitHub-Weboberfläche hinzufügen können.

### 5.1 Repository öffnen

1. Öffnen Sie [github.com/Schachverein-Dresden-Striesen/Vereins-Wiki](https://github.com/Schachverein-Dresden-Striesen/Vereins-Wiki).
2. Melden Sie sich mit Ihrem GitHub-Konto an.

### 5.2 Datei aufrufen und bearbeiten

1. Navigieren Sie in den Ordner **`pages/`**.
2. Klicken Sie auf die Datei, die Sie bearbeiten möchten (z. B. `vereinsturniere.md`).
3. Klicken Sie auf das **Bleistift-Symbol** (✏️) oben rechts in der Dateiansicht, um den Editor zu öffnen.

### 5.3 Inhalt hinzufügen

Fügen Sie Ihren neuen Inhalt im Markdown-Format ein. Beispiel für ein Turnierergebnis:

```markdown
### Vereinsmeisterschaft April 2026

| Platz | Name           | Punkte |
|-------|----------------|--------|
| 1.    | Max Mustermann | 5,5    |
| 2.    | Erika Muster   | 5,0    |
| 3.    | Hans Beispiel  | 4,5    |

*Herzlichen Glückwunsch an alle Platzierten!*
```

### 5.4 Änderungen speichern (Commit)

1. Scrollen Sie nach unten zum Abschnitt **„Commit changes"**.
2. Geben Sie eine kurze, beschreibende Nachricht ein, z. B.:
   - ✅ `Turnierergebnis April 2026 hinzugefügt`
   - ❌ `Änderungen` (zu unspezifisch)
3. Wählen Sie **„Create a new branch for this commit and start a pull request"**.
4. Klicken Sie auf **„Propose changes"**.

### 5.5 Pull Request erstellen

1. Sie werden automatisch zur Pull-Request-Seite weitergeleitet.
2. Überprüfen Sie den Titel und fügen Sie bei Bedarf eine kurze Beschreibung hinzu.
3. Klicken Sie auf **„Create pull request"**.

### 5.6 Auf Überprüfung warten

- Ein Administrator wird Ihre Änderungen prüfen.
- Bei Rückfragen werden diese direkt im Pull Request als Kommentar gestellt.
- Nach der Genehmigung werden Ihre Änderungen automatisch auf der Website veröffentlicht.

> **Gut zu wissen:** Sie können den Status Ihres Pull Requests jederzeit unter
> [github.com/Schachverein-Dresden-Striesen/Vereins-Wiki/pulls](https://github.com/Schachverein-Dresden-Striesen/Vereins-Wiki/pulls)
> einsehen.

---

## Weiterführende Ressourcen

### Offizielle Dokumentationen

- [GitHub Docs (Deutsch)](https://docs.github.com/de) – Offizielle GitHub-Dokumentation
- [GitHub Hello World Tutorial](https://docs.github.com/de/get-started/start-your-journey/hello-world) – Einsteiger-Tutorial von GitHub
- [Markdown Guide](https://www.markdownguide.org/) – Umfassende Markdown-Referenz
- [Jekyll Dokumentation](https://jekyllrb.com/docs/) – Für technisch Interessierte
- [Jekyll Liquid-Syntax](https://jekyllrb.com/docs/liquid/) – Erklärung anderer Jekyll-Vorlagenbefehle

### Im Vereins-Wiki

- [Startseite]({{ site.baseurl }}/) – Übersicht aller Inhalte
- [Archiv]({{ site.baseurl }}/pages/archiv/) – Historische Dokumente
- [README des Repositories](https://github.com/Schachverein-Dresden-Striesen/Vereins-Wiki/blob/website/README.md) – Technische Informationen zur lokalen Entwicklung

### Bei Problemen

Bei Fragen oder Problemen können Sie:

1. Ein [Issue im Repository öffnen](https://github.com/Schachverein-Dresden-Striesen/Vereins-Wiki/issues/new) – beschreiben Sie Ihr Problem kurz auf Deutsch.
2. Den Vorstand kontaktieren: [info@sv-dresden-striesen.de](mailto:info@sv-dresden-striesen.de)

---

*Viel Erfolg beim Beitragen zum Vereins-Wiki! Jeder Beitrag – egal wie klein – hilft dabei, unsere Vereinsgeschichte lebendig zu halten.* ♟️

[← Zurück zur Startseite]({{ site.baseurl }}/)
