#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.configuration import ScriptoriumConfiguration
from src.document import Document
from src.protocols import ImporterHandler, TransmuterHandler


class Scriptorium:
    DEFAULT_OUTPUT_PATH: str = "output"

    def __init__(self):
        self.importer: ImporterHandler | None = None
        self.transmuters: TransmuterHandler | list[TransmuterHandler] | None = None
        self.options: ScriptoriumConfiguration = ScriptoriumConfiguration()
        self.document: Document | None = None
        self.input_files: list[Path] | None = None

    def setup(self, opts: dict | str | Path = None) -> None:
        self.options.setup(opts)
        self.set_options()
        self.set_importer()
        self.set_transmuters()

    def set_options(self) -> None:
        self.input_files = self.options.input_file

    def set_importer(self, importer: ImporterHandler | None = None) -> None:
        self.importer = importer or self.options.importer

    def set_transmuters(
        self, transmuters: TransmuterHandler | list[TransmuterHandler] | None = None
    ) -> None:
        if transmuters is None:
            transmuters = self.options.transmuters
        elif not isinstance(transmuters, list):
            transmuters = [transmuters]
        self.transmuters = transmuters

    def load_data(self) -> Document:
        self.importer.load_data(self.input_files)
        self.document = self.importer.generate_document()
        return self.document

    def transmute(self, document: Document | None = None) -> None:
        document = document if document else self.document
        for transmuter in self.transmuters:
            transmuter.transmute(document)

    def synthesize_transmutation(self):
        raise NotImplementedError

    def validate_output(self) -> None:
        raise NotImplementedError

    def export(self):
        raise NotImplementedError

    def collect_transmuters(self, type: TransmuterHandler):
        raise NotImplementedError
