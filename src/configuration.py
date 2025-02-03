#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.catalyst_collector import CatalystCollector
from src.protocols import ImporterHandler, TransmuterHandler

IMPORTERS_SOURCE = "src.importers"
MODELS_SOURCE = "src.modules"
TRANSMUTERS_SOURCE = "src.transmuters"


class ScriptoriumConfiguration:
    def __init__(self) -> None:
        self.transmuters: list[TransmuterHandler] | None = None
        self.importer = None
        self.validated = False
        self.collector = CatalystCollector()

    def validate(self, opts: dict) -> bool:
        self.validated = True
        return True

    def set_options(self, opts: dict) -> None:
        opts = self.parse_options(opts)
        if not self.validate(opts):
            raise ValueError("Bad options")

    def parse_options(self, opts: dict) -> dict:
        opts["input"] = Path(opts.get("input"))

        collect_handler = self.collector.collect_handler
        if not self.transmuters:
            transmuters = []
            for transmuter_name in opts.get("transmuters"):
                Transmuter = collect_handler(transmuter_name, TRANSMUTERS_SOURCE)
                transmuters.append(Transmuter())
            if not transmuters:
                raise ValueError("Not transmuter has been loaded")
            self.transmuters = transmuters

        if not self.importer:
            Importer = collect_handler(opts.get("importer"), IMPORTERS_SOURCE)
            if not Importer:
                raise ValueError("Missing importer")
            self.importer = Importer()

        return opts

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
