#!/usr/bin/env python3
"""Main Python script - Beispiel für ein Python‑Projekt

Dieses Skript hat zwei Funktionen:
- Die Standard‑Funktion `main()` zeigt die lokale Python‑Version an.
- Optionales Beispiel: sicherer Telegram Inline‑Query/Start‑Handler —
    dieser ist nur aktiv, wenn das Paket ``python-telegram-bot`` installiert
    ist und beim Start die Option ``--run-bot`` übergeben wird.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
from typing import Optional
from uuid import uuid4


def get_python_version() -> str:
    """Gibt die aktuelle Python-Version zurück."""
    import sys

    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def main() -> None:
    """Hauptfunktion: einfache Erfolgsmeldung und Python-Version."""
    print("Hallo! Python ist erfolgreich in VS Code konfiguriert!")
    print(f"Python Version: {get_python_version()}")


# Optional: Telegram bot example (only if package is installed)
try:
    from telegram import (InlineQueryResultArticle, InputTextMessageContent,
                          Update, User)
    from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                              InlineQueryHandler)

    _HAS_TELEGRAM = True
except Exception:
    _HAS_TELEGRAM = False


# Logging einrichten (hilft bei der Fehlersuche)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_mention_text(user: User) -> str:
    """Erstellt einen sicheren Mention-String für Markdown.

    Bevorzugt `@username`. Wenn kein Username vorhanden ist, wird
    der Vorname mit tg://user?id=... als Markdown-Link zurückgegeben.
    Namen werden minimal bereinigt, um Markdown-Syntaxfehler zu vermeiden.
    """

    if getattr(user, "username", None):
        return f"@{user.username}"

    clean_name = getattr(user, "first_name", "Nutzer").replace("[", "").replace("]", "")
    return f"[{clean_name}](tg://user?id={user.id})"


def process_update_data(data: dict) -> None:
    """Verarbeitet eine bereits geladene JSON-Update-Struktur.

    Diese Funktion ist importierbar und testbar. Sie versucht, wenn
    ``python-telegram-bot`` installiert ist, echte ``telegram.Update``-Objekte
    zu bauen und die asynchronen Handler aufzurufen; andernfalls führt sie
    die einfache Offline-Simulation aus.
    """

    # Versuche zuerst, die Daten mit python-telegram-bot zu handhaben.
    if _HAS_TELEGRAM and _try_process_with_telegram(data):
        return

    # Ansonsten Offline-Fallback
    _process_offline(data)


def _try_process_with_telegram(data: dict) -> bool:
    """Versucht, `telegram.Update` zu bauen und Handler aufzurufen.

    Gibt `True` zurück, wenn das Update verarbeitet wurde, sonst `False`.
    """

    try:
        import asyncio
        import types

        from telegram import Update as TgUpdate

        update_obj = TgUpdate.de_json(data, bot=None)

        inline_obj = getattr(update_obj, "inline_query", None)
        if inline_obj is not None:

            async def _print_answer(self, results):
                print("InlineQuery erkannt. Simulierte Antworten (real handler):")
                for r in results:
                    title = getattr(r, "title", "(kein Titel)")
                    desc = getattr(r, "description", "")
                    print(f"- {title}: {desc}")

            inline_obj.answer = types.MethodType(_print_answer, inline_obj)
            asyncio.run(inline_query(update_obj, None))
            return True

        msg = getattr(update_obj, "message", None)
        if msg is not None:

            async def _print_reply(self, text, **kwargs):
                print(f"Message erkannt (real handler). Würde antworten: {text}")

            msg.reply_text = types.MethodType(_print_reply, msg)
            asyncio.run(start(update_obj, None))
            return True

    except Exception as exc:
        print(f"Fehler beim Erzeugen/Verarbeiten von telegram.Update: {exc}")

    return False


def _process_offline(data: dict) -> None:
    """Einfache Offline-Simulation, wenn kein Telegram-Paket verfügbar."""

    inline = data.get("inline_query")
    if inline is not None:
        query = inline.get("query")
        if not query:
            print("InlineQuery erkannt, aber `query` ist leer oder fehlt.")
            return
        print("InlineQuery erkannt. Simulierte Antworten:")
        print(f"- Großbuchstaben: {query.upper()}")
        print(f"- Original: {query}")
        return

    message = data.get("message")
    if message is not None:
        from_user = message.get("from") or {}
        username = from_user.get("username")
        first_name = from_user.get("first_name") or "Nutzer"
        user_id = from_user.get("id", 0)
        mention = (
            f"@{username}" if username else f"[{first_name}](tg://user?id={user_id})"
        )
        text = message.get("text") or ""
        print(f"Message erkannt. Text: {text}")
        if text.strip().startswith("/start"):
            print(f"Würde antworten: Hallo {mention}, willkommen beim Bot!")
        else:
            print("Keine /start-Nachricht erkannt; keine Aktion simuliert.")
        return

    print("Weder `inline_query` noch `message` in der JSON-Datei gefunden.")


if _HAS_TELEGRAM:

    async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sichere Inline-Query-Behandlung.

        Verwendet `getattr` um `update.inline_query` zu prüfen und `query`
        optional zu lesen (vermeidet AttributeError bei falschen Updates).
        """

        inline = getattr(update, "inline_query", None)
        query: Optional[str] = getattr(inline, "query", None)
        if not query:
            # Keine Eingabe -> nichts senden
            return

        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Großbuchstaben",
                input_message_content=InputTextMessageContent(query.upper()),
                description=f"Sendet: {query.upper()}",
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Original (raw)",
                input_message_content=InputTextMessageContent(query),
                description=f"Sendet: {query}",
            ),
        ]

        # Wir benutzen die bereits sichere lokale Variable `inline` statt
        # direkt `update.inline_query`, damit ein möglicher `None`-Wert
        # vorher berücksichtigt ist (vermeidet Linter-/Typwarnungen).
        if inline:
            await inline.answer(results)

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start-Handler: erwähnt den Benutzer sicher (Markdown)."""

        user = update.effective_user
        mention = get_mention_text(user) if user else "Nutzer"
        if getattr(update, "message", None):
            await update.message.reply_text(f"Hallo {mention}!", parse_mode="Markdown")

    def run_bot(token: Optional[str]) -> None:
        """Startet den Beispiel-Bot, wenn ein Token vorhanden ist."""

        if not token:
            print("Kein Bot-Token angegeben.")
            print("Setze TELEGRAM_TOKEN oder übergebe --token.")
            return

        app = ApplicationBuilder().token(token).build()
        app.add_handler(InlineQueryHandler(inline_query))
        app.add_handler(CommandHandler("start", start))
        print("Bot läuft... (STRG+C zum Beenden)")
        app.run_polling()  # pragma: no cover


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-bot",
        action="store_true",
        help="Start the example Telegram bot",
    )
    parser.add_argument(
        "--process-update",
        type=str,
        default=None,
        help=(
            "Path to JSON file containing a serialized Telegram Update to "
            "process locally"
        ),
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="Bot token (overrides BOT_TOKEN or TELEGRAM_TOKEN env var)",
    )
    args = parser.parse_args()

    if args.process_update:
        # Wrapper: Datei lesen und an die exportierte Funktion übergeben
        try:
            with open(args.process_update, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:
            print(f"Fehler beim Lesen der Datei '{args.process_update}': {exc}")
            raise SystemExit(2)

        # Versuche, die importierbare Funktion `process_update_data` zu nutzen,
        # falls sie vorhanden (wird weiter unten definiert). Falls nicht, benutze
        # das vorhandene Inline-Fallback (sollte nicht vorkommen).
        try:
            process_update_data(data)
        except NameError:
            # Fallback: (alte Inline-Simulation)
            inline = data.get("inline_query")
            if inline is not None:
                query = inline.get("query")
                if not query:
                    print("InlineQuery erkannt, aber `query` ist leer oder fehlt.")
                else:
                    print("InlineQuery erkannt. Simulierte Antworten:")
                    print(f"- Großbuchstaben: {query.upper()}")
                    print(f"- Original: {query}")
                raise SystemExit(0)

            message = data.get("message")
            if message is not None:
                from_user = message.get("from") or {}
                username = from_user.get("username")
                first_name = from_user.get("first_name") or "Nutzer"
                user_id = from_user.get("id", 0)
                if username:
                    mention = f"@{username}"
                else:
                    mention = f"[{first_name}]" f"(tg://user?id={user_id})"
                text = message.get("text") or ""
                print(f"Message erkannt. Text: {text}")
                if text.strip().startswith("/start"):
                    print(f"Würde antworten: Hallo {mention}, willkommen beim Bot!")
                else:
                    print("Keine /start-Nachricht erkannt; keine Aktion simuliert.")
                raise SystemExit(0)

            print("Weder `inline_query` noch `message` in der JSON-Datei gefunden.")
            raise SystemExit(0)

    if args.run_bot:
        # Prefer `BOT_TOKEN` but allow the older `TELEGRAM_TOKEN` name for
        # backwards compatibility.
        token = args.token
        if not token:
            token = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
        if not _HAS_TELEGRAM:
            print(
                "Das Paket 'python-telegram-bot' ist nicht installiert. "
                "Installiere es mit: `pip install python-telegram-bot`"
            )
        else:
            run_bot(token)  # pragma: no cover
    else:
        main()
