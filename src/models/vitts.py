#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any

from src.protocols import TransmuterType


class ModelVitts:
    transmuter_type: TransmuterType = TransmuterType.TTS

    id: str = "vitts:latest"  # :14b or latest
    base_instruction: dict = {}
    tag: str = "vitts"

    def __init__(self, id: str | None = None, instruction: str | None = None):
        self.id = id if id else self.id
        self.instruction = instruction if instruction else self.base_instruction
        self.name = "tts_models/es/css10/vits"

    def make_instructions(self, content) -> Any:
        pass

    def response_validator(self, response: str | None, original: str) -> bool:
        return True
