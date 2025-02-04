#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib

# import os
import json
from pathlib import Path

from src.protocols import ImporterHandler, ModelHandler, TransmuterHandler


class CatalystCollector:
    IMPORTERS_SOURCE_PATH = "src.importers"
    MODELS_SOURCE_PATH = "src.modules"
    TRANSMUTERS_SOURCE_PATH = "src.transmuters"

    def collect_importer_handler(self, name: str) -> ImporterHandler:
        """Returns the class subscribed to the InputHandler protocol (not the instance)"""
        Importer = self.collect_handler(name, self.IMPORTERS_SOURCE_PATH)
        return Importer

    def collect_transmuter_handler(self, name: str) -> TransmuterHandler:
        """Returns the class subscribed to the TransmuterHandler protocol (not the instance)"""
        Transmuter = self.collect_handler(name, self.TRANSMUTERS_SOURCE_PATH)
        return Transmuter

    def collect_model_handler(self, name: str) -> ModelHandler | None:
        """Returns the class subscribed to the ModelHandler protocol (not the instance)"""
        if not name:
            return None
        Importer = self.collect_handler(name, self.IMPORTERS_SOURCE_PATH)
        return Importer

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

    def collect_options(self, opts: dict | Path = None) -> dict[str, str | list[str]]:
        if isinstance(opts, dict):
            return opts

        opts_path = Path(opts)
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
