#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory

import pytest

from src.epub import EpubImporter
from src.models.qwen2_5 import ModelQwen
from src.protocols import ImporterHandler, ModelHandler, TransmuterHandler
from src.scriptorium import Scriptorium
from src.translator import Translator


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="test/files", prefix="acceptance_test-") as tmp:
        yield tmp


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
    scriptum.load_data()  # The ImporterHandler gets the data from the source
    scriptum.generate_document()  # The ImporterHandler generates a Document instance
    scriptum.transmute()  # The TransmuterHandler receives the Document and perform the Transmutation
    scriptum.validate_output()
    output = scriptum.export()

    assert output
    assert len(expected) == len(output)
    for expected_line, output_line in zip(expected.split("\n"), output.split("\n")):
        assert expected_line == output_line
