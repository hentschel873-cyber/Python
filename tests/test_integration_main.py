import sys
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_main_with(example_filename: str) -> tuple[int, str]:
    """Run `main.py --process-update <example>` and return
    (returncode, stdout+stderr).
    """
    exe = sys.executable
    p = subprocess.run(
        [
            exe,
            str(ROOT / "main.py"),
            "--process-update",
            str(ROOT / example_filename),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return p.returncode, p.stdout + p.stderr


def test_example_inline():
    rc, out = run_main_with("example_inline.json")
    assert rc == 0
    assert "InlineQuery erkannt" in out
    assert "HALLO WELT" in out
    assert "Python Version" in out


def test_example_message_no_username():
    rc, out = run_main_with("example_message_no_username.json")
    assert rc == 0
    assert "Message erkannt" in out
    assert "/start" in out
    assert "Hallo [Anna]" in out or "Hallo [Anna](tg://user?id=67890)" in out


def test_example_message_start():
    rc, out = run_main_with("example_message_start.json")
    assert rc == 0
    assert "Message erkannt" in out
    assert "/start" in out
    assert "Hallo @max" in out
