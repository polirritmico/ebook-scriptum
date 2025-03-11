#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from pathlib import Path

from src.configuration import ScriptoriumConfiguration
from src.document import Document


class DocumentSectionSelector:
    def select(self, document: Document, opts: ScriptoriumConfiguration) -> Document:
        preselection = opts.get_selected_sections()
        if preselection:
            return self.resolve_selection(document, preselection)
        else:
            return self.manual_selector(document)

    def manual_selector(self, document: Document) -> Document:
        try:
            import inquirer
        except Exception:
            raise ImportError("Failed import: inquirer")

        preselect_question = inquirer.Confirm("sel", message="Preselect all sections?")
        select_all = inquirer.prompt([preselect_question]).get("sel")

        section_choices: dict[str, str] = {}
        for section in document.sections.values():
            choice = f"{section.order:02}. {section.title}"  # {section.filepath.name}"
            section_choices[choice] = section.filepath

        choices = list(section_choices.keys())
        sections_selector_checkbox = inquirer.Checkbox(
            "sections",
            message="Select document sections to transmute",
            choices=choices,
            default=choices if select_all else [],
        )
        user_selection = inquirer.prompt([sections_selector_checkbox]).get("sections")

        selected_sections = [section_choices[selected] for selected in user_selection]
        return self.resolve_selection(document, selected_sections)

    def resolve_selection(self, document: Document, selected: list[Path]) -> Document:
        if selected[0].name == "*":
            return document

        selected_sections = {file.name: document.get_section(file) for file in selected}
        filtered_document = copy(document)
        filtered_document.sections = selected_sections
        return filtered_document
