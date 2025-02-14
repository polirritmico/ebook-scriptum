#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.models.llama3_2 import ModelLlama3_2
from src.transmuters.ollama_translator import OllamaTranslator


@pytest.fixture
def translator() -> None:
    translator = OllamaTranslator()
    translator.set_model(None)
    return translator


def test_ollama_basic_translation() -> None:
    case = "Hello, World!"
    expected = ["hola", "mundo", "!"]

    translator = OllamaTranslator()
    translator.set_model(ModelLlama3_2())
    output = translator.translate_text(case)

    for expected_word in expected:
        assert expected_word in output.lower()


def test_translation_with_tags(translator) -> None:
    case = "This paragraph has <b>bold</b> text."
    expected = ["párrafo", "<b>", "</b>"]

    output = translator.translate_text(case)

    for expected_word in expected:
        assert expected_word in output.lower()


def test_translation_with_link(translator) -> None:
    case = '<p class="bar foo" style="color:red">This paragraph has a <a href="target">inner</a> link.</p>'
    expected = '<a href="target">'

    output = translator.translate_text(case)

    assert expected in output.lower()


def test_response_validator(translator) -> None:
    case1 = "aaa bbbb 12345"
    case2 = "a 整,没有a额"
    case3 = "aaaa 应当aaa"

    case4 = "a 某些地方ch"
    case5 = "aaa 出了翻译chars"
    case6 = "<p>转向个体特征的棋手。"
    case7 = "外的的部"
    case8 = "a 整，没有额"
    case9 = "的西班aaa 牙语翻a 译应该是 a"
    case10 = "办公室"
    case11a = "aaaa 应  当aaa"
    case11b = "aaaa 应 当aaa"

    assert translator.model.response_validator(case1, case1)
    assert translator.model.response_validator(case2, case2)
    assert translator.model.response_validator(case3, case3)
    assert not translator.model.response_validator(case4, case4)
    assert not translator.model.response_validator(case5, case5)
    assert not translator.model.response_validator(case6, case6)
    assert not translator.model.response_validator(case7, case7)
    assert not translator.model.response_validator(case8, case8)
    assert not translator.model.response_validator(case9, case9)
    assert not translator.model.response_validator(case10, case10)
    assert not translator.model.response_validator(case11a, case11b)


def test_validate_translation(translator) -> None:
    case = "aaaa"
    expected = "aaa a"
    expected_calls = 4

    attempts = 0

    def fake_send_prompt(_):
        nonlocal attempts
        attempts += 1
        return "aa  aa" if attempts < 4 else "aaa a"

    translator.send_prompt = fake_send_prompt
    output = translator.translate_text(case)

    assert expected_calls == attempts
    assert output == expected


def test_bad_response(translator) -> None:
    case = "aaaa"
    expected = "aa  aa"
    expected_calls = 10

    attempts = 0

    def fake_send_prompt_corrupted(_):
        nonlocal attempts
        attempts += 1
        return "aa  aa"

    translator.send_prompt = fake_send_prompt_corrupted
    output = translator.translate_text(case)

    assert expected_calls == attempts
    assert output == expected
