#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

import pytest

from src.importers.epub import EpubImporter

test_fs: Path = Path("tests/files/out")


@pytest.fixture
def clean_fs() -> None:
    if test_fs.exists():
        shutil.rmtree(test_fs)
    test_fs.mkdir(parents=True)
    yield
    if test_fs.exists():
        shutil.rmtree(test_fs)


def test_parse_toc_file() -> None:
    case_file = [Path("tests/files/simple_ebook.epub")]
    expected_entries = [
        ("Text/cubierta.xhtml", "Cubierta"),
        ("Text/Section0001.xhtml", "Chapter 1"),
    ]

    epub = EpubImporter()
    epub.load_data(case_file)
    output_toc = epub.get_section_names_from_toc_file()

    for expected, output in zip(expected_entries, output_toc):
        assert expected[0] == output[0]
        assert expected[1] == output[1]


def test_epub_importer_handler_protocol_compliance() -> None:
    case_file = [Path("tests/files/simple_ebook.epub")]

    epub = EpubImporter()
    epub.load_data(case_file)
    output = epub.generate_document()
    assert type(output).__name__ == "Document"
    assert output.metadata


def test_get_sections_in_order_from_content_opf(clean_fs) -> None:
    case_file = Path("tests/files/simple_ebook.epub")
    expected_files = [
        "Text/cubierta.xhtml",
        "Text/TOC.xhtml",
        "Text/Section0001.xhtml",
    ]

    epub = EpubImporter()
    epub.extract_epub(case_file, test_fs)
    epub.collect_metadata_and_text_files(test_fs)
    epub.collect_files_data()
    metadata = epub.parse_document_metadata()
    assert metadata
    output = metadata.spine

    for expected, output in zip(expected_files, output):
        assert Path(expected).name == output.name


def test_parse_sections(clean_fs) -> None:
    case_file = Path("tests/files/simple_ebook.epub")
    expected_section = "Section0001.xhtml"
    expected_sections_count = 3
    expected_title = "Chapter 1"
    expected_lang = "es"
    expected_order = 2  # 0-index

    epub = EpubImporter()
    epub.extract_epub(case_file, test_fs)
    epub.collect_metadata_and_text_files(test_fs)
    epub.collect_files_data()

    metadata = epub.parse_document_metadata()
    assert metadata is not None
    epub.parse_sections(metadata)
    assert expected_sections_count == len(epub.parsed_sections)
    output = epub.parsed_sections[expected_section]

    assert output
    assert expected_title == output.title
    assert expected_lang == output.lang
    assert expected_order == output.order


def test_parse_section_title(clean_fs) -> None:
    case_file = Path("tests/files/simple_ebook.epub")
    expected_section = "cubierta.xhtml"
    expected_title = "Cubierta"
    expected_lang = "es"
    expected_order = 0

    epub = EpubImporter()
    epub.extract_epub(case_file, test_fs)
    epub.collect_metadata_and_text_files(test_fs)
    epub.collect_files_data()

    metadata = epub.parse_document_metadata()
    assert metadata is not None
    epub.parse_sections(metadata)
    output = epub.parsed_sections[expected_section]

    assert output
    assert expected_title == output.title
    assert expected_lang == output.lang
    assert expected_order == output.order


def test_parse_metadata(clean_fs) -> None:
    case_file = Path("tests/files/simple_ebook.epub")
    expected_title = "Título"
    expected_language = "es"
    expected_creator = "Nombres Apellidos"

    epub = EpubImporter()
    epub.extract_epub(case_file, test_fs)
    epub.collect_metadata_and_text_files(test_fs)
    epub.collect_files_data()
    output = epub.parse_document_metadata()

    assert expected_title == output.title
    assert expected_language == output.lang
    assert expected_creator == output.creator


def test_collect_files_data(clean_fs) -> None:
    case_file = Path("tests/files/simple_ebook.epub")
    expected_file = Path(test_fs) / "OEBPS" / "Text" / "Section0001.xhtml"
    expected_str = "<p><i>Italic paragraph.</i></p>"
    expected_metadata = "<dc:title>Título</dc:title>"

    epub = EpubImporter()
    epub.extract_epub(case_file, test_fs)
    epub.collect_metadata_and_text_files(test_fs)
    epub.collect_files_data()

    assert epub.text_files_content
    assert epub.metadata_file_content

    assert epub.text_files_content[expected_file]
    assert expected_str in epub.text_files_content[expected_file]
    assert expected_metadata in epub.metadata_file_content


def test_extract_epub(clean_fs) -> None:
    case = Path("tests/files/simple_ebook.epub")
    expected_chapters_path = Path(test_fs) / "OEBPS" / "Text"
    expected_files = ["cubierta.xhtml", "Section0001.xhtml", "TOC.xhtml"]

    epub = EpubImporter()
    epub.extract_epub(case, test_fs)

    assert test_fs.exists()
    assert any([element.is_dir() for element in test_fs.iterdir()])
    for i, file in enumerate(expected_chapters_path.iterdir()):
        assert file.name in expected_files


def test_collect_text_and_metadata_files(clean_fs) -> None:
    case = Path("tests/files/simple_ebook.epub")
    expected_text_paths = [
        "tests/files/out/OEBPS/Text/Section0001.xhtml",
        "tests/files/out/OEBPS/Text/TOC.xhtml",
        "tests/files/out/OEBPS/Text/cubierta.xhtml",
    ]

    epub = EpubImporter()
    epub.extract_epub(case, test_fs)
    output_text, output_meta = epub.collect_metadata_and_text_files(test_fs)

    assert output_meta
    assert len(output_text) == 3
    for expected in expected_text_paths:
        assert Path(expected) in output_text
