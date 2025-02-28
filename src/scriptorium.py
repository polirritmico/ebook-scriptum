#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.configuration import ScriptoriumConfiguration
from src.document import Document
from src.protocols import ExporterHandler, ImporterHandler, TransmuterHandler


class Scriptorium:
    DEFAULT_OUTPUT_PATH: str = "output"

    def __init__(self):
        self.importer: ImporterHandler | None = None
        self.transmuter: TransmuterHandler | None = None
        self.options: ScriptoriumConfiguration = ScriptoriumConfiguration()
        self.document: Document | None = None
        self.input_files: list[Path] | None = None
        self.output: Path | None = None

    def setup(self, opts: dict | str | Path = None) -> None:
        self.options.setup(opts)
        self.set_options()
        self.set_importer()
        self.set_transmuter()
        self.set_exporter()

    def set_options(self) -> None:
        self.input_files = self.options.input_file
        self.output = self.options.output

        importer_opts = self.options.get_importer_opts()
        if importer_opts:
            self.importer.set_options(importer_opts)

        transmuter_opts = self.options.get_transmuter_opts()
        if transmuter_opts:
            self.transmuter.set_options(transmuter_opts)

        exporter_opts = self.options.get_exporter_opts()
        if exporter_opts and self.transmuter.exporter:
            self.transmuter.exporter.set_options(exporter_opts)

    def set_importer(self, importer: ImporterHandler | None = None) -> None:
        self.importer = importer or self.options.importer

    def set_transmuter(self, transmuter: TransmuterHandler | None = None) -> None:
        self.transmuter = transmuter or self.options.transmuter

    def set_exporter(self, exporter: ExporterHandler | None = None) -> None:
        exporter = exporter or self.options.exporter
        if exporter is None:
            return
        exporter.set_options(self.options)
        self.transmuter.set_exporter(exporter)

    def load_data(self) -> Document:
        self.importer.load_data(self.input_files)
        self.document = self.importer.generate_document()
        return self.document

    def transmute(self, document: Document | None = None) -> None:
        document = document if document else self.document
        self.transmuter.transmute(document)

    def export(self, document: Document | None = None) -> Path:
        return self.transmuter.export(self.options.output)

    def validate_output(self) -> None:
        raise NotImplementedError
