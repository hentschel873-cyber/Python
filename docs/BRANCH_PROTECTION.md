Branch Protection — Anleitung

Ziel
----
Diese Anleitung erklärt, wie du Branch Protection (Schutzregel) für den Branch `main` aktivierst.

Option A — Per GUI (empfohlen, sofort ausführbar)
1. Öffne das Repository auf GitHub.
2. Gehe zu `Settings` → `Branches` → `Add rule`.
3. Setze `Branch name pattern` auf `main`.
4. Aktiviere:
   - "Require pull request reviews before merging" (setze mindestens 1 Review required)
   - "Require status checks to pass before merging" und wähle `CI` aus
   - Optional: "Include administrators" (erzwungen für Admins)
5. Speichern.

Option B — Per CLI / API (nützlich zur Automatisierung)
Hinweis: Für private Repositories kann GitHub das Setzen per API einschränken (geht nur bei bestimmten Account/Plan-Einstellungen). Wenn die API fehlschlägt, nutze die GUI (Option A).

PowerShell (gh CLI) — Beispiel für lokale Ausführung:

```powershell
# Voraussetzungen:
# - gh (GitHub CLI) ist installiert und eingeloggt
# - Repo ist öffentlich ODER dein Account/Org unterstützt branch-protection via API

$body = @{
  required_status_checks = @{ strict = $true; contexts = @("CI") }
  enforce_admins = $true
  required_pull_request_reviews = @{ dismiss_stale_reviews = $true; require_code_owner_reviews = $false; required_approving_review_count = 1 }
} | ConvertTo-Json -Depth 5

gh api --method PUT /repos/hentschel873-cyber/Python/branches/main/protection -f "$body"
```

Wenn die API auf einen 403/Planfehler läuft, folge Option A oder ändere die Repository-Sichtbarkeit.

Weiteres
------
- Wenn du möchtest, kann ich dieses Skript in das Repo einfügen und einen PR öffnen (bereitgestellt in `scripts/enable-branch-protection.ps1`).
- Das Skript ist nur ein Convenience-Wrapper; die eigentliche Berechtigung/Plan muss auf deiner Seite passen.
