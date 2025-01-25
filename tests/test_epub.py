#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

import pytest

from src.epub import EpubImporter

test_fs: Path = Path("tests/files/out")


@pytest.fixture
def clean_fs() -> None:
    if test_fs.exists():
        shutil.rmtree(test_fs)
    test_fs.mkdir(parents=True)
    yield
    if test_fs.exists():
        shutil.rmtree(test_fs)


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
    expected_metadata_paths = [
        "tests/files/out/OEBPS/content.opf",
        "tests/files/out/OEBPS/toc.ncx",
    ]

    epub = EpubImporter()
    epub.extract_epub(case, test_fs)
    out_text, out_meta = epub.collect_text_and_metadata_files(test_fs)

    assert len(out_text) == 3
    assert len(out_meta) == 2
    for expected in expected_text_paths:
        assert Path(expected) in out_text
    for expected in expected_metadata_paths:
        assert Path(expected) in out_meta


# def test_get_section_titles(clean_fs) -> None:
#     case = os.path.normpath("tests/files/simple_ebook.epub")
#     expected = {
#         "Text/cubierta.xhtml": "Cubierta",
#         "Text/Section0001.xhtml": "Chapter 1",
#     }
#     expected_path = "tests/files/out/OEBPS/toc.ncx"
#
#     epub = Epub(case)
#     epub.extract(test_fs)
#     assert os.path.exists(expected_path)
#
#     epub.collect_section_files()
#     output = epub.extract_section_title()
#
#     for exp, out in zip(expected.items(), output.items()):
#         assert exp[0] == out[0]
#         assert exp[1] == out[1]
