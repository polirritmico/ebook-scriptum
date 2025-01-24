#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from src.section import Section


class Document:
    def __init__(self):
        self.sections: list[Section] = []
        self.source_path: str = ""
