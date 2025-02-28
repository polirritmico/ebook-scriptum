#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path

from src.scriptorium import Scriptorium


def test_simple_text_export() -> None:
    case_output_path = Path("tests/files/outputs/test_simple_text_export.txt")
    case = {
        "input": "tests/files/simple-translation.txt",
        "output": case_output_path,
        "transmuter": ("OllamaTranslator", ""),
        "importer": "SimpleTextImporter",
        "exporter": "SimpleTextExporter",
    }
    expected = "domingo"

    scriptum = Scriptorium()
    scriptum.setup(case)
    scriptum.load_data()
    scriptum.transmute()
    scriptum.export()
    output = case_output_path.read_text()

    assert expected in output.lower()
