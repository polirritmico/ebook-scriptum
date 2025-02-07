#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.exporters.epub import EpubExporter
from src.importers.epub import EpubImporter


def test_export_epub() -> None:
    case = Path("tests/files/simple_ebook.epub")
    output_path = "tests/files/output-export-epub"

    importer = EpubImporter()
    exporter = EpubExporter()
    importer.load_data(case)
    document = importer.generate_document()
    exporter.export(document, output_path)
