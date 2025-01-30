#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.catalyst_collector import CatalystCollector
from src.importers.epub import EpubImporter
from src.transmuters.translator import Translator


def test_collect_config_in_directory() -> None:
    case = "tests/files/"
    expected_lang = "es"
    expected_input = "tests/files/simple.txt"

    collector = CatalystCollector()
    output = collector.collect_options(case)

    assert expected_lang == output.get("lang")
    assert expected_input == output.get("input")
    assert output.get("importer")
    assert output.get("transmuters")


def test_load_transmuter_from_config_json() -> None:
    case_name = "Translator"
    case_path = "src.transmuters"
    expected = Translator

    collector = CatalystCollector()
    output = collector.collect_handler(case_name, case_path)

    assert output is expected


def test_load_importer_from_config_json() -> None:
    case_name = "EpubImporter"
    case_path = "src.importers"
    expected = EpubImporter

    collector = CatalystCollector()
    output = collector.collect_handler(case_name, case_path)

    assert output is expected
