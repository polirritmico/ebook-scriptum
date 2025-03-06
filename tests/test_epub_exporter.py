#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.exporters.epub import EpubExporter
from src.importers.epub import EpubImporter


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory(dir="tests/files/", prefix="epub_exporter-test-") as tmp:
        yield Path(tmp)


def test_export_epub(tmp_dir) -> None:
    case = [Path("tests/files/simple_ebook.epub")]
    expected = tmp_dir / "test_export_epub"

    importer = EpubImporter()
    exporter = EpubExporter()
    importer.load_data(case)
    document = importer.generate_document()
    exporter.export(document, expected)

    assert expected.exists()
    assert expected.is_file()
    assert expected.stat().st_size > 0


def test_update_epub_section(tmp_dir) -> None:
    case = "THIS IS WORKING"
    expected = "THIS IS WORKING"
    expected_file = tmp_dir / "test_update_epub_section.epub"
    case_input = [Path("tests/files/simple_ebook.epub")]
    case_output = [expected_file]

    prev_importer = EpubImporter()
    prev_importer.load_data(case_input)
    prev_document = prev_importer.generate_document()
    prev_section = prev_document.sections["Section0001.xhtml"]
    prev_section.content.find("p").string.replace_with(case)
    assert case == prev_section.content.find("p").string

    exporter = EpubExporter()
    exporter.export(prev_document, case_output[0])

    after_importer = EpubImporter()
    after_importer.load_data(case_output)
    after_document = after_importer.generate_document()
    after_section = after_document.sections["Section0001.xhtml"]
    output = after_section.content.find("p").string

    assert expected in output

    assert expected_file.exists()
    assert expected_file.is_file()
    assert expected_file.stat().st_size > 0
