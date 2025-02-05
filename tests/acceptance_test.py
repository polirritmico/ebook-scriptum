#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.document import Document
from src.importers.epub import EpubImporter
from src.models.qwen2_5 import ModelQwen
from src.protocols import ImporterHandler, ModelHandler, TransmuterHandler
from src.scriptorium import Scriptorium
from src.transmuters.translator import Translator


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="acceptance-test_") as tmp:
        yield tmp


def test_epub_importer_handler_protocol_compliance() -> None:
    case_file = Path("tests/files/simple_ebook.epub")

    epub = EpubImporter()
    epub.load_data(case_file)
    output = epub.generate_document()
    assert isinstance(output, Document)
    assert output.metadata


@pytest.mark.skip(reason="Not implemented")
def test_translate_full_ebook(tmp_dir) -> None:
    case = {
        "input": "tests/files/simple_ebook.epub",
        "output": "tests/files/mock.epub",
        "transmuters": {"Translator": ""},
        "importer": "EpubImporter",
    }

    scriptum = Scriptorium()
    scriptum.setup(case)
    scriptum.load_data()
    # scriptum.transmute()
    # scriptum.validate_output()
    # output = scriptum.export()
    # assert output
