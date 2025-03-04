#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.configuration import ScriptoriumConfiguration
from src.importers.simple_text import SimpleTextImporter
from src.models.llama3_2 import ModelLlama3_2
from src.protocols import ImporterHandler, ModelHandler
from src.transmuters.ollama_translator import OllamaTranslator


def test_transmuter_and_importer_not_overwriten_by_config() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/mock.epub",
        "transmuter": ("OllamaTranslator", ""),
        "importer": "EpubImporter",
        "exporter": "EpubExporter",
    }

    case_importer = SimpleTextImporter()
    case_transmuter = OllamaTranslator()
    case_model = ModelLlama3_2()
    case_transmuter.set_model(case_model)

    config = ScriptoriumConfiguration()
    config.importer = case_importer
    config.transmuter = case_transmuter

    config.resolve_and_validate_opts(case)
    config.parse_options(case)
    out_transmuter = config.transmuter

    assert case_model is out_transmuter.model
    assert case_transmuter is out_transmuter
    assert case_importer is config.importer


def test_load_config_json() -> None:
    case = "tests/files/config.json"
    expected_lang = "es"
    expected_input = ["tests/files/simple.txt"]
    ExpectedImporter = SimpleTextImporter
    ExpectedTransmuter = OllamaTranslator
    ExpectedModel = ModelHandler

    config = ScriptoriumConfiguration()
    case = config.resolve_and_validate_opts(case)
    config.parse_options(case)

    for expected, output in zip(expected_input, config.input_file):
        assert expected == output.as_posix()
    assert expected_lang == config.metadata["lang"]
    assert isinstance(config.importer, ExpectedImporter)
    assert isinstance(config.transmuter, ExpectedTransmuter)
    assert isinstance(config.transmuter.model, ExpectedModel)


def test_minimal_keys_check_ok() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuter": "OllamaTranslator",
        "importer": "EpubImporter",
        "exporter": "EpubExporter",
    }
    config = ScriptoriumConfiguration()
    config.check_spec_compliance(case)


def test_minimal_keys_check_missing_input() -> None:
    case = {
        "output": "tests/files/output",
        "transmuter": "OllamaTranslator",
        "importer": "EpubImporter",
        "exporter": "EpubExporter",
    }
    with pytest.raises(ValueError) as error:
        config = ScriptoriumConfiguration()
        config.setup(case)

    expected = ("missing", "input")
    output_error = error.value.args[0]
    for expected_str in expected:
        assert expected_str in output_error.lower()


def test_config_without_exporter() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuter": "OllamaTranslator",
        "importer": "EpubImporter",
    }
    config = ScriptoriumConfiguration()
    config.check_spec_compliance(case)


def test_detect_opts_mismatch_types_with_spec() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuter": "OllamaTranslator",
        "importer": ["EpubImporter"],  # this should not be a list
        "exporter": "EpubExporter",
    }
    expected = ["type", "importer", "list", "str"]

    with pytest.raises(ValueError) as error:
        config = ScriptoriumConfiguration()
        config.check_spec_compliance(case)

    output_error = error.value.args[0]
    for expected_str in expected:
        assert expected_str in output_error.lower()


def test_parse_opts() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuter": "OllamaTranslator",
        "importer": "EpubImporter",
        "exporter": "EpubExporter",
    }
    ExpectedType = ImporterHandler

    config = ScriptoriumConfiguration()
    config.parse_handlers(case)

    OutputType = config.importer
    assert config.importer
    assert isinstance(OutputType, ExpectedType)


def test_parse_opts_model() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuter": ("OllamaTranslator", "ModelLlama3_2"),
        "importer": "EpubImporter",
        "exporter": "EpubExporter",
    }
    ExpectedType = ModelLlama3_2

    config = ScriptoriumConfiguration()
    config.parse_handlers(case)

    assert config.transmuter_type
    OutputModel = config.transmuter_type[1]
    assert OutputModel is ExpectedType
