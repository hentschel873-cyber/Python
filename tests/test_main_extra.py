from main import process_update_data


def test_inline_empty_query(capsys):
    data = {"inline_query": {"query": ""}}
    process_update_data(data)
    captured = capsys.readouterr()
    assert "InlineQuery erkannt, aber `query` ist leer oder fehlt." in captured.out


def test_message_not_start(capsys):
    data = {"message": {"from": {"username": "max"}, "text": "hello"}}
    process_update_data(data)
    captured = capsys.readouterr()
    assert "Message erkannt. Text: hello" in captured.out
    assert "Keine /start-Nachricht erkannt; keine Aktion simuliert." in captured.out


def test_no_inline_no_message(capsys):
    data = {"update_id": 12345}
    process_update_data(data)
    captured = capsys.readouterr()
    assert (
        "Weder `inline_query` noch `message` in der JSON-Datei gefunden."
        in captured.out
    )
