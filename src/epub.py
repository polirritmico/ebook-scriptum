#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

from src.document import Document


class EpubImporter:
    def load_data(self, source: Path) -> None:
        pass

    def generate_document(self) -> Document:
        pass

    def extract(self, source: Path, target_path: Path) -> None:
        if any(element.is_dir() for element in target_path.iterdir()):
            raise FileExistsError(f"The epub extract dir is not empty: '{target_path}'")

        self.temp_path = target_path
        with ZipFile(source, "r") as stream:
            stream.extractall(target_path)
