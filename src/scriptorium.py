#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.protocols import ImporterHandler, TransmuterHandler


class Scriptorium:
    def set_importer(self, importer: ImporterHandler) -> None:
        raise NotImplementedError

    def set_transmuters(
        self, transmuters: TransmuterHandler | list[TransmuterHandler]
    ) -> None:
        raise NotImplementedError

    def set_options(self, opts) -> None:
        raise NotImplementedError

    def load_data(self) -> None:
        raise NotImplementedError

    def generate_document(self) -> None:
        raise NotImplementedError

    def transmute(self) -> None:
        raise NotImplementedError

    def validate_output(self) -> None:
        raise NotImplementedError

    def export(self):
        raise NotImplementedError
