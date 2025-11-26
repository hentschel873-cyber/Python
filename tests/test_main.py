import json
from pathlib import Path
from typing import Any, cast

from main import process_update_data


def load_json(name: str) -> dict[str, Any]:
    p = Path(__file__).parent.parent / name
    # json.loads returns Any; cast to a mapping for stricter typing checks
    return cast(dict[str, Any], json.loads(p.read_text(encoding="utf-8")))


def test_inline_query_outputs(capsys):
    data = load_json("example_inline.json")
    process_update_data(data)
    captured = capsys.readouterr()
    assert "InlineQuery erkannt" in captured.out
    assert "HALLO WELT" in captured.out
    assert "hallo welt" in captured.out


def test_start_with_username(capsys):
    data = load_json("example_message_start.json")
    process_update_data(data)
    captured = capsys.readouterr()
    assert "Message erkannt. Text: /start" in captured.out
    assert "Würde antworten: Hallo @max" in captured.out


def test_start_without_username(capsys):
    data = load_json("example_message_no_username.json")
    process_update_data(data)
    captured = capsys.readouterr()
    assert "Message erkannt. Text: /start" in captured.out
    assert "Würde antworten: Hallo [Anna](tg://user?id=67890)" in captured.out
