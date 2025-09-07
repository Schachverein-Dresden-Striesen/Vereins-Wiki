# Vereins-Wiki - Schachverein Dresden-Striesen e.V.

Diese Website wird mit GitHub Pages und Jekyll erstellt und automatisch bereitgestellt. Sie enthält alle notwendigen Dateien und Konfigurationen für die automatische Veröffentlichung bei Änderungen.

## Projektstruktur

- **index.md**: Hauptseite der Website
- **pages/**: Inhaltsseiten des Vereins
- **files/**: Dateien, Bilder und Dokumente
- **_config.yml**: Jekyll-Konfiguration für GitHub Pages
- **.devcontainer/**: Entwicklungsumgebung für VSCode

## Lokale Entwicklung

### Voraussetzungen

**Für beide Optionen:**
- [Git](https://git-scm.com/)

**Option 1 (empfohlen):**
- [VSCode](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/)

**Option 2:**
- Ruby (Version 2.7 oder höher)
  - Windows: [RubyInstaller](https://rubyinstaller.org/)
  - macOS: `brew install ruby` (mit [Homebrew](https://brew.sh/))
  - Linux: Paketmanager Ihrer Distribution verwenden

### Setup

1. **Repository klonen**:
   ```bash
   git clone https://github.com/Schachverein-Dresden-Striesen/Vereins-Wiki.git
   cd Vereins-Wiki
   ```

2. **Entwicklungsumgebung wählen:**

   **Option A: VSCode mit Devcontainer (empfohlen)**
   ```bash
   code .
   ```
   - VSCode wird automatisch vorschlagen, den Container zu öffnen
   - Oder: `F1` → "Dev Containers: Reopen in Container"
   - Abhängigkeiten werden automatisch installiert

   **Option B: Lokale Installation**
   ```bash
   gem install bundler
   bundle install
   ```

3. **Website starten**:
   ```bash
   # Für lokale Entwicklung (empfohlen - vermeidet Baseurl-Probleme):
   bundle exec jekyll serve --baseurl ""
   
   # Oder mit Standard-Konfiguration:
   bundle exec jekyll serve
   ```

Die Website ist dann unter `http://localhost:4000` erreichbar.

### Inhalte bearbeiten

**Lokale Entwicklung:**
- Bearbeiten Sie Markdown-Dateien (`.md`) in VSCode oder Ihrem bevorzugten Editor
- Änderungen werden automatisch beim Speichern übernommen (Live-Reload)

**Direkt in GitHub:**
- Dateien können direkt über die GitHub-Weboberfläche bearbeitet werden
- Besonders praktisch für schnelle Textänderungen ohne lokale Entwicklungsumgebung
- Änderungen werden automatisch als Commit gespeichert

**Neue Inhalte:**
- Neue Seiten können im `pages/` Verzeichnis erstellt werden

### Deployment

Änderungen werden automatisch über GitHub Actions veröffentlicht, wenn sie in den `website`-Branch gepusht werden.

## Mitwirkung

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue für Vorschläge oder Verbesserungen.

