#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.metadata import DocumentMetadata, SectionMetadata
from src.section import Section


class Document:
    def __init__(self):
        self.sections: list[Section] = []
        self.source_path: str = ""

    def set_medatada(self, metadata: dict[str, SectionMetadata]) -> None:
        pass

    def set_sections(self, sections) -> None:
        pass
