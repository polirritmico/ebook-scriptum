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
    with TemporaryDirectory(dir="tests/files/", prefix="acceptance-test-") as tmp:
        yield Path(tmp)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_audio_processor(tmp_dir):
    case = ["TOC.xhtml", "Section0001.xhtml"]
    log_file = tmp_dir / "logs"
    expected1 = tmp_dir / "02. Chapter 1.mp3"
    expected2 = tmp_dir / "01. Índice de contenido.mp3"

    opts = {
        "input": "tests/files/simple_ebook.epub",
        "output": tmp_dir,
        "selection": case,
        "transmuter": ("CoquiTTS", "ModelVittsEs"),
        "importer": "EpubImporter",
        "exporter_opts": {"lang": "es", "log": log_file},
    }

    scriptum = Scriptorium()
    scriptum.setup(opts)
    scriptum.load_data()
    scriptum.transmute()
    scriptum.export()

    assert expected1.exists()
    assert expected2.exists()
    assert expected1.is_file()
    assert expected2.is_file()
    assert expected1.stat().st_size > 0
    assert expected2.stat().st_size > 0


# @pytest.mark.skip(reason="Slow execution")
def test_tts_ebook_to_wav(tmp_dir) -> None:
    case = ["Section0001.xhtml"]
    expected = tmp_dir / "02. Chapter 1.wav"

    word_dict = {
        "Chapter": "Capítulo",
        "This is a basic paragraph.": "Esto es un párrafo sencillo.",
    }
    opts = {
        "input": "tests/files/simple_ebook.epub",
        "output": tmp_dir,
        "selection": case,
        "transmuter": ("CoquiTTS", "ModelVittsEs"),
        "importer": "EpubImporter",
        "exporter_opts": {
            "lang": "es",
            "log": tmp_dir / "logs",
            "keep_wav": True,
            "word_dict": word_dict,
        },
    }

    scriptum = Scriptorium()
    scriptum.setup(opts)
    scriptum.load_data()
    scriptum.transmute()
    scriptum.export()

    assert expected.exists()
    assert expected.is_file()
    assert expected.stat().st_size > 0


# @pytest.mark.skip(reason="Slow execution")
def test_translate_full_ebook(tmp_dir) -> None:
    expected = tmp_dir / "output.epub"
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": expected,
        "selection": ["Section0001.xhtml"],
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

    assert expected.exists()
    assert expected.is_file()
    assert expected.stat().st_size > 0


def test_epub_to_txt(tmp_dir) -> None:
    case = ["*"]
    expected = tmp_dir / "output.txt"
    opts = {
        "input": "tests/files/simple_ebook.epub",
        "output": expected,
        "selection": case,
        "transmuter": ("DummyTransmuter", ""),
        "importer": "EpubImporter",
        "exporter": "SimpleTextExporter",
    }

    scriptum = Scriptorium()
    scriptum.setup(opts)
    scriptum.load_data()
    scriptum.transmute()
    scriptum.export()

    assert expected.exists()
    assert expected.is_file()
    assert expected.stat().st_size > 0
