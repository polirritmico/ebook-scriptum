#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.importers.simple_text import SimpleTextImporter
from src.models.vitts_en import ModelVittsEn
from src.models.vitts_es import ModelVittsEs
from src.transmuters.coqui_tts import CoquiTTS


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="tts-test-") as tmp:
        yield Path(tmp)


def test_paragraph_separation() -> None:
    case = Path("tests/files/simple_text_paragraph.txt")
    expected = "Title , This is a paragraph ,\n\nThis is another paragraph."

    importer = SimpleTextImporter()
    importer.load_data([case])
    document = importer.generate_document()

    tts = CoquiTTS()
    tts.set_model(ModelVittsEn())
    tts.set_options({})
    output = tts.process_text(document)

    output_file = next(iter(output))
    assert expected == output[output_file]


def test_text_processor(tmp_dir) -> None:
    case_file = Path("tests/files/text_processor.txt")
    case_opts = {
        "exporter_opts": {
            "log": tmp_dir,
            "lang": "es",
        },
    }

    text = SimpleTextImporter()
    text.load_data(case_file)
    document = text.generate_document()

    tts = CoquiTTS()
    model = ModelVittsEs()
    tts.set_model(model)
    tts.set_options(case_opts)
    tts.transmute(document)
    tts.export(tmp_dir)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_tts_acceptance(tmp_dir) -> None:
    case_file = Path("tests/files/simple.txt")
    expected_log = tmp_dir / "tts_log"
    expected1 = tmp_dir / "01. simple.wav"
    expected2 = tmp_dir / "01. simple.mp3"
    case_opts = {
        "text_processor_opts": {"lang": "es"},
        "keep_wav": True,
        "log": expected_log,
    }

    text = SimpleTextImporter()
    text.load_data(case_file)
    document = text.generate_document()

    tts = CoquiTTS()
    model = ModelVittsEs()
    tts.set_model(model)
    tts.set_options(case_opts)
    tts.transmute(document)
    tts.export(tmp_dir)

    assert expected1.exists()
    assert expected1.is_file()
    assert expected1.stat().st_size > 0, "wav file should not be an empty file"
    assert expected2.exists()
    assert expected2.is_file()
    assert expected2.stat().st_size > 0, "mp3 file should not be an empty file"

    assert any(expected_log.glob("*.txt")), f"No log files at '{expected_log}'"
