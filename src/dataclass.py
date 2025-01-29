#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup


@dataclass
class Section:
    content: BeautifulSoup
    title: str
    filepath: Path
    lang: str
    order: int
    text: str | None = None


@dataclass
class DocumentMetadata:
    creator: str
    description: str
    lang: str
    title: str
    spine: list[Path] | None = None
    source: Path | None = None
