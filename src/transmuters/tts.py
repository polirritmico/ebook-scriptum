#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.document import Document
from src.protocols import ModelHandler, TransmuterType


class TtsTransmuter:
    transmuter_type: TransmuterType = TransmuterType.TTS

    def generic_response_validator(self, response: str | None, original: str) -> bool:
        return True

    def set_model(self, model: ModelHandler) -> None:
        pass

    def transmute(self, document: Document) -> None:
        pass
