#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.scriptorium import Scriptorium


def main():
    opts = {
        "input": "source_file",
        "output": "output_dir",
        "importer": "SimpleTextImporter",
        "transmuter": ("OllamaTranslator", ""),
        "exporter": "EpubExporter",
    }

    scriptum = Scriptorium()
    scriptum.setup(opts)
    scriptum.load_data()
    scriptum.transmute()
    scriptum.export()


if __name__ == "__main__":
    main()
