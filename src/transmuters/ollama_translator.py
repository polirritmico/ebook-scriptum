#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Callable

from ollama import ChatResponse, chat
from ollama import list as ollama_list

from src.dataclass import Section
from src.document import Document
from src.exporters.simple_text import SimpleTextExporter as DefaultExporter
from src.models.qwen2_5 import ModelQwen as DefaultModel
from src.protocols import ExporterHandler, ModelHandler, TransmuterType


class OllamaTranslator:
    """A TransmuterHandler subscriptor

    ollama docs at https://github.com/ollama/ollama-python
    """

    max_retry_attemps: int = 10
    model: ModelHandler
    response: ChatResponse
    run_validator: Callable[[str | None, str], bool]
    transmuter_type: TransmuterType = TransmuterType.LLM
    exporter: ExporterHandler | None

    def __init__(self):
        self.translated_metadata: dict[str, str] = {}
        self.document = None
        self.exporter = None
        self.model = None
        self.response = None
        self.run_validator = None
        self.max_retry_attemps = 10
        self.translatable_tags = [
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "li",
            "a",
            "span",
        ]

    def set_model(self, model: ModelHandler | None) -> None:
        if model and model.transmuter_type != self.transmuter_type:
            msg = f"ModelHandler {model.transmuter_type} incompatible with {self.transmuter_type}"
            raise TypeError(msg)
        self.model = model or DefaultModel()
        if self.model.response_validator:
            self.run_validator = self.model.response_validator
        else:
            self.run_validator = self.generic_response_validator

    def set_exporter(self, exporter: ExporterHandler | None) -> None:
        if not exporter or not isinstance(exporter, ExporterHandler):
            exporter = DefaultExporter()
        self.exporter = exporter

    def transmute(self, document: Document) -> None:
        self.check_ollama()

        for section_name, section in document.sections.items():
            self.translate_section_metadata(section)
            self.translate_section_content(section)

        self.document = document

    def export(self, path: Path) -> None:
        if self.exporter is None:
            raise ValueError("Missing exporter. Try set_exporter()")
        if self.document is None:
            raise ValueError("Missing transmuted document. Try transmute()")

        self.exporter.export(self.document, path)

    def translate_section_metadata(self, section: Section) -> None:
        section.title = self.translate_metadata(section.title)

    def translate_metadata(self, text: str) -> str | None:
        if text in self.translated_metadata:
            return self.translated_metadata[text]

        translated_text = self.translate_text(text)
        self.translated_metadata[text] = translated_text

    def translate_section_content(self, section: Section) -> str:
        for tag in section.content.find_all(self.translatable_tags):
            if tag.string:
                translated_text = self.translate_text(tag.string)
                tag.string.replace_with(translated_text)

    def translate_text(self, text: str) -> str:
        attempts = 0
        while True:
            response = self.send_prompt(text)
            if self.run_validator(response, text):
                return response
            attempts += 1
            if attempts == self.max_retry_attemps:
                return response

    def check_ollama(self) -> None:
        try:
            ollama_list()
        except Exception:
            raise

    def send_prompt(self, text_to_translate: str = None) -> str:
        msg = self.model.make_instructions(text_to_translate)
        response: ChatResponse = chat(**msg)
        response_text = self.get_text_from_response(response)
        return response_text

    def get_text_from_response(self, response: ChatResponse) -> str:
        try:
            return response.message.content
        except AttributeError:
            return ""

    def generic_response_validator(self, response: str | None, original: str) -> bool:
        if response is None:
            return False
        if "  " in response and "  " not in original:
            return False
        # Since the translation is by paragraphs this should be a good criteria
        if "\n" in response and "\n" not in original:
            return False
        return True
