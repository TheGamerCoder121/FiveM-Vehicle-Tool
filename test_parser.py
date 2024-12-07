#!/usr/bin/env python3

from lxml import etree
import sys
from pathlib import Path

def analyze_meta_file(file_path, max_elements=5):
    file_path = Path(file_path).expanduser()
    print(f"\nAnalyzing {file_path}:")
    parser = etree.XMLParser(remove_blank_text=True)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = etree.parse(f, parser)
            root = tree.getroot()

        print("\nFound kitName elements:")
        for elem in root.findall(".//kitName")[:max_elements]:
            print(etree.tostring(elem, encoding='unicode').strip())
            parent = elem.getparent()
            if parent is not None:
                for child in parent:
                    if child.tag == 'id':
                        print("Associated ID:", etree.tostring(child, encoding='unicode').strip())
            print("---")

        print("\nFound sirenSettings elements:")
        for elem in root.findall(".//sirenSettings")[:max_elements]:
            print(etree.tostring(elem, encoding='unicode').strip())
            print("---")

        print("\nFound kits elements:")
        for elem in root.findall(".//kits")[:max_elements]:
            print(etree.tostring(elem, encoding='unicode').strip())
            print("---")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    analyze_meta_file("~/attachments/carcols.meta")
    analyze_meta_file("~/attachments/carvariations.meta")
