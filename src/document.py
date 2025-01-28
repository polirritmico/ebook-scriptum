#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.metadata import DocumentMetadata, SectionMetadata


class Document:
    def __init__(self):
        self.metadata: DocumentMetadata = None
        self.sections: dict[str, SectionMetadata] = None
        self.source_path: str = ""

    def set_medatada(self, metadata: DocumentMetadata) -> None:
        self.validate_document_metadata(metadata)
        self.metada = metadata

    def set_sections(self, sections: dict[str, SectionMetadata]) -> None:
        self.validate_sections_metadata(sections)
        self.raw_sections = sections
        self.sections = self.parse_sections(sections)

    def parse_sections(self, sections: dict[str, SectionMetadata]) -> None:
        pass

    def validate_sections_metadata(sections: dict[str, SectionMetadata]) -> None:
        if not sections:
            raise ValueError("Missing sections")
        elif not isinstance(sections, dict):
            raise TypeError("sections is not a dict")

    def validate_document_metadata(self, metadata: DocumentMetadata) -> None:
        if not metadata:
            raise ValueError("Missing metadata")
        elif not self.metadata.title:
            raise ValueError("Document metadata: Missing title")
