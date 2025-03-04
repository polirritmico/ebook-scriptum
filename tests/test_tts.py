#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from src.importers.simple_text import SimpleTextImporter
from src.models.vitts_es import ModelVittsEs
from src.transmuters.coqui_tts import CoquiTTS


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_foo() -> None:
    case_file = Path("tests/files/simple.txt")
    output_file = Path("tests/files/outputs/tts_out.wav")
    case_opts = {
        "vitts": {
            "lang": "es",
            "log": None,
        },
        "output_file": output_file,
    }
    output_file.unlink(missing_ok=True)  # clean old execution output

    text = SimpleTextImporter()
    text.load_data(case_file)
    doc = text.generate_document()

    tts = CoquiTTS()
    model = ModelVittsEs()
    tts.set_model(model)
    tts.set_options(case_opts)
    tts.transmute(doc)
    tts.export(output_file)

    assert output_file.exists()
    assert output_file.is_file()
    assert output_file.stat().st_size > 0, "Output should not be an empty file"
