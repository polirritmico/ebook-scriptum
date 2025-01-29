#!/usr/bin/env python
# -*- coding: utf-8 -*-

from protocols import TransmuterType
from src.document import Document


class Translator:
    """A TransmuterHandler subscriptor"""

    transmuter_type: TransmuterType = TransmuterType.LLM

    def transmute(self, document: Document) -> None:
        raise NotImplementedError
