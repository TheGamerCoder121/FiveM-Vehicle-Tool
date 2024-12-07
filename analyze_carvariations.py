#!/usr/bin/env python3

from lxml import etree
from pathlib import Path
import sys

def analyze_vehicle_structure(file_path):
    """Analyze the XML structure around vehicle items and sirenSettings."""
    file_path = Path(file_path).expanduser()
    print(f"\nAnalyzing vehicle structure in {file_path}:")

    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(str(file_path), parser)
        root = tree.getroot()

        print("\nListing all vehicle Items with their names and sirenSettings:")
        items = root.findall(".//variationData/Item")
        for item in items:
            name = item.attrib.get('name', 'NO_NAME')
            siren_settings = item.findall("sirenSettings")
            if siren_settings:
                print(f"\nVehicle Item name: '{name}'")
                print("sirenSettings values:")
                for siren in siren_settings:
                    print(f"  value: {siren.attrib.get('value', 'NO_VALUE')}")

        # Print summary
        print("\nSummary:")
        print(f"Total Items found: {len(items)}")
        items_with_siren = sum(1 for item in items if item.findall("sirenSettings"))
        print(f"Items with sirenSettings: {items_with_siren}")

        # List all unique vehicle names
        print("\nAll unique vehicle names:")
        names = sorted(set(item.attrib.get('name', 'NO_NAME') for item in items))
        for name in names:
            print(f"- {name}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    analyze_vehicle_structure("~/attachments/carvariations.meta")
