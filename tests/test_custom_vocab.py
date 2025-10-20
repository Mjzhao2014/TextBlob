"""Tests for domain-specific vocabulary preservation in TextBlob."""

import logging
from pathlib import Path

import pytest

import textblob.blob as blob_module
from textblob.blob import TextBlob, load_vocab_file


@pytest.fixture(autouse=True)
def clear_vocab_cache():
    """Ensure the vocabulary cache is isolated per test."""
    load_vocab_file.cache_clear()
    yield
    load_vocab_file.cache_clear()


def test_correct_preserves_vocab_words_case_insensitive(tmp_path, monkeypatch):
    """Words listed in the custom vocabulary file stay untouched by ``correct``."""
    vocab_path = tmp_path / "domain_vocab.txt"
    vocab_path.write_text("xray\n", encoding="utf-8")

    def fake_correct(self):
        return blob_module.Word(f"{self.string}_fixed")

    monkeypatch.setattr(blob_module.Word, "correct", fake_correct)

    blob = TextBlob("xray xraay Xray XRAY", custom_vocab_file=str(vocab_path))
    corrected_blob = blob.correct()

    assert corrected_blob.raw == "xray xraay_fixed Xray XRAY"
    assert corrected_blob.vocab_words == {"xray"}
    assert corrected_blob.custom_vocab_file == str(vocab_path)

    sentence = corrected_blob.sentences[0]
    assert sentence.vocab_words == {"xray"}
    assert sentence.custom_vocab_file == str(vocab_path)


def test_load_vocab_file_uses_lru_cache(tmp_path, monkeypatch):
    """Confirm the helper reuses cached vocabularies to avoid duplicate reads."""
    vocab_path = tmp_path / "medical_terms.txt"
    vocab_path.write_text("angiogram\n", encoding="utf-8")

    call_count = 0
    real_open = open

    def counting_open(file_path, *args, **kwargs):
        nonlocal call_count
        call_count += 1
        return real_open(file_path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", counting_open)

    first_load = load_vocab_file(str(vocab_path))
    second_load = load_vocab_file(str(vocab_path))

    assert call_count == 1
    assert first_load == {"angiogram"}
    assert second_load == {"angiogram"}


def test_load_vocab_file_logs_errors(tmp_path, caplog):
    """Errors encountered while reading vocab files are logged and handled."""
    missing_path = tmp_path / "missing_terms.txt"

    with caplog.at_level(logging.ERROR):
        vocab = load_vocab_file(str(missing_path))

    assert vocab == set()
    assert any(
        "Failed to load vocabulary file" in message for message in caplog.messages
    )
