#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Protocol, runtime_checkable

from src.document import Document


class TransmuterType(Enum):
    LLM = 1
    TTS = 2


type ResponseValidator = Callable[["ModelHandler", Any, Any], bool]


@runtime_checkable
class ModelHandler(Protocol):
    id: str  # <name>:<tag>
    transmuter_type: TransmuterType
    response_validator: ResponseValidator | None

    def make_instructions(self, content) -> Any: ...


class TransmuterHandler(Protocol):
    transmuter_type: TransmuterType
    generic_validator: ResponseValidator

    def __init__(self, model: ModelHandler | None = None): ...
    def set_model(self, model: ModelHandler) -> None: ...
    def transmute(self, document: Document) -> None: ...


class ImporterHandler(Protocol):
    source: Path | None = None

    def load_data(self, source: Path) -> None: ...
    def generate_document(self) -> Document: ...
