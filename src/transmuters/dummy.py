#!/usr/bin/env python
# -*- coding: utf-8 -*-


from src.document import Document
from src.protocols import ModelHandler, TransmuterType


class DummyTransmuter:
    transmuter_type: TransmuterType = TransmuterType.LLM

    def set_model(self, model: ModelHandler) -> None:
        return

    def transmute(self, document: Document) -> None:
        return

    def generic_response_validator(self, foo, bar) -> bool:
        return True
