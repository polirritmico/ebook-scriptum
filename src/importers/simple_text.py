#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

import chardet
from bs4 import BeautifulSoup
from langdetect import detect as langdetect

from src.dataclass import DocumentMetadata, Section
from src.document import Document


class SimpleTextImporter:
    """ImporterHandler subscriptor.

    It infers the title and author by the filename: `<author> - <title>.<ext>`
    """

    def __init__(self):
        self.sources: list[Path] = None
        self.content: list[str] = []
        self.metadata: list[DocumentMetadata] | None = None

    # TODO: add support for dirs
    def load_data(self, sources: list[Path]) -> None:
        if not sources:
            raise ValueError("Missing source")
        if len(sources) > 1:
            raise NotImplementedError("Not implemented support for multiple files")
        for source in sources:
            try:
                encoding = self.detect_encoding(source)
                content = source.read_text(encoding=encoding)
                self.content.append(content)
            except Exception as e:
                raise Exception(f"Error reading the file {source}: \n{e}")
        self.sources = sources

    def generate_document(self) -> Document:
        if not self.content:
            raise ValueError("Empty content. Try load_data() first.")

        document = Document()
        metadata = self.build_metadata()
        sections = self.build_sections()

        document.set_medatada(metadata)
        # TODO: Add functionality to handle multiple files
        document.set_sections(sections)
        return document

    def build_metadata(self) -> DocumentMetadata:
        # TODO: Redundant?
        if not self.content:
            raise ValueError("Empty content. Try load_data() first.")

        # TODO: Handle multiple files
        title, creator = self.get_creator_and_title_from_filename(self.sources[0])
        description = f"'{title}' by {creator}."
        lang_code = self.infer_content_lang()

        metadata = DocumentMetadata(
            title=title,
            creator=creator,
            lang=lang_code,
            description=description,
            # TODO: Add support for multiple files
            source=self.sources[0],
        )
        self.metadata = metadata
        return metadata

    def get_creator_and_title_from_filename(self, source: Path) -> (str, str):
        """Return (title, creator) extracted from the given filename."""

        # source -> <author> - <title>
        # TODO: Add support for multiple files
        source = source if source else self.sources[0]
        clean_filename: str = source.stem.replace("_", " ")
        parsed_filename: list[str] = clean_filename.split(" - ")
        if len(parsed_filename) > 1:
            creator = parsed_filename[0]
            title = parsed_filename[1]
        else:
            creator = "Author"
            title = parsed_filename[0]

        return title, creator

    def build_sections(self) -> dict[str, Section]:
        soup = self.make_html_soup()
        section = Section(
            content=soup,
            title=self.metadata.title,
            filepath=self.sources,
            lang=self.metadata.lang,
            order=0,
            text=self.content,
        )

        # TODO: Add support for multiple sources files
        return {self.sources[0].name: section}

    def make_html_soup(self) -> BeautifulSoup:
        soup = BeautifulSoup(features="html.parser")
        html = soup.new_tag("html")
        soup.append(html)
        body = soup.new_tag("body")
        html.append(body)

        # TODO: Add support for multiple content files
        content = self.content[0].split("\n")
        for raw_line in content:
            line = raw_line.strip()
            if line:
                p = soup.new_tag("p")
                p.string = line
                body.append(p)

        return soup

    def infer_content_lang(self, content: str | None = None) -> str:
        # TODO: Add support for multiple content files
        content = content if content else self.content[0]
        if not content:
            raise ValueError("Missing content. Try load_data first")

        detected = langdetect(content)
        if detected != "unknown":
            return detected

        return self.get_system_lang()

    def get_system_lang(self) -> str:
        failback = "en"

        system_locale = None
        for env in ["LANG", "LANGUAGE", "LC_ALL"]:
            system_locale = os.getenv(env)
            if system_locale:
                break

        if not system_locale:
            system_locale = failback
        system_lang = system_locale.split("_")[0]

        return system_lang or failback

    def detect_encoding(self, source: Path) -> str:
        default = "utf-8"
        with open(source, "rb") as stream:
            detector = chardet.universaldetector.UniversalDetector()
            for line in stream:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        return detector.result.get("encoding", default).lower()
