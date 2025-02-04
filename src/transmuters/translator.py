#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable

from ollama import ChatResponse, chat

from src.document import Document
from src.models.qwen2_5 import ModelQwen as DefaultModel
from src.protocols import ModelHandler, TransmuterType


class Translator:
    """A TransmuterHandler subscriptor

    ollama docs at https://github.com/ollama/ollama-python
    """

    max_retry_attemps: int = 10
    model: ModelHandler
    response: ChatResponse
    run_validator: Callable[[str | None, str], bool]
    transmuter_type: TransmuterType = TransmuterType.LLM

    def set_model(self, model: ModelHandler) -> None:
        if model.transmuter_type != self.transmuter_type:
            msg = f"ModelHandler {model.transmuter_type} incompatible with {self.transmuter_type}"
            raise TypeError(msg)
        self.model = model or DefaultModel()
        if self.model.response_validator:
            self.run_validator = self.model.response_validator
        else:
            self.run_validator = self.generic_response_validator

    def transmute(self, document: Document) -> None:
        raise NotImplementedError
        for section_name, content in document.sections.items():
            self.translate_section(section_name, content)

    def translate_section(self, name: str, content) -> str:
        raise NotImplementedError

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

    def translate_text(self, text: str) -> str:
        attempts = 0
        while True:
            response = self.send_prompt(text)
            if self.run_validator(response, text):
                return response
            attempts += 1
            if attempts == self.max_retry_attemps:
                return response

    def generic_validator(self, response: str | None, original: str) -> bool:
        if response is None:
            return False
        if "  " in response and "  " not in original:
            return False
        # Since the translation is by paragraphs this should be a good criteria
        if "\n" in response and "\n" not in original:
            return False
        return True
