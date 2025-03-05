#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path

from src.document import Document
from src.models.vitts_es import ModelVittsEs as DefaultModel
from src.processors.vitts_audio_processor import VittsAudioProcessor
from src.processors.vitts_text_processor import VittsTextProcessor
from src.protocols import ExporterHandler, ModelHandler, TransmuterType


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
        self.model = None
        self.opts = {}
        self.tts_opts = {}

    def generic_response_validator(self, response: str | None, original: str) -> bool:
        return True

    def set_options(self, opts: dict) -> None:
        if not isinstance(opts, dict):
            raise TypeError("CoquiTTS bad options type")
        self.opts = opts
        self.set_export_options(opts)

    def set_export_options(self, opts: dict) -> None:
        opts = opts.get("export_opts")
        if not opts:
            return

        self.tts_opts = opts
        self.tts_opts["vocoder_name"] = self.model.vocoder

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
        return

    def transmute(self, document: Document) -> None:
        processed_document = self.process_text(document)
        self.processed_document = processed_document

        self.model.prepare_request(self.opts)
        self.tts = TTS(
            model_name=self.model.name, config_path=self.opts.get("config_path")
        ).to(self.device)

    def export(self, output_dir: Path) -> None:
        # TODO: Add a document selector
        if not hasattr(self, "processed_document") or not hasattr(self, "tts"):
            raise ValueError("Not transmuted document. Try transmute() first")

        # # TODO: REMOVE
        # if len(self.document) > 1:
        #     # FIX: Implement this and clean options! check if is an output dir
        #     raise NotImplementedError("No multiple output files implemented")

        # NOTE:
        # 1. Change config 20100 -> 19800 khz to improve the tempo (to fast):
        #    ~/.local/share/tts/tts_models--es--css10--vits/config.json
        # 2. pysbd is hardcoded to `en` so changed to `es`:
        #    ~/.local/lib/python3.10/site-packages/TTS/utils/synthesizer.py:93
        #    .venv/lib/python3.12/site-packages/TTS/utils/synthesizer.py:93

        if output_dir.is_file():
            raise ValueError(f"Output path is not a dir: '{output_dir}'")
        output_dir.mkdir(parents=True, exist_ok=True)

        processed_files = []
        for name, section in self.processed_document.items():
            if not section:
                continue
            name = Path(name).with_suffix(".wav")
            output_file = output_dir / name
            processed_files.append(output_file)
            self.tts.tts_to_file(**self.tts_opts, text=section, file_path=output_file)

        self.apply_audio_post_processing(processed_files)

        return output_dir

    def apply_audio_post_processing(self, files: list[Path]) -> None:
        processor = VittsAudioProcessor()
        for file in files:
            processor.run(file)

    def process_text(self, document: Document) -> dict[Path, str]:
        processed_document: dict[Path, str] = {}
        opts = self.opts.get("text_processor_opts") or self.model.text_processor_opts
        book_words = self.opts.get("book_words", {})

        text_processor = VittsTextProcessor().process_text
        for section_name, section in document.sections.items():
            section_txt = document.get_content(section_name, True)
            processed_text = text_processor(section_txt, book_words, opts)
            processed_document[section_name] = processed_text

        return processed_document
