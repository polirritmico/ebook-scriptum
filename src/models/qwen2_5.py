#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any

from src.protocols import TransmuterType


class ModelQwen:
    transmuter_type: TransmuterType = TransmuterType.LLM

    id: str = "qwen2.5:latest"  # :14b or latest
    base_instruction: str = (
        "Translate from English to Spanish. Keep html tags. Use correct Spanish punctuation and grammar. "
        "Provide only the translated text without any additions. "
        "Focus exclusively on translating the given content text and ensure your response contains only the translation. "
        "Any extra text, beyond the translated text, would result in a poor response:"
    )
    bad_chars_tolerance: int = 3
    valid_utf = (
        (0x0020, 0x024F),  # Basic to extended Latin (without control chars)
        (0x0370, 0x03FF),  # Greek and Coptic
        (0x2200, 0x22FF),  # Mathematical Operators
        (0x1D400, 0x1D7FF),  # Mathematical Alphanumeric Symbols
        (0x1F300, 0x1F9FF),  # Emojis and Miscellaneous Symbols
        (0x2654, 0x265F),  # Chess Pieces
    )
    tag: str = "qwen2.5"

    def __init__(self, id: str | None = None, instruction: str | None = None):
        self.id = id if id else self.id
        self.instruction = instruction if instruction else self.base_instruction

    def make_instructions(self, content) -> Any:
        return {
            "model": self.id,
            "messages": [
                {"role": "system", "content": self.instruction},
                {"role": "user", "content": content},
            ],
        }

    def response_validator(self, response: str | None, original: str) -> bool:
        if response is None:
            return False
        if "  " in response and "  " not in original:
            return False
        if "\n" in response and "\n" not in original:
            return False

        consecutive_bad_chars = 0
        for char in response:
            if char == " ":
                continue
            val = ord(char)
            if any(left <= val <= right for left, right in self.valid_utf):
                consecutive_bad_chars = 0
            else:
                consecutive_bad_chars += 1
            if consecutive_bad_chars == self.bad_chars_tolerance:
                return False
        return True
