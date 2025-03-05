#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any

from src.protocols import TransmuterType


class ModelVittsEs:
    DEFAULT_VOCODER = "vocoder_models/universal/libri-tts/wavegrad"
    DEFAULT_MODEL_NAME = "tts_models/es/css10/vits"
    DEFAULT_LANG = "es"
    DEFAULT_TXT_PROC = {
        "lang": DEFAULT_LANG,
        "log": False,
    }

    transmuter_type: TransmuterType = TransmuterType.TTS
    response_validator = None

    id: str = "vitts:latest"  # :14b or latest
    base_instruction: dict = {}
    tag: str = "vitts"

    def __init__(self, id: str | None = None, instruction: str | None = None):
        self.id = id if id else self.id
        self.instruction = instruction if instruction else self.base_instruction
        self.text_processor_opts = self.DEFAULT_TXT_PROC

    def prepare_request(self, opts: dict) -> Any:
        opts = opts.get("vitts", opts)

        self.vocoder = opts.get("vocoder", self.DEFAULT_VOCODER)
        self.name = opts.get("name", self.DEFAULT_MODEL_NAME)
        self.lang = opts.get("lang", self.DEFAULT_LANG)
        self.speaker = opts.get("speaker", "")

        text_processor_opts = opts.get("text_processor")
        if text_processor_opts:
            self.text_processor_opts = text_processor_opts

        return {
            "vocoder_name": self.vocoder,
            "name": self.name,
            "lang": self.lang,
            "speaker_wav": self.speaker,
        }
