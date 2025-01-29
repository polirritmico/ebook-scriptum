#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.document import Document
from src.epub import EpubImporter

# from src.models.qwen2_5 import ModelQwen
from src.protocols import ImporterHandler, ModelHandler, TransmuterHandler
from src.scriptorium import Scriptorium
from src.translator import Translator


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="acceptance-test_") as tmp:
        yield tmp


def test_epub_importer_handler_protocol_compliance(tmp_dir) -> None:
    case_file = Path("tests/files/simple_ebook.epub")

    epub = EpubImporter()
    epub.load_data(case_file)
    output = epub.generate_document()
    assert isinstance(output, Document)
    assert output.metadata


@pytest.mark.skip(reason="Not implemented")
def test_translate_full_ebook(tmp_dir, file_loader) -> None:
    case = {
        "file_input": "tests/files/simple_ebook.epub",
        "output_file": "tests/files/mock.epub",
    }
    expected = file_loader("tests/files/simple_ebook_expected.html")

    importer: ImporterHandler = EpubImporter()
    model: ModelHandler = ModelQwen()
    translator: TransmuterHandler = Translator(model)

    scriptum = Scriptorium()
    scriptum.set_importer(importer)
    scriptum.set_transmuters(translator)
    scriptum.set_options(case)  # After this the system behaviour is fully setted
    scriptum.load_data()  # The ImporterHandler gets the data from the source, then generates a Document instance # fmt: skip
    scriptum.transmute()  # The TransmuterHandler receives the Document and perform the Transmutation # fmt: skip
    scriptum.validate_output()  # TODO: Who validates the output? ExportHandler -> IOHandler?
    output = scriptum.export()

    assert output
    assert len(expected) == len(output)
    for expected_line, output_line in zip(expected.split("\n"), output.split("\n")):
        assert expected_line == output_line
