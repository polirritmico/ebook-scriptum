#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.scriptorium import Scriptorium


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="acceptance-test-") as tmp:
        yield Path(tmp)


def test_simple_text_export(tmp_dir) -> None:
    expected = "domingo"
    output_file = tmp_dir / "test_simple_text_export.txt"
    case = {
        "input": "tests/files/simple_translation.txt",
        "output": output_file,
        "selection": ["*"],
        "transmuter": ("OllamaTranslator", ""),
        "importer": "SimpleTextImporter",
        "exporter": "SimpleTextExporter",
    }

    scriptum = Scriptorium()
    scriptum.setup(case)
    scriptum.load_data()
    scriptum.transmute()
    scriptum.export()

    assert output_file.exists()
    assert output_file.is_file()
    assert expected in output_file.read_text().lower()
