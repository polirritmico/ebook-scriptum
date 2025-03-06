#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.dataclass import DocumentMetadata, Section


class Document:
    def __init__(self):
        self.metadata: DocumentMetadata | None = None
        self.sections: dict[str, Section] | None = None
        self.source: Path | None = None

    def get_section(self, section_name: str | Path) -> Section:
        if isinstance(section_name, Path):
            section_name = section_name.name
        return self.sections.get(section_name)

    def get_content(self, section_name: str | Path, raw: bool = False) -> str:
        if isinstance(section_name, Path):
            section_name = section_name.name
        section = self.sections.get(section_name)
        if not section:
            raise KeyError(f"Missing section from the document: {section_name}")

        if raw:
            return section.content.get_text()
        else:
            return section.content.prettify()

    def set_medatada(self, metadata: DocumentMetadata) -> None:
        self.validate_document_metadata(metadata)
        self.metadata = metadata
        self.source = metadata.source

    def set_sections(self, sections: dict[str, Section]) -> None:
        self.validate_sections(sections)
        self.sections = sections

    def validate_sections(self, sections: dict[str, Section]) -> None:
        if not sections:
            raise ValueError("Missing sections")
        elif not isinstance(sections, dict):
            raise TypeError("sections is not a dict")

    def validate_document_metadata(self, metadata: DocumentMetadata) -> None:
        if not metadata:
            raise ValueError("Missing metadata")
