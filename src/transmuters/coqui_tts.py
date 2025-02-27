#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path

from src.document import Document
from src.models.vitts import ModelVitts as DefaultModel
from src.protocols import ModelHandler, TransmuterType


class CoquiTTS:
    transmuter_type: TransmuterType = TransmuterType.TTS

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
        self.opts = {}

    def generic_response_validator(self, response: str | None, original: str) -> bool:
        return True

    def set_model(self, model: ModelHandler) -> None:
        if model and model.transmuter_type != self.transmuter_type:
            msg = f"ModelHandler {model.transmuter_type} incompatible with {self.transmuter_type}"
            raise TypeError(msg)
        self.model = model or DefaultModel()
        if self.model.response_validator:
            self.run_validator = self.model.response_validator
        else:
            self.run_validator = self.generic_response_validator

    def process_text(self, document: Document) -> dict[Path, str]:
        processed_document: dict[Path, str] = {}
        return processed_document

    def transmute(self, document: Document) -> None:
        # processed_document = self.process_text(document)
        self.opts["vocoder"] = "vocoder_models/universal/libri-tts/wavegrad"
        self.output_path = "tests/files/outputs/tts_out.wav"

        self.tts = TTS(
            model_name=self.model.name, config_path=self.opts.get("config_path")
        ).to(self.device)

        text = document.get_content("simple.txt", raw=True)

        tts_opts = {
            "file_path": self.output_path,
            "text": text,
            "speaker_wav": self.opts.get("speaker"),
            "vocoder_name": self.opts.get("vocoder"),
        }

        if hasattr(self, "lang_model") and self.lang_model:
            tts_opts["lang"] = self.lang_model

        self.tts.tts_to_file(**tts_opts)
        return self.output_path

    # def process_file(file_path: str, output_file: str, opts):
    #     print("opening text file...")
    #     with open(file_path, "r", encoding="utf-8") as stream:
    #         content = stream.read()
    #
    #     content = text_processor(content, word_dict, opts)
    #
    #     print("Executing text to audio...")
    #     text_to_audio(content, output_file, opts)

    # def main():
    #     opts = {}
    #     tag = ""
    #
    #     # Universal ES
    #     opts["model"] = "tts_models/es/css10/vits"
    #     opts["vocoder"] = "vocoder_models/universal/libri-tts/wavegrad"
    #     opts["lang"] = "es"
    #     opts["lang_model"] = False
    #     # opts["vocoder"] = "vocoder_models/universal/libri-tts/fullband-melgan"
    #
    #     # NOTE: pysbd is hardcoded to `en` so changed to `es`:
    #     #    ~/.local/lib/python3.10/site-packages/TTS/utils/synthesizer.py:93
    #
    #     # EN (apt install espeak-ng)
    #     # opts["model"] = "tts_models/en/ljspeech/vits"
    #     # opts["vocoder"] = "vocoder_models/en/ljspeech/hifigan_v2"
    #     # opts["lang"] = "en"
    #     # opts["lang_model"] = False
    #
    #     files = [
    #         "path/to/section_file.txt",
    #     ]
    #
    #     outdir = Path("output")
    #     outdir.mkdir(exist_ok=True)
    #     for file in files:
    #         print(f"Processing file {file}")
    #         file_name = f"{Path(file).stem}_{Path(opts.get('model')).name}{tag}.wav"
    #         output_file = outdir / file_name
    #         process_file(file, output_file, opts)
    #         print("Done!")
