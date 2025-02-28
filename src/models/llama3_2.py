#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any

from src.protocols import TransmuterType


class ModelLlama3_2:
    transmuter_type: TransmuterType = TransmuterType.LLM

    id: str = "llama3.2"
    instruction: str = (
        "Translate from English to Spanish. Use correct punctuation and grammar. "
        "Preserve all non-letter symbols and assume the user knows their meaning. "
        "DO NOT INCLUDE ANY TEXT IN YOUR RESPONSE THAT IS NOT PART OF THE TRANSLATION"
        ", such as introductory statements, clarifications, questions, doubts, "
        "or any text not directly translating the given content:"
    )
    tag: str = "llama3.2"

    def __init__(self, id: str | None = None, instruction: str | None = None):
        if id:
            self.id = id
        if instruction:
            self.instruction = instruction

    def prepare_request(self, opts: dict) -> Any:
        content = opts.get("content")
        return {
            "model": self.id,
            "messages": [
                {"role": "system", "content": self.instruction},
                {"role": "user", "content": content},
            ],
        }

    response_validator = None
