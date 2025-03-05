#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime
from pathlib import Path

from num2words import num2words


class VittsTextProcessor:
    DEFAULT_LANG = "en"
    LOG_DIR = "logs/processed_text/"
    SYMBOLS = {
        "…": "...",
        "–": "-",
        "—": "-",
        "«": '"',
        "»": '"',
        "¿": '"',
        "?": '?"',
        "¡": '"',
        "!": '!"',
        ":": ".",  # : corrompe las frases
    }

    def replace_unhandled_symbols(self, line: str) -> str:
        for target, replacement in self.SYMBOLS.items():
            line = line.replace(target, replacement)
        return line

    def remove_double_quotes(self, line: str) -> str:
        return line.replace('""', '"')

    def add_missing_periods(self, line: str) -> str:
        pattern = r"[.!?…]$"
        if not re.search(pattern, line):
            return line + "."
        return line

    def convert_numbers_to_words(self, line: str, lang: str) -> str:
        line = re.sub(
            r"\d+", lambda match: num2words(int(match.group(0)), lang=lang), line
        )
        return line

    def apply_custom_replacement_dict(
        self, line: str, custom_dict: dict[str, str]
    ) -> str:
        for target, replacement in custom_dict.items():
            line = line.replace(target, replacement)
        return line

    def uppercase_first_letter(self, line: str) -> str:
        pattern = r"([a-záéíóúA-ZÁÉÍÓÚ])"
        line = re.sub(pattern, lambda char: char.group(1).upper(), line, 1)
        return line

    def store_generated_text(self, text: str, source_name: str = "") -> None:
        target_path = Path(self.LOG_DIR)
        target_path.mkdir(parents=True, exist_ok=True)

        if source_name:
            source_name = "_" + source_name
        basename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file = target_path / f"{source_name}{basename}.txt"

        file.write_text(text, encoding="utf-8")

    def join_short_lines(self, text: list[str], min_width: int = 20) -> None:
        prev_line: str | None = None
        lines_to_remove = []
        for line_number, line in enumerate(text):
            if prev_line:
                # TODO: Check the impact of this:
                prev_line.replace(".", ",")

                line = prev_line + " " + line
                text[line_number] = line
                prev_line = None

            line_width = len(line)
            if line_width <= min_width:
                prev_line = line
                lines_to_remove.append(line_number)

        if prev_line:
            text[-1] = prev_line + " " + text[-1]

        for line_to_remove in reversed(lines_to_remove):
            del text[line_to_remove]

    def process_text(
        self,
        raw_text: str,
        replacement_dict: dict[str, str] | None = None,
        opts: dict | None = None,
    ) -> str:
        """
        Apply all text filters and processors to improve the str send to the TTS

        :param raw_text: Unformated text.
        :param replacement_dict: Dict with strings to repalce `dict[old] = new`
        :param opts: Special options to control inner behaviour:
            - `lang`: en, es
            - `log` (`bool`): store the generated multiline string into `log/`

        :return: Multiline processed string
        """
        processed: list[str] = []
        lang = opts.get("lang") or self.DEFAULT_LANG

        for line in raw_text.splitlines():
            if not line:
                continue
            line = self.add_missing_periods(line)
            line = self.convert_numbers_to_words(line, lang)
            line = self.replace_unhandled_symbols(line)
            line = self.apply_custom_replacement_dict(line, replacement_dict)
            line = self.uppercase_first_letter(line)
            line = self.remove_double_quotes(line)
            processed.append(line)
        self.join_short_lines(processed, min_width=20)
        multiline_text = "\n\n".join(processed)

        log = opts.get("log")
        if log:
            if not isinstance(log, str | Path):
                log = self.LOG_DIR
            source_filename = opts.get("filename")
            self.store_generated_text(multiline_text, source_filename)

        return multiline_text
