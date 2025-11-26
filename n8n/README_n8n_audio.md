# n8n: Audio track example (TTS → Telegram)

Dieses Verzeichnis enthält ein Beispiel‑Workflow (JSON) für n8n, das Text entgegennimmt, zu einem TTS‑Service schickt, die zurückgegebene Audiodatei als Binary speichert und anschließend an `Telegram Send Audio` übergibt.

Import / Verwendung
- Öffne n8n, gehe zu "Workflows" → "Import" und lade `n8n/workflows/audio_tts_telegram.json`.
- Fülle in dem `TTS HTTP Request` Node die echte TTS‑URL und `Authorization` (API‑Key).
- Konfiguriere die `Telegram` Node Credentials in n8n (Bot Token).
- Der Webhook‑Trigger wartet auf POSTs an `/webhook/tts-audio` (oder aktiviere und kopiere die URL aus n8n).

Payload Beispiele
- POST JSON-Beispiel an den Webhook:

```
{
  "text": "Hallo, das ist eine Sprachprobe.",
  "chatId": "123456789"
}
```

Hinweise zum Binary-Mapping
- `TTS HTTP Request` ist so konfiguriert, dass der Node die Antwort als Datei/Binary erwartet (Response Format = `file`).
- `Move Binary Data` benennt die Binary-Eigenschaft `data` → `audioFile` um. Viele n8n File‑/Upload‑Nodes (z. B. `Telegram Send Audio` oder `Respond to Webhook`) erwarten den Binary‑Property‑Namen; stelle sicher, dass `audioFile` dort eingetragen ist.

Wenn du statt TTS eine existierende Audio‑URL verwenden willst
- Ersetze den `TTS HTTP Request` Node durch einen `HTTP Request` Node mit `GET` und `Response Format = file`.

Wenn dein Ziel ein `Respond to Webhook` ist
- Tausche die `Telegram Send Audio` Node gegen `Respond to Webhook`. In `Respond to Webhook` → `Binary` wähle die `audioFile` aus, um die Datei zurückzugeben.

Fragen / Anpassungen
- Sag mir, welchen TTS‑Provider du nutzen willst (ElevenLabs, Google, Azure, Amazon Polly), dann passe ich das HTTP‑Request‑Template und die erforderlichen Header/Body‑Feldern an.
