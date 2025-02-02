#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.catalyst_collector import CatalystCollector
from src.document import Document
from src.protocols import ImporterHandler, TransmuterHandler


class Scriptorium:
    DEFAULT_OUTPUT_PATH: str = "output"

    def __init__(self):
        self.importer: ImporterHandler | None = None
        self.transmuters: TransmuterHandler | list[TransmuterHandler] | None = None
        self.options: dict = {}
        self.document: Document | None = None
        self.input_files: list[Path] | None = None

        self.collector = CatalystCollector()

    def synthesize_transmutation(self):
        if not self.options or not isinstance(self.options, dict):
            raise ValueError("Missing options. Try set_options() first.")

    def set_importer(self, importer: ImporterHandler) -> None:
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
        parsed_opts = self.parse_options(opts)
        self.options = parsed_opts

    def parse_options(self, opts: dict) -> dict:
        collect_handler = self.collector.collect_handler
        transmuters = []
        for transmuter_name in opts.get("transmuters"):
            transmuter = collect_handler(transmuter_name, "src.transmuters")
            transmuters.append(transmuter)
        importer = collect_handler(opts.get("importer"), "src.importers")
        self.transmuters = transmuters
        self.importer = importer

        opts["input"] = Path(opts.get("input"))
        opts["transmuters"] = transmuters
        opts["importer"] = importer
        return opts

    def validate_options(self, opts: dict) -> bool:
        # TODO: options should be specific to the transmuter/model? If so they
        # need to be validated here. So we need to access those validations from
        # the setted transmuter.
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
            # if not output.exists():
            #     # create dir?
            #     # create file?
            #     pass

            self.output = output
            return True

        except Exception:
            return False

    def load_data(self) -> Document:
        source: Path = self.options.get("input_file")
        self.importer.load_data(source)
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
