#!/usr/bin/env python3

"""
ConflictResolver module for handling ID conflicts in GTA V FiveM meta files.

This module provides functionality to resolve ID conflicts in both carcols.meta
and carvariations.meta files. It can handle both single vehicle and batch
processing modes.

Example:
    resolver = ConflictResolver('carcols.meta', 'carvariations.meta')

    # Process single vehicle
    changes = resolver.resolve_carcols_conflicts('24valor18sedan')

    # Process all vehicles
    changes = resolver.resolve_modkit_conflicts()

Note:
    - IDs are randomly generated within the 2-6 digit range
    - All changes are synchronized between both meta files
    - Backups are created automatically before modifications
"""

import logging
from typing import Optional, Set, Dict, List, Tuple
from pathlib import Path
from lxml import etree

from .meta_file_handler import MetaFileHandler
from .id_generator import IDGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ConflictResolver:
    """Resolves ID conflicts in GTA V meta files."""

    def __init__(self, carcols_path: str, carvariations_path: str):
        self.file_handler = MetaFileHandler()
        self.carcols_path = Path(carcols_path)
        self.carvariations_path = Path(carvariations_path)

        # Load and validate files
        self.carcols_root, _ = self.file_handler.load_meta_file(str(carcols_path))
        self.carvariations_root, _ = self.file_handler.load_meta_file(str(carvariations_path))

        # Initialize ID generator with existing IDs
        self.id_generator = IDGenerator(self.get_existing_ids())

    def get_existing_ids(self) -> Set[int]:
        """Collect all existing IDs from both meta files."""
        ids = set()

        # Collect from carcols.meta
        for id_elem in self.carcols_root.findall(".//id"):
            if 'value' in id_elem.attrib:
                ids.add(int(id_elem.attrib['value']))

        # Collect from carvariations.meta
        for siren in self.carvariations_root.findall(".//sirenSettings"):
            if 'value' in siren.attrib:
                ids.add(int(siren.attrib['value']))

        return ids

    def resolve_carcols_conflicts(self, vehicle_name: Optional[str] = None) -> Dict[str, List[Tuple[str, str]]]:
        """
        Resolve carcols ID conflicts for specified vehicle or all vehicles.

        Args:
            vehicle_name: Optional name of specific vehicle to process

        Returns:
            Dictionary of changes made {type: [(old_value, new_value)]}
        """
        changes = {'carcols': [], 'variations': []}
        logger.debug(f"Starting carcols conflict resolution for vehicle: {vehicle_name if vehicle_name else 'all'}")

        # Find all Items in carvariations.meta that have sirenSettings
        items = self.carvariations_root.findall(".//variationData/Item")
        logger.debug(f"Found {len(items)} Items in carvariations.meta")

        for item in items:
            # Check if this Item is for our vehicle
            if vehicle_name and not self._is_vehicle_element(item, vehicle_name):
                continue

            # Find sirenSettings directly under this Item
            siren_settings = item.findall("sirenSettings")
            if siren_settings:
                logger.debug(f"Found {len(siren_settings)} sirenSettings elements")
                for siren in siren_settings:
                    if 'value' not in siren.attrib:
                        continue

                    old_id = siren.attrib['value']
                    new_id = str(self.id_generator.generate_carcols_id())
                    logger.debug(f"Replacing sirenSettings ID {old_id} with {new_id}")

                    # Update sirenSettings in carvariations.meta
                    siren.attrib['value'] = new_id
                    changes['variations'].append((old_id, new_id))

                    # Find and update corresponding id in carcols.meta
                    for id_elem in self.carcols_root.findall(".//id"):
                        if id_elem.attrib.get('value') == old_id:
                            id_elem.attrib['value'] = new_id
                            changes['carcols'].append((old_id, new_id))
                            logger.debug(f"Updated corresponding ID in carcols.meta")

        # Save changes if any were made
        if changes['carcols'] or changes['variations']:
            self.file_handler.save_meta_file(str(self.carcols_path), self.carcols_root)
            self.file_handler.save_meta_file(str(self.carvariations_path), self.carvariations_root)
            logger.debug("Changes saved to both files")

        return changes

    def resolve_modkit_conflicts(self, vehicle_name: Optional[str] = None) -> Dict[str, List[Tuple[str, str]]]:
        """
        Resolve modkit ID conflicts for specified vehicle or all vehicles.

        Args:
            vehicle_name: Optional name of specific vehicle to process

        Returns:
            Dictionary of changes made {type: [(old_value, new_value)]}
        """
        changes = {'carcols': [], 'variations': []}

        # Process modkits in carcols.meta
        for kit_elem in self.carcols_root.findall(".//kitName"):
            if vehicle_name and not self._is_vehicle_element(kit_elem, vehicle_name):
                continue

            old_kit_name = kit_elem.text
            if not old_kit_name or '_modkit' not in old_kit_name:
                continue

            # Extract the old ID from the kit name
            old_id = old_kit_name.split('_')[0]
            new_id = str(self.id_generator.generate_modkit_id())

            # Update kitName
            new_kit_name = old_kit_name.replace(old_id, new_id, 1)
            kit_elem.text = new_kit_name
            changes['carcols'].append((old_kit_name, new_kit_name))

            # Update corresponding id value
            parent = kit_elem.getparent()
            if parent is not None:
                id_elem = parent.find("id")
                if id_elem is not None and id_elem.attrib.get('value') == old_id:
                    id_elem.attrib['value'] = new_id

            # Update corresponding Item in carvariations.meta
            for item in self.carvariations_root.findall(".//kits/Item"):
                if item.text == old_kit_name:
                    item.text = new_kit_name
                    changes['variations'].append((old_kit_name, new_kit_name))

        # Save changes
        self.file_handler.save_meta_file(str(self.carcols_path), self.carcols_root)
        self.file_handler.save_meta_file(str(self.carvariations_path), self.carvariations_root)

        return changes

    def _is_vehicle_element(self, element: etree._Element, vehicle_name: str) -> bool:
        """
        Check if an XML element belongs to the specified vehicle.

        Args:
            element: XML element to check
            vehicle_name: Name of the vehicle to match

        Returns:
            bool: True if element belongs to vehicle, False otherwise
        """
        # Check kitName elements
        kit_name = element.find(".//kitName")
        if kit_name is not None and kit_name.text:
            # Extract vehicle name from kitName pattern (e.g., "680357_24valor18sedan_modkit")
            parts = kit_name.text.split('_')
            if len(parts) >= 2:
                element_vehicle = parts[1]
                return vehicle_name.lower() in element_vehicle.lower()

        # Check kits/Item elements
        kits = element.find(".//kits")
        if kits is not None:
            for kit_item in kits.findall("Item"):
                if kit_item.text:
                    parts = kit_item.text.split('_')
                    if len(parts) >= 2:
                        element_vehicle = parts[1]
                        return vehicle_name.lower() in element_vehicle.lower()

        return False
