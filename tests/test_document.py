#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.document import Document, Section


def test_parse_sections() -> None:
    case = {
        "file1": Section(soup1, path1, "es", 0, "File 1"),
        "file2": Section(soup2, path2, "es", 1, "File 2"),
    }
    doc = Document()
    doc.set_sections(case)

    output = doc.sections["file1"].soup1
