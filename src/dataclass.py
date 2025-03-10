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
    title: str
    creator: str
    lang: str
    description: str
    source: Path | None = None
    spine: list[Path] | None = None
    toc: list[tuple[str, str]] | None = None
