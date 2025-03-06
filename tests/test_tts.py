#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from src.importers.simple_text import SimpleTextImporter
from src.models.vitts_es import ModelVittsEs
from src.transmuters.coqui_tts import CoquiTTS


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_tts_acceptance() -> None:
    case_file = Path("tests/files/simple.txt")
    output_dir = Path("tests/files/outputs/audios")
    outfile = output_dir / "simple.wav"
    outfile.unlink(missing_ok=True)  # clean old execution output
    outfile.with_suffix(".mp3").unlink(missing_ok=True)

    case_opts = {
        "vitts": {
            "lang": "es",
            "log": True,
        },
        # TODO: is this used? change to output_dir?
        "output_file": output_dir,
    }

    text = SimpleTextImporter()
    text.load_data(case_file)
    doc = text.generate_document()

    tts = CoquiTTS()
    model = ModelVittsEs()
    tts.set_model(model)
    tts.set_options(case_opts)
    tts.transmute(doc)
    tts.export(output_dir)

    assert outfile.exists()
    assert outfile.is_file()
    assert outfile.stat().st_size > 0, "mp3 file should not be an empty file"
    outfile.with_suffix(".mp3")
    assert outfile.exists()
    assert outfile.is_file()
    assert outfile.stat().st_size > 0, "wav file should not be an empty file"
