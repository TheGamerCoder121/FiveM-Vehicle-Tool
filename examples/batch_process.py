"""
Example script demonstrating how to resolve conflicts for all vehicles.
"""
from meta_tool.conflict_resolver import ConflictResolver
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def main():
    # Paths to your meta files
    carcols_path = Path("path/to/your/carcols.meta")
    carvariations_path = Path("path/to/your/carvariations.meta")

    # Create resolver instance
    resolver = ConflictResolver(carcols_path, carvariations_path)

    # Process all vehicles
    print("\nProcessing all vehicles...")

    # Resolve carcols conflicts
    carcols_changes = resolver.resolve_carcols_conflicts()
    print("\nCarcols changes:")
    print(f"Changed {len(carcols_changes['carcols'])} IDs in carcols.meta")
    print(f"Changed {len(carcols_changes['variations'])} IDs in carvariations.meta")

    # Resolve modkit conflicts
    modkit_changes = resolver.resolve_modkit_conflicts()
    print("\nModkit changes:")
    print(f"Changed {len(modkit_changes['carcols'])} modkit IDs in carcols.meta")
    print(f"Changed {len(modkit_changes['variations'])} modkit IDs in carvariations.meta")

if __name__ == "__main__":
    main()
