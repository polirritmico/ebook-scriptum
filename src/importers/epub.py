#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from bs4 import BeautifulSoup

from src.dataclass import DocumentMetadata, Section
from src.document import Document


class EpubImporter:
    sources: list[Path] | None = None

    def __init__(self):
        self.text_files = None
        self.metadata_file = None
        self.text_files_content = None
        self.metadata_file_content = None
        self.parsed_sections = None
        self.temp_path = None
        self.sources = None

    def set_options(self, options: dict) -> None:
        raise NotImplementedError()

    def load_data(self, sources: list[Path]) -> None:
        if len(sources) > 1:
            raise NotImplementedError("Not implement support for multiple epubs")

        source = sources[0]
        if not source:
            raise ValueError("load_data: Empty source path")
        if not isinstance(source, Path):
            raise TypeError(f"source should be a Path object: {type(source)}")

        self.sources = [source]
        with TemporaryDirectory(prefix="scriptum_") as tmpdir:
            tmp_path = Path(tmpdir)
            self.extract_epub(source, tmp_path)
            self.collect_metadata_and_text_files(tmp_path)
            self.collect_files_data()

    def generate_document(self) -> Document:
        document = Document()
        metadata = self.parse_document_metadata()
        sections = self.parse_sections(metadata)

        document.set_medatada(metadata)
        document.set_sections(sections)
        return document

    def parse_sections(self, metadata: DocumentMetadata) -> dict[str, Section]:
        sections = {}
        for order, filepath in enumerate(metadata.spine):
            raw_data = self.text_files_content[filepath]

            extension = filepath.suffix[1:]
            if extension == "xhtml":
                extension = "lxml-xml"
            elif extension == "html":
                extension = "lxml"
            content = BeautifulSoup(raw_data, extension)

            section_metadata = Section(
                content=content,
                title=self.get_section_title(content) or filepath.stem,
                filepath=self.get_section_inzip_path(filepath),
                lang=self.get_section_lang(content) or metadata.lang,
                order=order,
                text=content.get_text(separator="\n"),
            )
            sections[filepath.name] = section_metadata

        self.parsed_sections = sections
        return sections

    def get_section_inzip_path(self, path: Path) -> Path:
        root_index = path.parts.index("OEBPS")
        inzip_path = Path(*path.parts[root_index:])
        return inzip_path

    def get_section_lang(self, content: BeautifulSoup) -> str:
        lang = content.html.get("xml:lang")
        return lang

    def get_section_title(self, content: BeautifulSoup) -> str:
        title = content.get("title", "")

        if not title:
            title_tag = content.find("title")
            title = title_tag.get_text() if title_tag else ""

        if not title:
            for i in range(1, 7):
                try:
                    htag = content.html.body.find(f"h{i}")
                    title = htag.get_text() or htag.get("title") or ""
                    if title:
                        return title
                except Exception:
                    title = ""

        if not title:
            og_title = content.find("meta", attrs={"property": "og:title"})
            title = og_title.get("content") if og_title else ""

        # if not title:
        #     first_three_paragraphs = content.find_all("p")[:3]
        #     paragraph = " ".join(p.get_text() for p in first_three_paragraphs)
        #     title = " ".join(paragraph.split()[:3]) or ""

        # if not title:
        #     beginning = content.get_text().split()[:3]
        #     title = " ".join(beginning)

        return title

    def parse_document_metadata(self) -> DocumentMetadata:
        if self.metadata_file_content is None:
            raise ValueError("No metadata_file_content. Try collect_files_data() first")
        if self.toc_file_content is None:
            raise ValueError("No toc_file_content. Try collect_files_data()first")

        soup = BeautifulSoup(self.metadata_file_content, "xml")
        metadata = DocumentMetadata(
            title=self.get_text_from_soup_tag("dc:title", soup),
            creator=self.get_text_from_soup_tag("dc:creator", soup),
            lang=self.get_text_from_soup_tag("dc:language", soup),
            description=self.get_text_from_soup_tag("dc:description", soup),
            source=self.sources,
            spine=self.get_sections_in_order_from_soup(soup),
            toc=self.get_section_names_from_toc_file(self.toc_file_content),
        )

        return metadata

    def get_sections_in_order_from_soup(self, soup: BeautifulSoup) -> list[Path]:
        if not self.text_files:
            raise ValueError("Missing text_files. Try collect_metadata_and_text_files")
        if not soup:
            raise ValueError("Missing soup")

        ordered_section_files = []
        spine = [itemref["idref"] for itemref in soup.find_all("itemref")]
        manifest = {item["id"]: item["href"] for item in soup.find_all("item")}

        # Cross-reference: The spine has the order, the manifest the actual file
        for section_name in spine:
            full_section_name = manifest.get(section_name, "")
            section_file = full_section_name.rsplit("/", 1)[-1]
            if not section_file:
                continue

            # TODO: Refactor. An "inner for" each time?
            for readed_file in self.text_files:
                if readed_file.name == section_file:
                    ordered_section_files.append(readed_file)
                    break

        return ordered_section_files

    def get_text_from_soup_tag(self, tag: str, soup: BeautifulSoup) -> str | None:
        tag_element = soup.find(tag)
        if tag_element and hasattr(tag_element, "text"):
            return tag_element.get_text()

    def get_section_names_from_toc_file(
        self, source: str | None = None
    ) -> tuple[str, str]:
        source = source or self.toc_file_content
        if not source:
            raise ValueError("Not loaded content.opf. Try load_document()")

        soup = BeautifulSoup(source, "xml")
        nav_point = soup.find("navMap")
        text_tags = [tag.text for tag in nav_point.find_all("text")]
        content_tags = [tag.get("src") for tag in nav_point.find_all("content")]

        toc = []
        for filename, title in zip(content_tags, text_tags):
            entry = (filename, title)
            toc.append(entry)
        return toc

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

        with open(self.toc_file, "r", encoding="utf-8") as stream:
            raw_data = stream.read()
            self.toc_file_content = raw_data

    def collect_metadata_and_text_files(self, path: Path) -> (list[str], str):
        text_files = []
        metadata_file = "content.opf"
        toc_file = "toc.ncx"
        text_suffixes = {".xhtml", ".html"}

        for entry in path.rglob("*"):
            if entry.name == metadata_file:
                metadata = entry  # TODO: What if more than one file is found?
            elif entry.name == toc_file:
                toc = entry
            elif entry.suffix in text_suffixes:
                text_files.append(entry)

        # TODO: All epubs have metadata and toc files?
        assert metadata, "Missing content.opf"
        assert toc, "Missing toc.ncx"

        self.text_files = text_files
        self.metadata_file = metadata
        self.toc_file = toc
        return text_files, metadata

    def extract_epub(self, source: Path, target_path: Path) -> None:
        if any(element.is_dir() for element in target_path.iterdir()):
            raise FileExistsError(f"The epub extract dir is not empty: '{target_path}'")

        self.temp_path = target_path
        with ZipFile(source, "r") as stream:
            stream.extractall(target_path)
