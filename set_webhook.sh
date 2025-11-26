#!/usr/bin/env bash
set -euo pipefail

# set_webhook.sh
# Setzt einen Telegram-Webhook. Versucht, ngrok zu erkennen (http://127.0.0.1:4040).

usage() {
  cat <<EOF
Usage: $0 [-u url] [-s secret]

Options:
  -u URL     Public HTTPS URL to set as webhook (e.g. https://xyz.ngrok.io/telegram)
  -s SECRET  Optional secret token for webhook verification
EOF
}

URL=""
SECRET=""
while getopts ":u:s:h" opt; do
  case ${opt} in
    u) URL="$OPTARG" ;;
    s) SECRET="$OPTARG" ;;
    h) usage; exit 0 ;;
    *) usage; exit 1 ;;
  esac
done

# Detect token
if [ -n "${BOT_TOKEN-}" ]; then
  TOKEN="$BOT_TOKEN"
elif [ -n "${TELEGRAM_TOKEN-}" ]; then
  TOKEN="$TELEGRAM_TOKEN"
else
  read -r -p "BOT_TOKEN nicht gesetzt. Bitte Token eingeben: " TOKEN
  if [ -z "$TOKEN" ]; then
    echo "Kein Token angegeben. Abbruch." >&2
    exit 1
  fi
fi

# Try detect ngrok
if [ -z "$URL" ]; then
  if command -v curl >/dev/null 2>&1; then
    NGROK_URL=$(curl -sS http://127.0.0.1:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[]?.public_url' 2>/dev/null | grep '^https' | head -n1 || true)
    if [ -n "$NGROK_URL" ]; then
      URL="$NGROK_URL"
      echo "Gefundener ngrok-Tunnel: $URL"
    fi
  fi
fi

if [ -z "$URL" ]; then
  read -r -p "Bitte die öffentliche HTTPS-URL eingeben (z.B. https://xyz.ngrok.io/telegram): " URL
  if [ -z "$URL" ]; then
    echo "Keine URL angegeben. Abbruch." >&2
    exit 1
  fi
fi

if [[ "$URL" != https:* ]]; then
  echo "Warnung: URL scheint nicht HTTPS zu sein: $URL" >&2
fi

# Build curl data
DATA=( -d "url=$URL" )
if [ -n "$SECRET" ]; then
  DATA+=( -d "secret_token=$SECRET" )
fi

API="https://api.telegram.org/bot${TOKEN}/setWebhook"

echo "Setting webhook to $URL ..."
if curl -sS -X POST "$API" "${DATA[@]}" | jq -r '.ok, .description' >/dev/null 2>&1; then
  curl -sS -X POST "$API" "${DATA[@]}" | jq
else
  echo "Fehler beim Aufruf von setWebhook" >&2
  curl -sS -X POST "$API" "${DATA[@]}"
  exit 1
fi

# Show getWebhookInfo
curl -sS "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | jq
