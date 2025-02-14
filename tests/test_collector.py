#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.collector import Collector
from src.importers.epub import EpubImporter
from src.transmuters.ollama_translator import OllamaTranslator


def test_collect_model() -> None:
    case = "ModelQwen"

    collector = Collector()
    output = collector.collect_model_handler(case)

    assert case == output.__name__


def test_collect_config_in_directory() -> None:
    case = "tests/files/"
    expected_lang = "es"
    expected_input = "tests/files/simple.txt"

    collector = Collector()
    output = collector.collect_options(case)
    output_metadata = output.get("metadata")

    assert expected_input == output.get("input")
    assert expected_lang == output_metadata.get("lang")
    assert output.get("importer")
    assert output.get("transmuters")


def test_load_transmuter_from_config_json() -> None:
    case_name = "OllamaTranslator"
    case_path = "src.transmuters"
    expected = OllamaTranslator

    collector = Collector()
    output = collector.collect_handler(case_name, case_path)

    assert output is expected


def test_load_importer_from_config_json() -> None:
    case_name = "EpubImporter"
    case_path = "src.importers"
    expected = EpubImporter

    collector = Collector()
    output = collector.collect_handler(case_name, case_path)

    assert output is expected
