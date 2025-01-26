#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SectionMetadata:
    content: any  # TODO: Beautiful Soup
    filepath: Path
    lang: str
    order: int
    title: str


@dataclass
class DocumentMetadata:
    creator: any  # TODO: Beautiful Soup
    description: str  # TODO: bs4 tag
    lang: str
    title: str
    manifest: str
    spine: any  # TODO: bs4 tag
