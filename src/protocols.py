#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Any, Protocol, runtime_checkable

from src.document import Document


class TransmuterHandler(Protocol):
    def transmute(self, document: Document) -> None: ...


class ImporterHandler(Protocol):
    def load_data(self, source: str) -> None: ...

    def generate_document(self) -> Document: ...


class ModelType(Enum):
    OLLAMA = 1
    TTS = 2


@runtime_checkable
class ModelHandler(Protocol):
    model_type: ModelType
    id: str

    def response_validator(self, response, request) -> bool: ...

    def make_instructions(self, content) -> Any: ...
