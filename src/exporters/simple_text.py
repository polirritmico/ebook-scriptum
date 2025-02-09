#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

# from bs4 import BeautifulSoup
# from src.dataclass import DocumentMetadata, Section
from src.document import Document


class SimpleTextExporter:
    """ExporterHandler subscriptor"""

    def set_options(self, config) -> None:
        pass

    def export(self, document: Document, output: Path) -> None:
        new_content = self.merge_all_sections_into_a_multiline_string(document)
        try:
            output.write_text(new_content, encoding="utf-8")
        except Exception:
            raise Exception("Can't write output file")

    def merge_all_sections_into_a_multiline_string(self, document: Document) -> str:
        new_content: list[str] = []
        for file, section in document.sections.items():
            new_section = document.get_content(file, raw=True)
            new_content.append(new_section)

        output_text = "\n\n".join(new_content)
        return output_text
