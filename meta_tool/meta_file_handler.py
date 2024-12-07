#!/usr/bin/env python3

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from lxml import etree

class MetaFileHandler:
    """Handles XML file operations for GTA V meta files."""

    def __init__(self):
        self.parser = etree.XMLParser(remove_blank_text=True)

    def load_meta_file(self, file_path: str) -> Tuple[etree._Element, str]:
        """
        Load and parse a meta file.

        Args:
            file_path: Path to the meta file

        Returns:
            Tuple of (XML root element, original XML string)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            root = etree.fromstring(xml_content.encode(), self.parser)
            return root, xml_content
        except (IOError, etree.ParseError) as e:
            raise ValueError(f"Failed to load meta file {file_path}: {str(e)}")

    def save_meta_file(self, file_path: str, root: etree._Element) -> None:
        """
        Save XML content back to file.

        Args:
            file_path: Path to save the file
            root: XML root element
        """
        try:
            xml_content = etree.tostring(
                root,
                pretty_print=True,
                encoding='utf-8',
                xml_declaration=True
            ).decode()

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
        except IOError as e:
            raise ValueError(f"Failed to save meta file {file_path}: {str(e)}")

    def backup_files(self, files: list[str]) -> None:
        """
        Create backups of the specified files.

        Args:
            files: List of file paths to backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"backups_{timestamp}")
        backup_dir.mkdir(exist_ok=True)

        for file_path in files:
            file_path = Path(file_path)
            if not file_path.exists():
                raise ValueError(f"File not found: {file_path}")

            backup_path = backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)

    def validate_meta_file(self, file_path: str) -> bool:
        """
        Validate that the file is a properly formatted meta file.

        Args:
            file_path: Path to the meta file to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            root, _ = self.load_meta_file(file_path)
            # Basic validation - check for expected root element
            return root.tag in ['CVehicleModelInfoVarGlobal', 'CVehicleModelInfoVariation']
        except Exception:
            return False
