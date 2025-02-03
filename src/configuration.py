#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.catalyst_collector import CatalystCollector
from src.protocols import ImporterHandler, TransmuterHandler


class ScriptoriumConfig:
    def __init__(self) -> None:
        self.validated = False

    def validate(self, opts: dict) -> bool:
        self.validated = True
        return True

    def set_options(self, opts: dict) -> None:
        opts = self.parse_options(opts)
        if not self.validate(opts):
            raise ValueError("Bad options")

    def parse_options(self, opts: dict) -> dict:
        pass

    def set_importer(self, importer: ImporterHandler | None = None) -> None:
        pass

    def set_transmuters(
        self, transmuter: TransmuterHandler | list[TransmuterHandler] | None = None
    ) -> None:
        pass

    def collect_transmuters(self) -> list[TransmuterHandler]:
        pass

    def collect_importer(self) -> ImporterHandler:
        pass
