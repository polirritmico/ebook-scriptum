#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any

from src.protocols import TransmuterType

# transmuter_type: TransmuterType
# id: str
#
# def response_validator(self, response, request) -> bool: ...
# def make_instructions(self, content) -> Any: ...


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

    def make_instructions(self, content) -> Any:
        if not isinstance(content, str):
            raise TypeError("content is not of type str")
        return {
            "model": self.id,
            "messages": [
                {"role": "system", "content": self.instruction},
                {"role": "user", "content": content},
            ],
        }

    response_validator = None
