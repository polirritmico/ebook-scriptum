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
    transmuter_type: TransmuterType  # LLM, TTS
    response_validator: ResponseValidator | None

    def prepare_request(self, opts: dict) -> Any: ...


@runtime_checkable
class ImporterHandler(Protocol):
    sources: list[Path] | None = None

    def load_data(self, sources: Path | list[Path]) -> None: ...

    def generate_document(self) -> Document: ...


@runtime_checkable
class ExporterHandler(Protocol):
    def set_options(self, options: dict[str, Any]) -> None: ...

    def export(self, document: Document, output: Path) -> None: ...


@runtime_checkable
class TransmuterHandler(Protocol):
    exporter: ExporterHandler | None
    generic_response_validator: ResponseValidator
    transmuter_type: TransmuterType

    def set_model(self, model: ModelHandler) -> None: ...

    def set_exporter(self, exporter: ExporterHandler) -> None: ...

    def transmute(self, document: Document) -> None: ...

    def export(self, path: Path) -> None: ...
