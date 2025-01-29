#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.document import Document
from src.protocols import TransmuterType


class Translator:
    """A TransmuterHandler subscriptor"""

    transmuter_type: TransmuterType = TransmuterType.LLM

    def transmute(self, document: Document) -> None:
        raise NotImplementedError
