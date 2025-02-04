#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.configuration import ScriptoriumConfiguration
from src.models.llama3_2 import ModelLlama3_2
from src.protocols import ImporterHandler, TransmuterHandler


def test_minimal_keys_check_ok() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuters": {"Translator": ""},
        "importer": "EpubImporter",
    }
    config = ScriptoriumConfiguration()
    config.check_minimun_required_keys(case)


def test_minimal_keys_check_missing_input() -> None:
    case = {
        "output": "tests/files/output",
        "transmuters": {"Translator": ""},
        "importer": "EpubImporter",
    }
    with pytest.raises(KeyError) as error:
        config = ScriptoriumConfiguration()
        config.check_minimun_required_keys(case)

    expected_error = "Missing parameter: 'input'"
    output_error = error.value.args[0]
    assert expected_error in output_error


def test_parse_opts() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuters": {"Translator": ""},
        "importer": "EpubImporter",
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
        "transmuters": {"Translator": "ModelLlama3_2"},
        "importer": "EpubImporter",
    }
    ExpectedType = ModelLlama3_2

    config = ScriptoriumConfiguration()
    config.parse_handlers(case)
    assert len(config.transmuters) == 1
    first_transmuter_with_model = config.transmuters[0]
    Model = first_transmuter_with_model[1]
    assert Model is ExpectedType
