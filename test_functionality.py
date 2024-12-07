import logging
from pathlib import Path
from meta_tool.conflict_resolver import ConflictResolver
from meta_tool.meta_file_handler import MetaFileHandler
from meta_tool.id_generator import IDGenerator
import shutil

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup_test_files():
    """Create copies of meta files for testing."""
    attachments_dir = Path.home() / "attachments"
    test_dir = Path.home() / "test_files"
    test_dir.mkdir(exist_ok=True)

    # Copy test files
    shutil.copy2(attachments_dir / "carcols.meta", test_dir / "carcols.meta")
    shutil.copy2(attachments_dir / "carvariations.meta", test_dir / "carvariations.meta")
    return test_dir

def test_single_vehicle():
    """Test carcols and modkit resolution for a single vehicle."""
    test_dir = setup_test_files()
    resolver = ConflictResolver(
        test_dir / "carcols.meta",
        test_dir / "carvariations.meta"
    )

    # Test with known vehicle name from analysis
    vehicle = "24valor18sedan"
    logger.info(f"\nTesting single vehicle mode with {vehicle}")

    # Test carcols resolution
    carcols_changes = resolver.resolve_carcols_conflicts(vehicle)
    logger.info(f"Carcols changes: {carcols_changes}")

    # Test modkit resolution
    modkit_changes = resolver.resolve_modkit_conflicts(vehicle)
    logger.info(f"Modkit changes: {modkit_changes}")

    return bool(carcols_changes['carcols'] or modkit_changes['modkit'])

def test_all_vehicles():
    """Test carcols and modkit resolution for all vehicles."""
    test_dir = setup_test_files()
    resolver = ConflictResolver(
        test_dir / "carcols.meta",
        test_dir / "carvariations.meta"
    )

    logger.info("\nTesting all vehicles mode")

    # Test carcols resolution
    carcols_changes = resolver.resolve_carcols_conflicts()
    logger.info(f"Carcols changes: {carcols_changes}")

    # Test modkit resolution
    modkit_changes = resolver.resolve_modkit_conflicts()
    logger.info(f"Modkit changes: {modkit_changes}")

    return bool(carcols_changes['carcols'] or modkit_changes['modkit'])

def main():
    """Run all tests and report results."""
    logger.info("Starting functionality tests...")

    single_vehicle_success = test_single_vehicle()
    all_vehicles_success = test_all_vehicles()

    logger.info("\nTest Results:")
    logger.info(f"Single vehicle mode: {'✓ PASS' if single_vehicle_success else '✗ FAIL'}")
    logger.info(f"All vehicles mode: {'✓ PASS' if all_vehicles_success else '✗ FAIL'}")

if __name__ == "__main__":
    main()
