#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.scriptorium import Scriptorium


def main():
    from src.coqui import CoquiTTS
    from src.simpletext import SimpleTextImporter

    input_files = [
        "files/test.txt",
    ]
    opts = {}

    scriptum = Scriptorium()
    text_to_speech = CoquiTTS()
    importer = SimpleTextImporter()

    # TODO: It seems odd this approach, shouldn't be all defined in the opts?
    # In that case, the scriptum should resolve this internally, so a higher
    # level function is required...
    # Input could be a list or a single file
    for file in input_files:
        local_opts = opts.copy()
        local_opts["input_files"] = file

        scriptum.set_importer(importer)
        scriptum.set_transmuters(text_to_speech)
        scriptum.set_options(local_opts)

        scriptum.load_data()
        scriptum.transmute()

        scriptum.validate_output()
        scriptum.export()


if __name__ == "__main__":
    main()
