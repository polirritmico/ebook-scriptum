#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

from bs4 import BeautifulSoup

from src.document import Document
from src.metadata import DocumentMetadata, SectionMetadata


class EpubImporter:
    def __init__(self):
        self.text_files = None
        self.metadata_file = None
        self.text_files_content = None
        self.metadata_file_content = None

    def load_data(self, source: Path) -> None:
        self.source_data = {}
        with TemporaryDirectory(suffix="scriptum_") as tmpdir:
            tmp_path = Path(tmpdir)
            self.extract_epub(source, tmp_path)
            self.collect_metadata_and_text_files(tmp_path)
            self.collect_files_data()

    def generate_document(self) -> Document:
        # TODO: Not called
        document = Document()
        metadata = self.parse_document_metadata()
        sections = self.parse_sections(metadata)

        document.set_medatada(metadata)
        document.set_sections(sections)
        return document

    def parse_sections(self, metadata: dict) -> dict[str, SectionMetadata]:
        sections = {}
        ordered_sections = self.get_sections_in_order(metadata)
        for order, filepath in enumerate(ordered_sections):
            raw_data = self.text_files_content[filepath]

            extension = filepath.suffix[1:]
            if extension == "xhtml":
                extension = "xml"
            content = BeautifulSoup(raw_data, extension)

            section_metadata = SectionMetadata(
                content=content,
                filepath=filepath,
                lang=self.get_section_lang(content),
                order=order,
                title=self.get_section_title(content),
            )
            sections[filepath.name] = section_metadata

        self.parsed_sections = sections
        return sections

    def get_section_lang(self, content) -> str:
        # TODO: if not defined use the metadata. If not defined use default?
        lang = content.html.get("xml:lang")
        return lang

    def get_section_title(self, content) -> str:
        title = content.get("title")
        if not title:
            title_tag = content.find("title")
            title = title_tag.get_text() if title_tag else title
        if not title:
            try:
                title = content.html.body.find("h1").get_text()
            except Exception:
                title = "NONE"
        return title

    def get_sections_in_order(self, metadata: DocumentMetadata) -> list[str]:
        ordered_sections = []
        spine = metadata.spine.find_all("itemref")
        for section in spine:
            id = section.get("idref")
            for file in self.text_files:
                if file.name == id:
                    ordered_sections.append(file)
                    break

        return ordered_sections

    def parse_document_metadata(self) -> DocumentMetadata:
        if self.metadata_file_content is None:
            raise ValueError("No metadata_file_content. Try collect_files_data() first")

        soup = BeautifulSoup(self.metadata_file_content, "xml")
        metadata = DocumentMetadata(
            creator=self.get_text_from_soup_tag("dc:creator", soup),
            description=self.get_text_from_soup_tag("dc:description", soup),
            lang=self.get_text_from_soup_tag("dc:language", soup),
            title=self.get_text_from_soup_tag("dc:title", soup),
            manifest=soup.find("manifest"),
            spine=soup.find("spine"),
        )

        return metadata

    def get_text_from_soup_tag(self, tag: str, soup: BeautifulSoup) -> str | None:
        tag_element = soup.find(tag)
        if tag_element and hasattr(tag_element, "text"):
            return tag_element.get_text()

    def collect_files_data(self) -> None:
        if self.metadata_file is None or self.text_files is None:
            raise ValueError("Not collected files. Try load_data() first.")

        self.text_files_content = {}
        for file in self.text_files:
            with open(file, "r", encoding="utf-8") as stream:
                raw_data = stream.read()
                self.text_files_content[file] = raw_data

        with open(self.metadata_file, "r", encoding="utf-8") as stream:
            raw_data = stream.read()
            self.metadata_file_content = raw_data

    def collect_metadata_and_text_files(self, path: Path) -> (list[str], str):
        text, metadata = [], []
        metadata_file = "content.opf"
        text_suffixes = {".xhtml", ".html"}

        for entry in path.rglob("*"):
            if entry.name == metadata_file:
                metadata = entry
            elif entry.suffix in text_suffixes:
                text.append(entry)

        self.text_files = text
        self.metadata_file = metadata
        return text, metadata

    def extract_epub(self, source: Path, target_path: Path) -> None:
        if any(element.is_dir() for element in target_path.iterdir()):
            raise FileExistsError(f"The epub extract dir is not empty: '{target_path}'")

        self.temp_path = target_path
        with ZipFile(source, "r") as stream:
            stream.extractall(target_path)
