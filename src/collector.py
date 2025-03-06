#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import json
from pathlib import Path

from src.protocols import (
    ExporterHandler,
    ImporterHandler,
    ModelHandler,
    TransmuterHandler,
)


class Collector:
    IMPORTERS_SOURCE_PATH = "src.importers"
    EXPORTERS_SOURCE_PATH = "src.exporters"
    MODELS_SOURCE_PATH = "src.models"
    TRANSMUTERS_SOURCE_PATH = "src.transmuters"

    def collect_importer_handler(self, name: str) -> ImporterHandler:
        """Returns the class subscribed to the InputHandler protocol (not the instance)"""
        Importer = self.collect_handler(name, self.IMPORTERS_SOURCE_PATH)
        return Importer

    def collect_exporter_handler(self, name: str) -> ExporterHandler:
        """Returns the class subscribed to the ExporterHandler protocol (not the instance)"""
        Exporter = self.collect_handler(name, self.EXPORTERS_SOURCE_PATH)
        return Exporter

    def collect_transmuter_handler(self, name: str) -> TransmuterHandler:
        """Returns the class subscribed to the TransmuterHandler protocol (not the instance)"""
        Transmuter = self.collect_handler(name, self.TRANSMUTERS_SOURCE_PATH)
        return Transmuter

    def collect_model_handler(self, name: str) -> ModelHandler | None:
        """Returns the class subscribed to the ModelHandler protocol (not the instance)"""
        if not name:
            return None
        Model = self.collect_handler(name, self.MODELS_SOURCE_PATH)
        return Model

    def collect_handler(
        self, handler_name: str, source_path: str
    ) -> ImporterHandler | TransmuterHandler | ModelHandler:
        """Returns the handler class (not the instance)"""
        if not handler_name or not source_path:
            raise ValueError("Can't import handler. Check parameters")

        path = Path(source_path.replace(".", "/"))
        for file in path.iterdir():
            if file.name == "__init__.py":
                continue

            module_name = f"{source_path}.{file.stem}"
            module = importlib.import_module(module_name)

            handler_class = getattr(module, handler_name, None)
            if handler_class:
                return handler_class

        raise ImportError(f"Could not import handler {handler_name} from {module_name}")

    def collect_options(self, opts: dict | str) -> dict[str, str | dict[str, str]]:
        opts_path = opts if isinstance(opts, Path) else Path(opts)

        if opts_path.is_dir():
            opts_path /= "config.json"
        if not opts_path.is_file():
            raise FileNotFoundError(f"Missing configuration file at '{opts_path}'")
        return self.read_config_file(opts_path)

    def read_config_file(self, path: Path) -> dict:
        try:
            with path.open(mode="r", encoding="utf-8") as stream:
                opts = json.load(stream)
            return opts
        except Exception:
            raise IOError(f"Could not read config json at '{path}'")
