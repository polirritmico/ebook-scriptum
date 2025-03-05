#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.importers.epub import EpubImporter
from src.selectors import DocumentSectionSelector


def test_resolve_selection() -> None:
    case_input_file = [Path("tests/files/simple_ebook.epub")]
    case = ["Section0001.xhtml"]
    expected_len = 1
    expected_file = case[0]

    importer = EpubImporter()
    importer.load_data(case_input_file)
    document = importer.generate_document()

    selector = DocumentSectionSelector()
    output = selector.resolve_selection(document, case)

    assert expected_len == len(output.sections)
    assert expected_file == next(iter(output.sections.keys()))
