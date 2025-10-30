import json

from gramartico import RealTimeWritingAssistant


def _analyse(text: str):
    assistant = RealTimeWritingAssistant()
    return assistant.analyse(text)


def test_detects_repeated_words():
    suggestions = _analyse("This is is a test.")
    assert any("Repeated word" in item.message for item in suggestions)


def test_detects_common_typos():
    suggestions = _analyse("We recieved the letter.")
    assert any("Did you mean" in item.message for item in suggestions)


def test_detects_missing_terminal_punctuation():
    suggestions = _analyse("This sentence lacks punctuation")
    assert suggestions[-1].message.startswith("Add terminal punctuation")


def test_json_serialisation_round_trip():
    suggestions = _analyse("teh end")
    encoded = json.dumps([item.as_dict() for item in suggestions])
    decoded = json.loads(encoded)
    assert decoded[0]["replacements"][0] == "the"
