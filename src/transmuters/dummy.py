#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path

from src.document import Document
from src.protocols import ExporterHandler, ModelHandler, TransmuterType


class DummyTransmuter:
    transmuter_type: TransmuterType = TransmuterType.LLM

    def set_options(self, options: dict) -> None:
        return

    def set_model(self, model: ModelHandler) -> None:
        return

    def set_exporter(self, exporter: ExporterHandler) -> None:
        return

    def transmute(self, document: Document) -> None:
        return

    def export(self, path: Path) -> None:
        return

    def generic_response_validator(self, foo, bar) -> bool:
        return True
