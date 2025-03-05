#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import ffmpeg


class AudioProcessor:
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
        self.tmp_register: list[str] = []


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
        self, wav_file: str, output_file: str, settings: dict | None = None
    ) -> None:
        if isinstance(wav_file, Path):
            wav_file = str(wav_file)
        if isinstance(output_file, Path):
            output_file = str(output_file)

        export_settings = settings or self.DEFAULT_EXPORT_SETTINGS
        audio = ffmpeg.input(wav_file)
        audio.output(output_file, **export_settings).run(overwrite_output=True)

    def make_temp_filename(self, input_file: str) -> str:
        tmp_idx = len(self.tmp_register) + 1
        tmp_filename = f"{input_file[:-4]}_temp{tmp_idx}.wav"
        self.tmp_register.append(tmp_filename)
        return tmp_filename
