#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.document import Document
from src.protocols import ImporterHandler, TransmuterHandler


class Scriptorium:
    DEFAULT_OUTPUT: str = "output"

    def __init__(self):
        self.importer: ImporterHandler | None = None
        self.transmuters: TransmuterHandler | list[TransmuterHandler] | None = None
        self.opts: dict = {}
        self.document: Document | None = None
        self.input_files: list[Path] | None = None

    def set_importer(self, importer: ImporterHandler) -> None:
        self.importer = importer

    def set_transmuters(
        self, transmuters: TransmuterHandler | list[TransmuterHandler]
    ) -> None:
        if not isinstance(transmuters, list):
            transmuters = [transmuters]
        self.transmuters = transmuters

    def set_options(self, opts) -> None:
        if not self.validate_options(opts):
            raise ValueError("Bad options")
        self.opts = opts

    def validate_options(self, opts) -> bool:
        # TODO: options should be specific to the transmuter/model? If so they
        # need to be validated here. So we need to access those validations from
        # the setted transmuter.
        try:
            input_files = self.opts.get("input_files")
            if isinstance(input_files, str):
                input_files = [input_files]
            for i, file in enumerate(input_files):
                input_files[i] = Path(file)
            self.input_files = input_files

            output = self.opts.get("output", self.DEFAULT_OUTPUT)
            if isinstance(output, str):
                output = Path(output)
            elif not isinstance(output, Path):
                raise TypeError("opts.output is not a string nor a Path")
            self.output = output

            return True
        except Exception:
            return False

    def load_data(self) -> Document:
        source: Path = self.opts.get("input_file")
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
