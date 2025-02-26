#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path

from src.importers.simple_text import SimpleTextImporter
from src.models.vitts import ModelVitts
from src.transmuters.coqui_tts import CoquiTTS


def test_foo() -> None:
    case_file = Path("tests/files/simple.txt")

    text = SimpleTextImporter()
    text.load_data(case_file)
    doc = text.generate_document()
    tts = CoquiTTS()

    model = ModelVitts()

    tts.set_model(model)
    tts.transmute(doc)
