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
    """
    ModelHandler Protocol. This class is used by the `TransmuterHandler` and
    allows implementing multiple models to the same handler if is compatible
    (share the same `TransmuterType`).

    :param id: <Model name>:<Tag>. For example: `"deepseek:latest"`.
    :param transmuter_type: TransmuterType enum. (LLM or TTS)
    :param response_validator: `ResponseValidator` function. If is `None` the
        `TransmuterHandler` would use its generic validator.
    :param make_instructions: Function to generate the instructions passed to
        the IA service by the `TransmuterHandler`.
    """

    id: str  # <name>:<tag>
    transmuter_type: TransmuterType
    response_validator: ResponseValidator | None

    def make_instructions(self, content) -> Any: ...


@runtime_checkable
class TransmuterHandler(Protocol):
    transmuter_type: TransmuterType
    generic_response_validator: ResponseValidator

    def set_model(self, model: ModelHandler) -> None: ...

    def transmute(self, document: Document) -> None: ...


@runtime_checkable
class ImporterHandler(Protocol):
    sources: list[Path] | None = None

    def load_data(self, sources: list[Path]) -> None: ...

    def generate_document(self) -> Document: ...


@runtime_checkable
class ExporterHandler(Protocol):
    def set_options(self, config) -> None: ...

    def export(self, document: Document, output: Path) -> None: ...
