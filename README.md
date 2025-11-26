[![CI](https://github.com/hentschel873-cyber/Python/actions/workflows/ci.yml/badge.svg)](https://github.com/hentschel873-cyber/Python/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-unknown-lightgrey.svg)](https://github.com/hentschel873-cyber/Python/actions/workflows/ci.yml)
 # Beispiel: `main.py` - Offline Update-Tests

Dieses Repository enthält ein kleines Beispielskript `main.py` mit einer optionalen
Telegram-Handler-Demo. Zusätzlich gibt es Offline-Test-JSONs, mit denen du
simulieren kannst, wie die Handler auf Updates reagieren, ohne einen echten Bot
zu starten.

Dateien

- `main.py` — Hauptskript. Unterstützt `--process-update <path>` zum Laden einer JSON-Datei mit einer serialisierten Telegram-`Update`-Struktur.
- `example_inline.json` — Beispiel für eine Inline-Query: `{ "inline_query": { "query": "hallo welt" } }`
- `example_message_start.json` — Beispiel für eine `/start`-Nachricht mit `username`.
- `example_message_no_username.json` — Beispiel für eine `/start`-Nachricht ohne `username` (zeigt Benennung über `first_name`).

Nutzung

- Offline-Simulation einer Inline-Query:

```powershell
python .\main.py --process-update .\example_inline.json
```

- Offline-Simulation einer `/start`-Nachricht:

```powershell
python .\main.py --process-update .\example_message_start.json
python .\main.py --process-update .\example_message_no_username.json
```

Entwicklungs-Setup
------------------

Empfohlene Schritte zum Einrichten der Entwicklungsumgebung und der CI-Checks:

```powershell
# Virtuelle Umgebung aktivieren (PowerShell)
. .\.venv\Scripts\Activate.ps1

# Dev-Abhängigkeiten installieren
python -m pip install -r requirements-dev.txt

# Pre-commit Hooks einmal lokal installieren
pre-commit install

# Tests, Lint und Typprüfung lokal laufen lassen
python -m pytest -q
python -m flake8 --exclude=.venv .
python -m mypy .

# Coverage erzeugen (HTML-Bericht in 'htmlcov')
python -m coverage run -m pytest
python -m coverage report -m
python -m coverage html

# Abhängigkeits-Sicherheitsscan
python -m pip_audit
```

Echtes Bot-Running

- Um den Beispiel-Bot wirklich zu starten, installiere `python-telegram-bot` (z. B.):

```powershell
pip install python-telegram-bot
```

- Dann starte mit:

```powershell
python .\main.py --run-bot --token <DEIN_TOKEN>
```

Hinweis

- Die `--process-update`-Option führt nur eine Offline-Simulation durch und ruft
  keine echten `telegram.Update`-Objekte oder die asynchronen Handler der
  Bibliothek auf. Wenn du möchtest, kann ich `main.py` erweitern, sodass bei
  installiertem `python-telegram-bot` echte `Update`-Objekte konstruiert und die
  Handler direkt ausgeführt werden.

Merge-Policy / Branch Protection
-------------------------------

Empfehlung für Repository-Schutzregeln (konfiguriere unter GitHub -> Settings -> Branches):

- Require pull request reviews before merging (1 reviewer mindestens).
- Require status checks to pass before merging: aktiviere `CI` (pytest), `flake8` und `mypy`.
- Optional: Enable "Require branches to be up to date before merging".
- Optional: Restrict who can push to `main` (z. B. nur Maintainer).

Wenn du möchtest, kann ich ein Issue erstellen oder per API diese Regeln setzen (benötigt Token/Permissions).
