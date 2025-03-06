#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pathlib import Path

import ffmpeg


class VittsAudioProcessor:
    DEFAULT_EXPORT_SETTINGS = {
        "codec": "libmp3lame",
        "ab": "64k",
        "ar": "22050",
        "ac": 1,
    }
    DEFAULT_INNER_SILENCE_FILTER = {
        "stop_periods": -1,
        "stop_threshold": "-40dB",
        "stop_duration": 0.8,
    }
    DEFAULT_WRAP_FILTER = {"pad_dur": 1}

    def __init__(self):
        self.tmp_register: list[Path] = []

    def run(
        self,
        input_file: str | Path,
        output_file: str | Path | None = None,
        opts: dict | None = None,
    ) -> None:
        opts_remove_inner = opts and opts.get("remove_inner")
        opts_add_wrap = opts and opts.get("add_wrap")
        opts_codec = opts and opts.get("codec")

        if output_file is None:
            output_file = Path(input_file).with_suffix(".mp3")

        audio_file = self.remove_inner_silences(input_file, opts_remove_inner)
        audio_file = self.add_wrap_silences(audio_file, opts_add_wrap)
        self.wav_to_mp3(audio_file, output_file, opts_codec)

        self.clean_temp_files()

    def remove_inner_silences(
        self, wav_file: str | Path, filter: dict | None = None
    ) -> str:
        if isinstance(wav_file, Path):
            wav_file = str(wav_file)
        tmp_file = self.make_temp_filename(wav_file)
        filter = filter or self.DEFAULT_INNER_SILENCE_FILTER

        stream = ffmpeg.input(wav_file).filter("silenceremove", **filter)
        stream.output(tmp_file).run(overwrite_output=True)
        return tmp_file

    def add_wrap_silences(
        self, wav_file: str | Path, filter: dict | None = None
    ) -> str:
        wrap_duration = "1s"

        if isinstance(wav_file, Path):
            wav_file = str(wav_file)
        tmp_file = self.make_temp_filename(wav_file)

        stream = (
            ffmpeg.input(wav_file)
            .filter("adelay", delays=wrap_duration)
            .filter("apad", pad_dur=wrap_duration)
        )
        stream.output(tmp_file).run(overwrite_output=True)
        return tmp_file

    def wav_to_mp3(
        self,
        wav_file: str | Path,
        output_file: str | Path,
        settings: dict | None = None,
    ) -> None:
        if isinstance(wav_file, Path):
            wav_file = str(wav_file)
        if isinstance(output_file, Path):
            output_file = str(output_file)

        export_settings = settings or self.DEFAULT_EXPORT_SETTINGS
        audio = ffmpeg.input(wav_file)
        audio.output(output_file, **export_settings).run(overwrite_output=True)

    def make_temp_filename(self, original_filename: str) -> str:
        original_filename = re.sub(r"_temp\d+", "", original_filename)
        tmp_idx = len(self.tmp_register) + 1
        tmp_filename = f"{original_filename[:-4]}_temp{tmp_idx}.wav"
        self.tmp_register.append(Path(tmp_filename))
        return tmp_filename

    def clean_temp_files(self) -> None:
        for tmp_file in self.tmp_register:
            if "temp" in tmp_file.name:
                tmp_file.unlink()
