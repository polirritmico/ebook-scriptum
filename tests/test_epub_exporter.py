#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.exporters.epub import EpubExporter
from src.importers.epub import EpubImporter


def test_export_epub() -> None:
    case = [Path("tests/files/simple_ebook.epub")]
    output_path = "tests/files/outputs/test_export_epub"

    importer = EpubImporter()
    exporter = EpubExporter()
    importer.load_data(case)
    document = importer.generate_document()
    exporter.export(document, output_path)


def test_update_epub_section() -> None:
    case = "THIS IS WORKING"
    expected = "THIS IS WORKING"
    case_input = [Path("tests/files/simple_ebook.epub")]
    case_output = [Path("tests/files/outputs/test_update_epub_section.epub")]

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
