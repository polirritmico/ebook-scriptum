#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.configuration import ScriptoriumConfiguration
from src.document import Document
from src.protocols import ExporterHandler, ImporterHandler, TransmuterHandler
from src.selectors import DocumentSectionSelector


class Scriptorium:
    DEFAULT_OUTPUT_PATH: str = "output"

    def __init__(self):
        self.document: Document | None = None
        self.exporter: ExporterHandler | None = None
        self.importer: ImporterHandler | None = None
        self.input_files: list[Path] | None = None
        self.options: ScriptoriumConfiguration = ScriptoriumConfiguration()
        self.output: Path | None = None
        self.transmuter: TransmuterHandler | None = None

    def setup(self, opts: dict | str | Path = None) -> None:
        self.options.setup(opts)
        self.set_handlers()
        self.set_handlers_options()

    def set_handlers(self) -> None:
        self.set_importer()
        self.set_transmuter()
        self.set_exporter()

    def set_handlers_options(self) -> None:
        self.input_files = self.options.input_file
        self.output = self.options.output

        importer_opts = self.options.get_importer_opts()
        if importer_opts:
            self.importer.set_options(importer_opts)

        exporter_opts = self.options.get_export_opts()
        if exporter_opts and self.exporter:
            self.exporter.set_options(exporter_opts)

        transmuter_opts = self.options.get_transmuter_opts()
        if transmuter_opts:
            self.transmuter.set_options(transmuter_opts)

    def set_importer(self, importer: ImporterHandler | None = None) -> None:
        self.importer = importer or self.options.importer

    def set_transmuter(self, transmuter: TransmuterHandler | None = None) -> None:
        self.transmuter = transmuter or self.options.transmuter

    def set_exporter(self, exporter: ExporterHandler | None = None) -> None:
        self.exporter = exporter or self.options.exporter

    def load_data(self) -> Document:
        self.importer.load_data(self.input_files)
        self.document = self.importer.generate_document()
        return self.document

    def transmute(self, document: Document | None = None) -> None:
        document = document if document else self.document
        selection = DocumentSectionSelector().select(document, self.options)
        self.transmuter.transmute(selection)

    def export(self, document: Document | None = None) -> Path:
        return self.transmuter.export(self.options.output)

    def validate_output(self) -> None:
        raise NotImplementedError
