#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.dataclass import DocumentMetadata, Section
from src.document import Document


class SimpleTextImporter:
    def load_data(self, source: Path) -> None:
        pass

    def generate_document(self) -> Document:
        document = Document()
        metadata = self.build_metadata()
        # sections = self.parse_sections(metadata)

        # document.set_medatada(metadata)
        # document.set_sections(sections)
        return document

    def build_metadata(self):
        pass
