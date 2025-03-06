#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil

import pytest

from src.processors.vitts_audio_processor import VittsAudioProcessor


@pytest.mark.skip(reason="Manual test")
def test_remove_inner_silences() -> None:
    source_case_file = "tests/files/audio/simple.wav"
    case = "tests/files/audio/inner_silences_output.wav"
    shutil.copy(source_case_file, case)

    processor = VittsAudioProcessor()
    processor.remove_inner_silences(case)


@pytest.mark.skip(reason="Manual test")
def test_add_wrap_silences() -> None:
    source_case_file = "tests/files/audio/simple.wav"
    case = "tests/files/audio/add_wrap_output.wav"
    shutil.copy(source_case_file, case)

    processor = VittsAudioProcessor()
    processor.add_wrap_silences(case)


@pytest.mark.skip(reason="Manual test")
def test_wav_to_mp3() -> None:
    input_file = "tests/files/audio/simple.wav"
    output_file = "tests/files/audio/output.mp3"

    processor = VittsAudioProcessor()
    processor.wav_to_mp3(input_file, output_file)


@pytest.mark.skip(reason="Manual test")
def test_full_process() -> None:
    input_file = "tests/files/audio/simple.wav"
    output_file = "tests/files/audio/output.mp3"

    processor = VittsAudioProcessor()
    processor.run(input_file, output_file)
