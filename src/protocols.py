#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from src.document import Document


class TransmuterType(Enum):
    LLM = 1
    TTS = 2


@runtime_checkable
class ModelHandler(Protocol):
    transmuter_type: TransmuterType
    id: str

    def response_validator(self, response, request) -> bool: ...
    def make_instructions(self, content) -> Any: ...


class TransmuterHandler(Protocol):
    transmuter_type: TransmuterType

    def generic_validator(self, response: Any, original: Any) -> bool: ...
    def set_model(self, model: ModelHandler) -> None: ...
    def transmute(self, document: Document) -> None: ...


class ImporterHandler(Protocol):
    source: Path | None = None

    def load_data(self, source: Path) -> None: ...
    def generate_document(self) -> Document: ...
