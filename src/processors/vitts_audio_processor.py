#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import ffmpeg


class AudioProcessor:
    def remove_inner_silences(self, wav_file: str | Path) -> str:
        pass

    def add_wrap_silences(self, wav_file: str | Path) -> str:
        pass

    def wav_to_mp3(self, wav_file: str, output_file: str, settings: dict) -> None:
        pass
