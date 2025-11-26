#!/usr/bin/env bash
set -euo pipefail

# remove_webhook.sh
# Removes the webhook by setting an empty URL.

usage() {
  cat <<EOF
Usage: $0

Environment:
  BOT_TOKEN or TELEGRAM_TOKEN must be set, otherwise you will be prompted.
EOF
}

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

API="https://api.telegram.org/bot${TOKEN}/setWebhook"

echo 'Removing webhook (setting empty URL) ...'
curl -sS -X POST "$API" -d "url=" | jq

# Show getWebhookInfo
curl -sS "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | jq
