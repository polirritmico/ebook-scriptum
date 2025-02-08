#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

# from src.dataclass import DocumentMetadata, Section
from src.document import Document

# from src.configuration import ScriptoriumConfiguration


# from bs4 import BeautifulSoup


class EpubExporter:
    source: Path | None = None
    DEFAULT_OUTPUT_FILENAME: str = "output.epub"

    def __init__(self):
        self.tmp_prefix = "scriptorium-export-tmp_"

    def set_options(self, config) -> None:
        if getattr(config, "output"):
            self.output = config.output

    def export(self, document: Document, output: Path) -> None:
        if document.source and document.source.exists():
            self.export_with_base_document(document, output)
        else:
            self.export_new_epub(document, output)

    # def split_dir_and_file(self, path: Path | None = None) -> (Path, Path):
    #     if not path:
    #         raise ValueError("Empty path")
    #
    #     if path.is_dir():
    #         dir = path
    #         file = Path(self.DEFAULT_OUTPUT_FILENAME)
    #     else:
    #         dir = path.parent
    #         file = path
    #
    #     return (dir, file)

    def export_with_base_document(self, document: Document, output: Path) -> None:
        # self.update_epub_metadata()
        with TemporaryDirectory(prefix=self.tmp_prefix) as temp_path_str:
            tmp_path = Path(temp_path_str)
            self.extract_epub(document.source, tmp_path)
            self.update_epub_section_files(document, tmp_path)
            self.write_epub(document, tmp_path)

    def update_epub_section_files(self, document: Document, tmp_dir: Path) -> None:
        for file, section in document.sections.items():
            new_content = document.get_content(file)
            target_path = self.unziped_target_path(section.filepath, tmp_dir)
            try:
                with open(target_path, "w", encoding="utf-8") as stream:
                    stream.write(new_content)
            except Exception:
                raise Exception(f"Error writing the file '{file}'")

    def unziped_target_path(self, section: Path, zip_dir: Path) -> Path:
        old_tmp_dir_root = section.parts.index("OEBPS")
        target_path = zip_dir / Path(*section.parts[old_tmp_dir_root:])
        return target_path

    def write_epub(self, output: Path, source_dir: Path) -> None:
        if not any(source_dir.iterdir()):
            raise FileNotFoundError(f"Can't access temp directory '{source_dir}'")

        files = [file for file in source_dir.rglob("*") if file.is_file()]
        with ZipFile(output, "w", ZIP_DEFLATED, compresslevel=9) as zip:
            for file in files:
                inzip_path = file.relative_to(source_dir)
                if file.name == "mimetype":
                    zip.write(str(file), str(inzip_path), compress_type=ZIP_STORED)
                else:
                    zip.write(str(file), str(inzip_path))

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
        text_files, metadata = [], []
        metadata_file = "content.opf"
        text_suffixes = {".xhtml", ".html"}

        for entry in path.rglob("*"):
            if entry.name == metadata_file:
                metadata = entry
            elif entry.suffix in text_suffixes:
                text_files.append(entry)

        self.text_files = text_files
        self.metadata_file = metadata
        return text_files, metadata

    def extract_epub(self, source: Path, target_path: Path) -> None:
        if any(element.is_dir() for element in target_path.iterdir()):
            raise FileExistsError(f"The epub extract dir is not empty: '{target_path}'")

        with ZipFile(source, "r") as stream:
            stream.extractall(target_path)

    def update_epub_metadata(self) -> None:
        raise NotImplementedError

    def export_new_epub(self, document: Document) -> None:
        raise NotImplementedError
