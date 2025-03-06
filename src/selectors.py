#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from pathlib import Path

from src.configuration import ScriptoriumConfiguration
from src.document import Document


class DocumentSectionSelector:
    def select(self, document: Document, opts: ScriptoriumConfiguration) -> dict:
        preselection = opts.get_selected_sections()
        if preselection:
            return self.resolve_selection(document, preselection)
        else:
            return self.manual_selector(document)

    def manual_selector(self, document: Document) -> Document:
        try:
            import inquirer
        except Exception:
            # TODO: self.failback_manual_selector(document)?
            raise ImportError("Failed import: inquirer")

        # doc_spine = document.metadata.spine
        choices: list[str] = []
        for i, section in enumerate(document.sections, start=1):
            name = f"{i:02}. {section.title}"
            choices.append(name)

        sections_selector_checkbox = inquirer.Checkbox(
            "sections",
            message="Select document sections to transmute",
            choices=choices,
        )
        selected = inquirer.prompt([sections_selector_checkbox]).get("sections")
        selected_sections = []
        for choice in selected:
            idx = int(choice.split(".")[0]) - 1
            selected_sections.append(document.sections[idx])
        return selected_sections

    def resolve_selection(self, document: Document, selected: list[Path]) -> Document:
        selected_sections = {file.name: document.get_section(file) for file in selected}
        filtered_document = copy(document)
        filtered_document.sections = selected_sections
        return filtered_document
