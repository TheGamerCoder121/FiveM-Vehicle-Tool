#!/usr/bin/env python3

from lxml import etree
from pathlib import Path
import sys

def analyze_vehicle_structure(file_path):
    """Analyze the XML structure in carcols.meta to find vehicle identifiers."""
    file_path = Path(file_path).expanduser()
    print(f"\nAnalyzing structure in {file_path}:")

    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(str(file_path), parser)
        root = tree.getroot()

        print("\nAnalyzing vehicle identifiers:")
        # Find all elements that contain vehicle identifiers
        kit_elements = root.findall(".//kitName")

        print("\nKit patterns found:")
        for kit in kit_elements:
            # Get the parent element that contains both kitName and id
            parent = kit.getparent()
            if parent is not None:
                id_elem = parent.find("id")
                if id_elem is not None:
                    print(f"\nKit: {kit.text}")
                    print(f"ID: {id_elem.attrib.get('value', 'NO_VALUE')}")
                    # Try to extract vehicle name from kitName
                    if '_' in kit.text:
                        vehicle_name = kit.text.split('_')[1]  # Assuming format like "990_vehiclename_modkit"
                        print(f"Extracted vehicle name: {vehicle_name}")

        # Find sirens section and analyze its structure
        sirens = root.find(".//sirens")
        if sirens is not None:
            siren_items = sirens.findall("Item")
            print(f"\nFound {len(siren_items)} siren items")
            # Look at comments in siren items to find vehicle identifiers
            for item in siren_items:
                # Get the comment text that might contain vehicle info
                comment = None
                for child in item.itersiblings(preceding=True):
                    if isinstance(child, etree._Comment):
                        comment = child.text
                        break
                if comment:
                    print(f"Siren comment: {comment}")

        print("\nSummary:")
        print(f"Total kitName elements: {len(kit_elements)}")
        if sirens is not None:
            print(f"Total siren items: {len(siren_items)}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    analyze_vehicle_structure("~/attachments/carcols.meta")
