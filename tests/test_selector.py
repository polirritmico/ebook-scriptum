#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import inquirer
import pytest

from src.importers.epub import EpubImporter
from src.selectors import DocumentSectionSelector


def test_resolve_selection() -> None:
    case_input_file = [Path("tests/files/simple_ebook.epub")]
    case = [Path("Section0001.xhtml")]
    expected_len = 1
    expected_file = case[0].name

    importer = EpubImporter()
    importer.load_data(case_input_file)
    document = importer.generate_document()

    selector = DocumentSectionSelector()
    output = selector.resolve_selection(document, case)

    assert expected_len == len(output.sections)
    assert expected_file == next(iter(output.sections.keys()))


def test_sections_selector(monkeypatch: pytest.MonkeyPatch) -> None:
    case_input_file = [Path("tests/files/simple_ebook.epub")]
    expected_selection_len = 2
    expected_section_filename = ["TOC.xhtml", "Section0001.xhtml"]

    importer = EpubImporter()
    importer.load_data(case_input_file)
    document = importer.generate_document()

    selector = DocumentSectionSelector()
    patched_output = {"sections": ["01. Índice de contenido", "02. Chapter 1"]}
    with monkeypatch.context() as m:
        m.setattr(inquirer, "prompt", lambda _: patched_output)
        document = selector.manual_selector(document)

    output = list(document.sections.keys())
    assert expected_selection_len == len(output)
    assert expected_section_filename[0] == output[0]
    assert expected_section_filename[1] == output[1]
