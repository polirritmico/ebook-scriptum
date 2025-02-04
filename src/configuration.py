#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.catalyst_collector import CatalystCollector
from src.protocols import ImporterHandler, ModelHandler, TransmuterHandler


class ScriptoriumConfiguration:
    def __init__(self) -> None:
        self.importer: ImporterHandler | None = None
        self.input_file: Path | None = None
        self.output: Path | None = None
        self.raw_opts: dict | None = None
        self.transmuters: dict[TransmuterHandler, ModelHandler] | None = None

        self.collector = CatalystCollector()

    def set_options(self, opts: dict) -> None:
        self.raw_opts = opts.copy()
        self.check_minimun_required_keys(opts)
        self.parse_non_handlers(opts)
        self.parse_handlers(opts)
        self.initialize_handlers()

    def initialize_handlers(self) -> None:
        self.importer: ImporterHandler = self.importer()

        instantiated_transmuters = []
        for Transmuter, Model in self.transmuters:
            model = Model() if Model is not None else None
            transmuter = Transmuter()
            transmuter.set_model(model)
            instantiated_transmuters.append(transmuter)
        self.transmuters = instantiated_transmuters

    def parse_non_handlers(self, opts: dict) -> None:
        self.input_file = Path(opts.get("input"))
        self.check_file(self.input_file)
        self.output = Path(opts.get("output"))
        self.check_dir(self.output)

    def parse_handlers(self, opts: dict) -> None:
        if not self.importer:
            self.importer = self.get_importer(opts)

        if not self.transmuters:
            self.transmuters = self.get_transmuter_model_pairs(opts)

    def get_importer(self, opts: dict) -> ImporterHandler:
        importer_name = opts.get("importer")
        Importer = self.collector.collect_importer_handler(importer_name)
        if not Importer:
            raise ValueError("Missing importer")

        return Importer

    def get_transmuter_model_pairs(self, opts: dict) -> list[TransmuterHandler]:
        transmuters_names = opts.get("transmuters")
        transmuters = []
        for transmuter_name, model_name in transmuters_names.items():
            Transmuter = self.collector.collect_transmuter_handler(transmuter_name)
            Model = self.collector.collect_model_handler(model_name)
            transmuters.append((Transmuter, Model))

        if not transmuters:
            raise ValueError("No transmuter has been loaded")

        return transmuters

    def check_minimun_required_keys(self, opts: dict) -> None:
        required_keys = [
            "input",
            "output",
            "transmuters",
            "importer",  # TODO: infer importer from the input
        ]

        missing_keys = []
        for required_key in required_keys:
            if required_key not in opts.keys():
                msg = f"  - Missing parameter: '{required_key}'"
                missing_keys.append(msg)
            elif opts[required_key] is None:
                msg = f"  - Missing {required_key} value"
                missing_keys.append(msg)

        if missing_keys:
            raise KeyError(f"opts is missing required setting:\n{missing_keys}")

    def check_dir(self, dir: Path, mkdir: bool = True) -> None:
        # 755 owner|group|others, 7: read+write+execute; 5: read+execute
        mkdir_mode = 0o755
        if not dir.exists():
            if not mkdir:
                raise ValueError(f"Output path does not exists: {dir}")

            dir.mkdir(mode=mkdir_mode, parents=True)

    def check_file(self, file: Path) -> None:
        if not file.exists():
            raise ValueError(f"File does not exists: '{file}'")
