#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import inquirer

from src.document import Document, Section


class DocumentSectionSelector:
    def select(self, document: Document) -> dict:
        choices: list[str] = []
        doc_spine = document.metadata.spine

        # sections = document.sections
        #
        # choices: list[str] = []
        # for i, section in enumerate(sections, start=1):
        #     name = f"{i:02}. {section.title}"
        #     choices.append(name)
        #
        # sections_selector_checkbox = inquirer.Checkbox(
        #     "sections",
        #     message="Select document sections to transmute",
        #     choices=choices,
        # )
        # selected = inquirer.prompt([sections_selector_checkbox]).get("sections")
        # selected_sections = []
        # for choice in selected:
        #     idx = int(choice.split(".")[0]) - 1
        #     selected_sections.append(sections[idx])
        # return selected_sections
