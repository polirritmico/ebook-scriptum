#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import ffmpeg


class AudioProcessor:
    DEFAULT_INNER_SILENCE_FILTER = {
        "stop_periods": -1,
        "stop_threshold": "-40dB",
        "stop_duration": 0.8,

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

    def make_temp_filename(self, input_file: str) -> str:
        tmp_idx = len(self.tmp_register) + 1
        tmp_filename = f"{input_file[:-4]}_temp{tmp_idx}.wav"
        self.tmp_register.append(tmp_filename)
        return tmp_filename
