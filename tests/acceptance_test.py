#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.scriptorium import Scriptorium

# HACK: to avoid anoying warning messages: https://github.com/ROCm/MIOpen/issues/2981
os.environ["MIOPEN_LOG_LEVEL"] = "3"


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="acceptance-test_") as tmp:
        yield tmp


# @pytest.mark.skip(reason="Slow execution")
def test_tts_ebook_to_wav(tmp_dir) -> None:
    expected_file = Path("tests/files/outputs/tts_test/Chapter 1.wav")
    expected_file.unlink(missing_ok=True)
    word_dict = {
        "Chapter": "Capítulo",
        "This is a basic paragraph.": "Esto es un párrafo sencillo.",
    }
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/outputs/tts_test/",
        "transmuter": ("CoquiTTS", "ModelVittsEs"),
        "importer": "EpubImporter",
        "exporter_opts": {
            "lang": "es",
            "log": "tests/files/outputs/tts_test/log",
            "keep_wav": True,
            "word_dict": word_dict,
        },
        "selection": ["Section0001.xhtml"],
    }

    scriptum = Scriptorium()
    scriptum.setup(case)
    scriptum.load_data()
    scriptum.transmute()
    scriptum.export()

    assert expected_file.exists()
    assert expected_file.is_file()
    assert expected_file.stat().st_size > 0


# @pytest.mark.skip(reason="Slow execution")
def test_translate_full_ebook(tmp_dir) -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output.epub",
        "transmuter": ("OllamaTranslator", ""),
        "importer": "EpubImporter",
        "exporter": "EpubExporter",
    }

    scriptum = Scriptorium()
    scriptum.setup(case)
    scriptum.load_data()
    scriptum.transmute()
    # scriptum.validate_output()
    scriptum.export()


def test_epub_to_txt() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "output.txt",
        "transmuter": ("DummyTransmuter", ""),
        "importer": "EpubImporter",
        "exporter": "SimpleTextExporter",
    }

    scriptum = Scriptorium()
    scriptum.setup(case)
    scriptum.load_data()
    scriptum.export()
