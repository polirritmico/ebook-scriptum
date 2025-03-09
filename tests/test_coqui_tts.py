#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.importers.simple_text import SimpleTextImporter
from src.models.vitts_es import ModelVittsEs
from src.transmuters.coqui_tts import CoquiTTS


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="tts-test-") as tmp:
        yield Path(tmp)


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
