import re
import types

from main import get_mention_text, get_python_version, main


def test_get_mention_with_username():
    user = types.SimpleNamespace(username="max", first_name="Max", id=1)
    assert get_mention_text(user) == "@max"


def test_get_mention_without_username():
    user = types.SimpleNamespace(username=None, first_name="Anna", id=67890)
    assert get_mention_text(user) == "[Anna](tg://user?id=67890)"


def test_get_python_version_format():
    ver = get_python_version()
    # basic check: digits.digits.digits
    assert re.match(r"^\d+\.\d+\.\d+", ver)


def test_main_prints(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hallo! Python ist erfolgreich in VS Code konfiguriert!" in captured.out
    assert "Python Version:" in captured.out
