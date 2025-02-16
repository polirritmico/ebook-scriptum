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
        if len(document.source) > 1:
            raise NotImplementedError("Not implemented export for more than 1 epub")
        source = document.source[0]
        if source and source.exists():
            self.export_with_base_document(document, output)
        else:
            self.export_new_epub(document, output)

    def export_with_base_document(self, document: Document, output: Path) -> None:
        with TemporaryDirectory(prefix=self.tmp_prefix) as temp_path_str:
            tmp_path = Path(temp_path_str)
            self.extract_epub(document.source, tmp_path)
            # self.update_epub_metadata()
            self.update_epub_section_files(document, tmp_path)
            self.write_epub(output, tmp_path)

    def update_epub_section_files(self, document: Document, tmp_dir: Path) -> None:
        for file, section in document.sections.items():
            new_content = document.get_content(file)
            target_path = tmp_dir / section.filepath
            try:
                with open(target_path, "w", encoding="utf-8") as stream:
                    stream.write(new_content)
            except Exception:
                raise Exception(f"Error writing the file '{file}'")

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

    def extract_epub(self, source: list[Path], target_path: Path) -> None:
        if len(source) > 1:
            raise NotImplementedError("Not implemented support for more than 1 epub")
        source = source[0]

        if any(element.is_dir() for element in target_path.iterdir()):
            raise FileExistsError(f"The epub extract dir is not empty: '{target_path}'")

        with ZipFile(source, "r") as stream:
            stream.extractall(target_path)

    def update_epub_metadata(self) -> None:
        raise NotImplementedError

    def export_new_epub(self, document: Document) -> None:
        raise NotImplementedError
