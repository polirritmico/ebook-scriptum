#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Tuple

from src.collector import Collector
from src.protocols import (
    ExporterHandler,
    ImporterHandler,
    ModelHandler,
    TransmuterHandler,
)

type TransmuterWithModel = Tuple[TransmuterHandler, ModelHandler]


class ScriptoriumConfiguration:
    config_spec = {
        "exporter": {"types": (str,), "mandatory": False},
        "importer": {"types": (str,), "mandatory": True},
        "input": {"types": (str, Path, list), "mandatory": True},
        "output": {"types": (str, Path), "mandatory": False},
        "transmuter": {"types": (str, tuple, list), "mandatory": True},
    }

    def __init__(self) -> None:
        self.importer: ImporterHandler | None = None
        self.exporter: ExporterHandler | None = None
        self.input_file: list[Path] | None = None
        self.output: Path | None = None
        self.raw_opts: dict | None = None
        self.transmuter: list[TransmuterHandler] | None = None
        self.transmuter_type: TransmuterWithModel | None = None
        self.importer_opts: dict | None = None
        self.transmuter_opts: dict | None = None
        self.exporter_opts: dict | None = None

        self.collector = Collector()

    def setup(self, opts: dict | str | Path) -> "ScriptoriumConfiguration":
        opts = self.set_options(opts)
        self.parse_options(opts)
        return self

    def set_options(self, opts: dict | str | Path) -> dict:
        opts = self.collector.collect_options(opts)
        self.raw_opts = opts.copy()
        self.check_spec_compliance(opts)
        return opts

    def parse_options(self, opts: dict | None = None) -> None:
        opts = opts or self.raw_opts.copy()
        if not opts:
            raise ValueError("Missing opts. Try set_options() first.")

        self.parse_non_handlers(opts)
        self.parse_handlers(opts)
        self.initialize_handlers()

    def initialize_handlers(self) -> None:
        uninstantiated_importer = isinstance(self.importer, type)
        if uninstantiated_importer:
            self.importer = self.importer()

        uninstantiated_exporter = isinstance(self.exporter, type)
        if uninstantiated_exporter:
            self.exporter = self.exporter()

        if self.transmuter_type:
            Transmuter, Model = self.transmuter_type
            model = Model() if Model is not None else None
            self.transmuter = Transmuter()
            self.transmuter.set_model(model)

    def parse_non_handlers(self, opts: dict) -> None:
        opts_input = opts.get("input")
        if not isinstance(opts_input, list):
            opts_input = [opts_input]
        self.input_file = [Path(filepath) for filepath in opts_input]

        self.check_files(self.input_file)
        self.output = Path(opts.get("output"))
        if self.output.is_dir():
            self.check_dir(self.output)

        metadata = opts.get("metadata")
        if metadata:
            self.metadata = opts.get("metadata")

        importer_opts = opts.get("importer_opts")
        if importer_opts:
            self.importer_opts = importer_opts

        exporter_opts = opts.get("exporter_opts")
        if exporter_opts:
            self.exporter_opts = exporter_opts

        transmuter_opts = opts.get("transmuter_opts")
        if transmuter_opts:
            self.transmuter_opts = transmuter_opts

    def parse_handlers(self, opts: dict) -> None:
        if not self.importer:
            self.importer = self.get_importer(opts)

        if not self.exporter:
            self.exporter = self.get_exporter(opts)

        if not self.transmuter:
            self.transmuter_type = self.get_transmuter_model_pairs(opts)

    def get_importer(self, opts: dict) -> ImporterHandler:
        importer_name = opts.get("importer")
        Importer = self.collector.collect_importer_handler(importer_name)
        if not Importer:
            raise ValueError("Missing importer")
        return Importer

    def get_exporter(self, opts: dict) -> ExporterHandler:
        exporter_name = opts.get("exporter")
        Exporter = self.collector.collect_exporter_handler(exporter_name)
        if not Exporter:
            raise ValueError("Missing exporter")
        return Exporter

    def get_transmuter_model_pairs(self, opts: dict) -> TransmuterWithModel:
        raw_transmuter = opts.get("transmuter")
        if isinstance(raw_transmuter, str):
            transmuter_name = raw_transmuter
            model_name = ""
        else:
            transmuter_name, model_name = raw_transmuter

        Transmuter = self.collector.collect_transmuter_handler(transmuter_name)
        Model = self.collector.collect_model_handler(model_name)

        if not Transmuter:
            raise ValueError("No transmuter has been loaded")

        return (Transmuter, Model)

    def check_spec_compliance(self, opts: dict) -> None:
        self.fill_optional_spec_fields_with_none()
        missing_entries_err = self.check_input_opts_missing_entries(opts)
        mismatch_settings_err = self.check_input_opts_mismatch_types(opts)

        detected_errors = missing_entries_err or mismatch_settings_err
        if detected_errors:
            msg = "Errors detected. Check passed options.\n"
            errors_msg = [msg] + missing_entries_err + mismatch_settings_err
            raise ValueError("\n".join(errors_msg))

    def fill_optional_spec_fields_with_none(self) -> None:
        for field, spec in self.config_spec.items():
            if spec["mandatory"] is False:
                spec["types"] = (*spec.get("types"), type(None))

    def check_input_opts_mismatch_types(self, opts: dict) -> list[str]:
        detected_type_mismatches = []
        for key, spec in self.config_spec.items():
            valid_types = spec.get("types")
            opt_value_type = type(opts.get(key))
            if any(issubclass(opt_value_type, valid) for valid in valid_types):
                continue

            opt_value_type = opt_value_type.__name__
            expected_types = ", ".join(_type.__name__ for _type in valid_types)
            err = (
                f"  - Key '{key}' has incorrect type: found '{opt_value_type}', "
                f"but '{expected_types}' is required"
            )
            detected_type_mismatches.append(err)

        return detected_type_mismatches

    def check_input_opts_missing_entries(self, opts: dict) -> list[str]:
        # TEST: This should not return an error with "" values (e.g. default model)
        detected_missing_keys = []
        for key, spec in self.config_spec.items():
            if not spec["mandatory"]:
                continue

            if key not in opts:
                err = f"  - Missing '{key}'"
                detected_missing_keys.append(err)
            elif opts[key] is None:
                err = f"  - Mandatory value is None: '{key}'"
                detected_missing_keys.append(err)

        if detected_missing_keys:
            err = "Found missing parameters in options:"
            detected_missing_keys.insert(0, err)

        return detected_missing_keys

    def check_dir(self, dir: Path, mkdir: bool = True) -> None:
        if not dir.exists():
            if not mkdir:
                raise ValueError(f"Output path does not exists: {dir}")
            # 755 owner|group|others, 7: read+write+execute; 5: read+execute
            dir.mkdir(mode=0o755, parents=True)

    def check_files(self, files: list[Path]) -> None:
        for file in files:
            if not file.exists():
                raise ValueError(f"File does not exists: '{file}'")

    def get_exporter_opts(self) -> dict | None:
        return self.exporter_opts

    def get_importer_opts(self) -> dict | None:
        return self.importer_opts

    def get_transmuter_opts(self) -> dict | None:
        return self.transmuter_opts
