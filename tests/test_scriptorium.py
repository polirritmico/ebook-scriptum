#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.importers.simple_text import SimpleTextImporter
from src.scriptorium import Scriptorium
from src.transmuters.translator import Translator


def test_load_config_json() -> None:
    case = "tests/files/config.json"
    expected_lang = "es"
    expected_input = Path("tests/files/simple.txt")
    expected_importer = SimpleTextImporter
    expected_transmuters = [Translator]

    scriptum = Scriptorium()
    scriptum.set_options(case)
    output = scriptum.options

    assert expected_lang == output.get("lang")
    assert expected_input == output.get("input")
    assert expected_importer == output.get("importer")

    transmuters_generator = zip(expected_transmuters, output.get("transmuters"))
    for exp_transmuter, out_transmuter in transmuters_generator:
        assert out_transmuter is exp_transmuter
