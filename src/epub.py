#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

from bs4 import BeautifulSoup

from src.document import Document


class EpubImporter:
    def __init__(self):
        self.collected_text_files = None
        self.collected_metadata_files = None

    def load_data(self, source: Path) -> None:
        self.source_data = {}
        with TemporaryDirectory(suffix="scriptum_") as tmpdir:
            tmp_path = Path(tmpdir)
            self.extract_epub(source, tmp_path)
            self.collect_text_and_metadata_files(tmp_path)
            self.collect_files_content()

    def collect_files_content(self) -> None:
        # TODO: read each collected file. Generate the corresponding soups?
        pass

    def generate_document(self) -> Document:
        # TODO: Not called
        document = Document()
        metadata = self.generate_metadata()
        sections = self.generate_sections()

        document.set_medatada(**metadata)
        document.set_sections(sections)
        return document

    def generate_metadata(self, metadata: list[str] = None) -> None:
        # TODO: implement: From the soups, extract the data
        if metadata is None:
            metadata = self.collected_metadata_files

    def generate_sections(self) -> dict[str, BeautifulSoup]:
        # TODO: implement: Create each section soup
        pass

    def extract_epub(self, source: Path, target_path: Path) -> None:
        if any(element.is_dir() for element in target_path.iterdir()):
            raise FileExistsError(f"The epub extract dir is not empty: '{target_path}'")

        self.temp_path = target_path
        with ZipFile(source, "r") as stream:
            stream.extractall(target_path)

    def collect_text_and_metadata_files(self, path: Path) -> (list[str], list[str]):
        text, metadata = [], []
        metadata_suffixes = {".opf", ".ncx"}
        text_suffixes = {".xhtml", ".html"}

        for entry in path.rglob("*"):
            if entry.suffix in metadata_suffixes:
                metadata.append(entry)
            elif entry.suffix in text_suffixes:
                text.append(entry)

        self.collected_text_files = text
        self.collected_metadata_files = metadata
        return text, metadata
