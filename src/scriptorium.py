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

    def synthesize_transmutation(self):
        if not self.options or not isinstance(self.options, dict):
            raise ValueError("Missing options. Try set_options() first.")

    def set_importer(self, importer: ImporterHandler) -> None:
        if importer:
            self.importer = importer
        else:
            importer = self.options.get("importer")
            if importer:
                self.importer = importer

    def set_transmuters(
        self, transmuters: TransmuterHandler | list[TransmuterHandler]
    ) -> None:
        if not isinstance(transmuters, list):
            transmuters = [transmuters]
        self.transmuters = transmuters

    def set_options(self, opts) -> None:
        opts = self.collector.collect_options(opts)
        if not self.validate_options(opts):
            raise ValueError("Bad options")
        parsed_opts = self.apply_options(opts)
        self.set_models(opts)
        self.options = parsed_opts

    def apply_options(self, opts: dict) -> dict:
        opts["input"] = Path(opts.get("input"))

        collect_handler = self.collector.collect_handler
        if not self.transmuters:
            transmuters = []
            for transmuter_name in opts.get("transmuters"):
                Transmuter = collect_handler(transmuter_name, "src.transmuters")
                transmuters.append(Transmuter())
            if not transmuters:
                raise ValueError("Not transmuter has been loaded")
            self.transmuters = transmuters

        if not self.importer:
            importer = collect_handler(opts.get("importer"), "src.importers")
            if not importer:
                raise ValueError("Missing importer")
            self.importer = importer()

        return opts

    def validate_options(self, opts: dict) -> bool:
        try:
            input_files = opts.get("input")
            if isinstance(input_files, str):
                input_files = [input_files]
            for i, file in enumerate(input_files):
                input_files[i] = Path(file)
            self.input_files = input_files

            output = self.options.get("output", self.DEFAULT_OUTPUT_PATH)
            if isinstance(output, str):
                output = Path(output)
            elif not isinstance(output, Path):
                raise TypeError("opts.output is not a string nor a Path")

            self.output = output
            return True

        except Exception:
            return False

    def load_data(self) -> Document:
        self.importer.load_data(self.input_files)
        self.document = self.importer.generate_document()
        return self.document

    def transmute(self, document: Document) -> None:
        document = document if document else self.document
        for transmuter in self.transmuters:
            transmuter.transmute(document)

    def validate_output(self) -> None:
        raise NotImplementedError

    def export(self):
        raise NotImplementedError

    def collect_transmuters(self, type: TransmuterHandler):
        pass
