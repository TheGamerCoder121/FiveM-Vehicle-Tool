import xml.etree.ElementTree as ET
from pathlib import Path

def print_element_context(elem, context_lines=2):
    print(f"\n{'='*50}")
    print(ET.tostring(elem, encoding='unicode').strip())
    print(f"{'='*50}")

def analyze_meta_file(filepath, pattern_type):
    print(f"\nAnalyzing {filepath.name}:")
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        if pattern_type == "carcols":
            print("\nSample id values:")
            count = 0
            for id_elem in root.findall(".//id"):
                if count >= 3:
                    break
                if 'value' in id_elem.attrib:
                    print(ET.tostring(id_elem, encoding='unicode').strip())
                    count += 1

            print("\nSample modkit patterns:")
            count = 0
            for elem in root.iter():
                if elem.tag == 'kitName':
                    print("\nModkit group:")
                    print(ET.tostring(elem, encoding='unicode').strip())
                    parent = elem.find("..")
                    if parent is not None:
                        for child in parent:
                            if child.tag == 'id':
                                print(ET.tostring(child, encoding='unicode').strip())
                    count += 1
                    if count >= 2:
                        break

        elif pattern_type == "carvariations":
            print("\nSample sirenSettings values:")
            count = 0
            for siren in root.findall(".//sirenSettings"):
                if count >= 3:
                    break
                if 'value' in siren.attrib:
                    print(ET.tostring(siren, encoding='unicode').strip())
                    count += 1

            print("\nSample kits patterns:")
            count = 0
            for kits in root.findall(".//kits"):
                if count >= 2:
                    break
                print("\nKit group:")
                print(ET.tostring(kits, encoding='unicode').strip())
                count += 1

    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")

def main():
    carcols_path = Path("~/attachments/carcols.meta").expanduser()
    carvariations_path = Path("~/attachments/carvariations.meta").expanduser()

    print("\n=== Analyzing Carcols.meta ===")
    analyze_meta_file(carcols_path, "carcols")

    print("\n=== Analyzing Carvariations.meta ===")
    analyze_meta_file(carvariations_path, "carvariations")

if __name__ == "__main__":
    main()
