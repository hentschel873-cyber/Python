Webhook-Skripte
================

Kurz: Zwei PowerShell-Skripte wurden hinzugefügt: `set_webhook.ps1` und `remove_webhook.ps1`.
Zusätzlich gibt es POSIX-kompatible Shell-Skripte `set_webhook.sh` und `remove_webhook.sh`.

PowerShell (Windows)

- Setzen des Webhooks (versucht ngrok zu erkennen oder fragt nach einer URL):

  ```powershell
  .\set_webhook.ps1
  ```

  Optional:
  ```powershell
  .\set_webhook.ps1 -Url 'https://xyz.ngrok.io/telegram' -Secret 'mein-secret'
  ```

- Entfernen des Webhooks:

  ```powershell
  .\remove_webhook.ps1
  ```

Shell (Linux / macOS / WSL)

- Setzen des Webhooks (versucht ngrok zu erkennen oder fragt nach einer URL):

  ```bash
  ./set_webhook.sh
  ```

  Optional:

  ```bash
  ./set_webhook.sh -u https://xyz.ngrok.io/telegram -s mein-secret
  ```

- Entfernen des Webhooks:

  ```bash
  ./remove_webhook.sh
  ```

Token-Handling

- Die Skripte verwenden zuerst die Umgebungsvariable `BOT_TOKEN`, falls gesetzt. Falls nicht vorhanden, wird `TELEGRAM_TOKEN` verwendet. Falls keine Variable gesetzt ist, wird interaktiv nach dem Token gefragt.

Hinweis

- Achte darauf, dass die öffentliche URL mit HTTPS beginnt (Telegram verlangt HTTPS für Webhooks).
- Die Shell-Skripte benötigen `curl` und `jq`.
