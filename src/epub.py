#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

from src.document import Document


class EpubImporter:
    def load_data(self, source: Path) -> None:
        self.source_data = {}
        with TemporaryDirectory(suffix="scriptum_") as tmpdir:
            tmp_path = Path(tmpdir)
            self.extract(source, tmp_path)
            self.collect_section_files(tmp_path)

    def collect_section_files(self, path: Path) -> dict:
        files = [entry for entry in path.rglob("*") if entry.is_file()]
        return files

    def generate_document(self) -> Document:
        document = Document()
        return document

    def extract(self, source: Path, target_path: Path) -> None:
        if any(element.is_dir() for element in target_path.iterdir()):
            raise FileExistsError(f"The epub extract dir is not empty: '{target_path}'")

        self.temp_path = target_path
        with ZipFile(source, "r") as stream:
            stream.extractall(target_path)
