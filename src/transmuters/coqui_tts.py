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
        self.device = "cuda"
        self.exporter = None
        self.keep_wav = None
        self.model = None
        self.opts = {}
        self.processor = None
        self.text_processor_opts = {}
        self.tts = None
        self.tts_opts = {}
        self.word_dict: dict[str, str] = {}

    def import_libraries(self) -> None:
        """
        Loading torch and TTS tooks a lot of time so we move the import here,
        to use it when it's really is needed.
        """
        try:
            global torch
            # import torch
            from torch import cuda

            assert cuda.is_available()

            global TTS
            from TTS.api import TTS

        except Exception:
            raise ImportError

    def generic_response_validator(self, response: str | None, original: str) -> bool:
        return True

    def set_options(self, opts: dict) -> None:
        if not isinstance(opts, dict):
            raise TypeError("CoquiTTS bad options type")
        self.opts = opts.get("exporter_opts", opts)
        self.set_export_options(self.opts)

    def set_export_options(self, opts: dict) -> None:
        word_dict = opts.get("word_dict")
        if word_dict:
            self.word_dict = word_dict

        self.tts_opts = opts.get("tts_opts", {})
        self.text_processor_opts = opts.get("text_processor_opts", {})
        self.text_processor_opts["log"] = opts.get("log")
        self.text_processor_opts["keep_wav"] = opts.get("keep_wav")
        self.text_processor_opts["lang"] = opts.get("lang")

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
        self.processed_document = self.process_text(document)

        self.model.prepare_request(self.opts)
        self.import_libraries()
        self.tts = TTS(
            model_name=self.model.name, config_path=self.opts.get("config_path")
        ).to(self.device)

    def export(self, output_dir: Path) -> None:
        if not hasattr(self, "processed_document") or not hasattr(self, "tts"):
            raise ValueError("Not transmuted document. Try transmute() first")

        # NOTE:
        # 1. Change config 20100 -> 19800 khz to improve the tempo (to fast):
        #    ~/.local/share/tts/tts_models--es--css10--vits/config.json
        # 2. pysbd is hardcoded to `en` so changed to `es`:
        #    ~/.local/lib/python3.10/site-packages/TTS/utils/synthesizer.py:93
        #    .venv/lib/python3.12/site-packages/TTS/utils/synthesizer.py:93

        if output_dir.is_file():
            raise ValueError(f"Output path is not a dir: '{output_dir}'")
        output_dir.mkdir(parents=True, exist_ok=True)

        for file, section in self.processed_document.items():
            if not section:
                continue
            if not isinstance(file, Path):
                file = Path(file)
            name = file.with_name(file.name + ".wav")
            audio_file = output_dir / name
            self.tts.tts_to_file(**self.tts_opts, text=section, file_path=audio_file)

            output_file = audio_file.with_suffix(".mp3")
            self.apply_audio_post_processing(audio_file, output_file)

        return output_dir

    def apply_audio_post_processing(self, input_file: Path, output_file: Path) -> None:
        if self.processor is None:
            self.processor = VittsAudioProcessor()
        self.processor.run(input_file, output_file, self.opts)

    def process_text(self, document: Document) -> dict[Path, str]:
        processed_document: dict[Path, str] = {}
        opts = self.text_processor_opts or self.model.text_processor_opts
        store_log = "log" in opts

        text_processor = VittsTextProcessor().process_text
        for section_name, section in document.sections.items():
            section_txt = document.get_content(section_name, True)
            if store_log:
                opts["log_section_name"] = section_name
            processed_text = text_processor(section_txt, self.word_dict, opts)
            output_name = f"{section.order:02}. {section.title}"
            processed_document[output_name] = processed_text

        return processed_document
