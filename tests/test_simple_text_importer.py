#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.importers.simple_text import SimpleTextImporter


def test_paragraph_separation() -> None:
    filename = "simple_text_paragraph.txt"
    case = Path("tests/files/") / filename
    expected = "Title\nThis is a paragraph.\nThis is another paragraph."
    get_raw_text_instead_html = True

    importer = SimpleTextImporter()
    importer.load_data([case])
    document = importer.generate_document()
    output = document.get_content(case, get_raw_text_instead_html)

    assert expected == output


def test_read_file() -> None:
    case = Path("tests/files/simple.txt")
    expected = "En un lugar de la Mancha, de cuyo nombre no quiero acordarme"

    importer = SimpleTextImporter()
    importer.load_data([case])
    output = importer.generate_document()

    assert output.metadata.lang
    assert output.metadata.title
    assert output.metadata.creator
    assert output.metadata.description
    assert output.sections

    assert case.name in output.sections

    assert output.sections[case.name].content
    assert expected in output.sections[case.name].text[0]


def test_build_metadata() -> None:
    case = [Path("tests/files/Author_Name_-_Some_Title.txt")]
    expected_lang = "es"
    expected_title = "Some Title"
    expected_creator = "Author Name"
    expected_description = "'Some Title' by Author Name."
    expected_source = case[0]

    importer = SimpleTextImporter()
    importer.load_data(case)
    output = importer.build_metadata()

    assert expected_lang == output.lang
    assert expected_title == output.title
    assert expected_creator == output.creator
    assert expected_description == output.description
    assert expected_source == output.source


def test_detect_lang() -> None:
    case_en = "This is a simple test."
    case_es = "Esto es una prueba simple."

    importer = SimpleTextImporter()

    assert "en" == importer.infer_content_lang(case_en)
    assert "es" == importer.infer_content_lang(case_es)


def test_detect_system_lang(monkeypatch) -> None:
    case = "es_CL.utf8"
    expected = "es"

    monkeypatch.setenv("LANG", case)

    importer = SimpleTextImporter()
    output = importer.get_system_lang()

    assert expected == output


def test_detect_encoding() -> None:
    case1 = Path("tests/files/simple.txt")
    case2 = Path("tests/files/simple-iso.txt")
    expected1 = "utf-8"
    expected2 = "iso-8859-1"

    importer = SimpleTextImporter()
    output1 = importer.detect_encoding(case1)
    output2 = importer.detect_encoding(case2)

    assert expected1 == output1
    assert expected2 == output2
