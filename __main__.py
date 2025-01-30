#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.scriptorium import Scriptorium


def main():
    opts = {
        "input": "source_text",  # dir or file
        "input_handler": "SimpleTextImporter",
        "transmuters": ["Translator"],
        "output": "target_path",  # output dir
        "title": "Archivo de prueba",
        "creator": "Anónimo",
        "lang": "es",
    }

    scriptum = Scriptorium()
    scriptum.set_options(opts)
    scriptum.synthesize()
    scriptum.crystallize()


if __name__ == "__main__":
    main()
