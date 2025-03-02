#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path

from src.document import Document
from src.models.vitts_es import ModelVittsEs as DefaultModel
from src.protocols import ExporterHandler, ModelHandler, TransmuterType
from src.utils.vitts_text_processor import VittsTextProcessor


class CoquiTTS:
    transmuter_type: TransmuterType = TransmuterType.TTS
    exporter: ExporterHandler | None

    def __init__(self):
        try:
            global torch
            import torch

            assert torch.cuda.is_available()

            global TTS
            from TTS.api import TTS

        except Exception:
            raise ImportError

        self.tts = None
        self.device = "cuda"
        self.exporter = None
        self.opts = {}

    def generic_response_validator(self, response: str | None, original: str) -> bool:
        return True

    def set_options(self, options: dict) -> None:
        if not isinstance(options, dict):
            raise TypeError("CoquiTTS bad options type")
        self.opts = options

    def set_model(self, model: ModelHandler) -> None:
        if model and model.transmuter_type != self.transmuter_type:
            msg = f"ModelHandler {model.transmuter_type} incompatible with {self.transmuter_type}"
            raise TypeError(msg)
        if "vitts" not in model.id:
            raise ValueError(f"Model {model.id} is not a vitts model")

        self.model = model or DefaultModel()
        if self.model.response_validator:
            self.run_validator = self.model.response_validator
        else:
            self.run_validator = self.generic_response_validator

    def set_exporter(self, exporter: ExporterHandler) -> None:
        if not isinstance(exporter, ExporterHandler):
            raise TypeError("exporter is not an ExporterHandler")
        self.exporter = exporter

    def transmute(self, document: Document) -> None:
        processed_document = self.process_text(document)
        self.document = processed_document

        self.model.prepare_request(self.opts)
        self.tts = TTS(
            model_name=self.model.name, config_path=self.opts.get("config_path")
        ).to(self.device)

    def export(self, output_path: Path) -> None:
        if not hasattr(self, "document") or not hasattr(self, "tts"):
            raise ValueError("Not transmuted document. Try transmute() first")

        tts_opts = {"vocoder_name": self.model.vocoder}

        # if hasattr(self, "lang_model") and self.lang_model:
        #     tts_opts["lang"] = self.lang_model

        if len(self.document) > 1:
            # FIX: Implement this and clean options! check if is an output dir
            raise NotImplementedError("No multiple output files implemented")

        # NOTE:
        # 1. Change config 20100 -> 19800 khz to improve the tempo (to fast):
        #    /home/docker-usr/.local/share/tts/tts_models--es--css10--vits/config.json
        # 2. pysbd is hardcoded to `en` so changed to `es`:
        #    ~/.local/lib/python3.10/site-packages/TTS/utils/synthesizer.py:93

        for name, section in self.document.items():
            tts_opts["text"] = section
            tts_opts["file_path"] = output_path  # / name
            self.tts.tts_to_file(**tts_opts)

        return output_path

    def process_text(self, document: Document) -> dict[Path, str]:
        processed_document: dict[Path, str] = {}
        opts = getattr(self, "opts", {})
        book_words = opts.get("book_words", {})

        process_text = VittsTextProcessor().process_text
        for section_name, section in document.sections.items():
            section_txt = document.get_content(section_name, True)
            processed_text = process_text(section_txt, book_words, opts)
            processed_document[section_name] = processed_text

        return processed_document
