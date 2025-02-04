#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.configuration import ScriptoriumConfiguration
from src.protocols import ImporterHandler, TransmuterHandler


def test_parse_opts() -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/output",
        "transmuters": ["Translator"],
        "importer": "EpubImporter",
    }
    ExpectedType = ImporterHandler

    config = ScriptoriumConfiguration()
    config.parse_options(case)

    OutputType = type(config.importer)
    assert config.importer
    assert isinstance(OutputType, ExpectedType)
