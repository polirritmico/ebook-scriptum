#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any

from src.protocols import TransmuterType


class ModelVittsEs:
    DEFAULT_VOCODER = "vocoder_models/universal/libri-tts/wavegrad"
    DEFAULT_MODEL_NAME = "tts_models/es/css10/vits"
    DEFAULT_LANG = "es"

    transmuter_type: TransmuterType = TransmuterType.TTS

    id: str = "vitts:latest"  # :14b or latest
    base_instruction: dict = {}
    tag: str = "vitts"

    def __init__(self, id: str | None = None, instruction: str | None = None):
        self.id = id if id else self.id
        self.instruction = instruction if instruction else self.base_instruction

    def prepare_request(self, opts: dict) -> Any:
        opts = opts.get("vitts", opts)

        self.vocoder = opts.get("vocoder", self.DEFAULT_VOCODER)
        self.name = opts.get("name", self.DEFAULT_MODEL_NAME)
        self.lang = opts.get("lang", self.DEFAULT_LANG)
        self.speaker = opts.get("speaker", "")

        return {
            "vocoder_name": self.vocoder,
            "name": self.name,
            "lang": self.lang,
            "speaker_wav": self.speaker,
        }

    def response_validator(self, response: str | None, original: str) -> bool:
        return True
