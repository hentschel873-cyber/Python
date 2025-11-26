import json

from main import process_update_data


def test_process_update_offline_minimal():
    # Passing an empty dict (no telegram library) should not raise
    process_update_data({})


def test_process_example_inline():
    # Use provided example payload to exercise inline-processing path
    with open("example_inline.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
    process_update_data(data)


def test_process_example_start():
    with open("example_message_start.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
    process_update_data(data)
