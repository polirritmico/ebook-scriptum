#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Protocol, runtime_checkable


class TransmuterHandler(Protocol):
    pass


class ImporterHandler(Protocol):
    pass


class ModelType(Enum):
    OLLAMA = 1
    TTS = 2


@runtime_checkable
class ModelHandler(Protocol):
    pass
