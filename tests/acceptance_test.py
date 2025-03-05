#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.scriptorium import Scriptorium


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="acceptance-test_") as tmp:
        yield tmp


# @pytest.mark.skip(reason="Slow execution")
def test_tts_ebook_to_wav(tmp_dir) -> None:
    expected_file = Path("tests/files/outputs/tts_test/Section0001.wav")
    case = {
        "input": "tests/files/simple_ebook.epub",
        # "selection": ["Section0001.xhtml"],
        "output": "tests/files/outputs/tts_test/",
        "transmuter": ("CoquiTTS", "ModelVittsEs"),
        "importer": "EpubImporter",
        "exporter_opts": {
            "lang": "es",
            "log": None,
        },
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
