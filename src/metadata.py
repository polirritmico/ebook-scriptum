#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup, Tag


@dataclass
class SectionMetadata:
    content: BeautifulSoup
    filepath: Path
    lang: str
    order: int
    title: str


@dataclass
class DocumentMetadata:
    creator: str
    description: str
    lang: str
    title: str
    spine: list[Path] = None
