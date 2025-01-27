#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.metadata import DocumentMetadata, SectionMetadata
from src.section import Section


class Document:
    def __init__(self):
        self.metadata: DocumentMetadata = None
        self.sections: dict[str, SectionMetadata] = {}
        self.source_path: str = ""

    def set_medatada(self, metadata: DocumentMetadata) -> None:
        if not metadata:
            raise ValueError("Got empty metadata")
        self.metada = metadata
        self.validate_document_metadata()

    def set_sections(self, sections: dict[str, SectionMetadata]) -> None:
        pass

    def validate_document_metadata(self) -> None:
        if not self.metadata:
            raise ValueError("Missing metadata")
        elif not self.metadata.title:
            raise ValueError("Document metadata: Missing title")
