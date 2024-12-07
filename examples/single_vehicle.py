"""
Example script demonstrating how to resolve conflicts for a single vehicle.
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

    # Process specific vehicle
    vehicle_name = "24valor18sedan"

    # Resolve carcols conflicts
    carcols_changes = resolver.resolve_carcols_conflicts(vehicle_name)
    print(f"\nCarcols changes for {vehicle_name}:")
    print(f"Changed {len(carcols_changes['carcols'])} IDs in carcols.meta")
    print(f"Changed {len(carcols_changes['variations'])} IDs in carvariations.meta")

    # Resolve modkit conflicts
    modkit_changes = resolver.resolve_modkit_conflicts(vehicle_name)
    print(f"\nModkit changes for {vehicle_name}:")
    print(f"Changed {len(modkit_changes['carcols'])} modkit IDs in carcols.meta")
    print(f"Changed {len(modkit_changes['variations'])} modkit IDs in carvariations.meta")

if __name__ == "__main__":
    main()
