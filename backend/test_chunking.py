
from app.chunking import chunk_text


def test_empty_text():
    assert chunk_text("") == []


def test_short_text():
    assert chunk_text("Hello document") == ["Hello document"]


def test_long_text():
    text = "This is a sample sentence. " * 100
    chunks = chunk_text(text)

    assert len(chunks) > 1
    assert all(len(chunk) <= 500 for chunk in chunks)
