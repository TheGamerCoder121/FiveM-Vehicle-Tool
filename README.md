# Clone the repository
git clone https://github.com/TheGamerCoder121/fivem-vehicle-tool.git
cd fivem-vehicle-tool

# Install the package
```
pip install -e .
```

## Usage

### Basic Usage

```bash
# Process all vehicles in both meta files
meta-tool resolve --carcols path/to/carcols.meta --variations path/to/carvariations.meta

# Process a specific vehicle
meta-tool resolve --carcols path/to/carcols.meta --variations path/to/carvariations.meta --vehicle 24valor18sedan
```

### Command Options

- `--carcols`: Path to your carcols.meta file
- `--variations`: Path to your carvariations.meta file
- `--vehicle`: (Optional) Name of the specific vehicle to process
- `--backup`: (Optional) Create backup files before making changes (default: True)

## How It Works

### Carcols Conflict Resolution

The tool finds and updates ID pairs in both meta files:

```xml
<!-- In carcols.meta -->
<id value="12345"/>

<!-- In carvariations.meta -->
<sirenSettings value="12345"/>
```

### Modkit ID Resolution

The tool updates modkit IDs consistently across both files:

```xml
<!-- In carcols.meta -->
<kitName>990_vehiclename_modkit</kitName>
<id value="990" />

<!-- In carvariations.meta -->
<kits>
  <Item>990_vehiclename_modkit</Item>
</kits>
```

## Troubleshooting

### Common Issues

1. **Vehicle Not Found**
   - Check that the vehicle name matches the pattern in kitName (e.g., "24valor18sedan")
   - Vehicle names are case-sensitive
   - Look for the vehicle name in kitName elements (format: "{number}_{vehiclename}_modkit")

2. **ID Conflicts Still Present**
   - Ensure both meta files are properly formatted XML
   - Check that the files are not read-only
   - Verify that the IDs follow the 2-6 digit format

3. **Changes Not Saving**
   - Check file permissions
   - Ensure you have write access to the directory
   - Look for backup files in case of issues

### Debug Mode

Run the tool with debug logging for more detailed information:

```bash
meta-tool --debug resolve --carcols path/to/carcols.meta --variations path/to/carvariations.meta
```

## Examples

### Single Vehicle Processing

```python
from meta_tool.conflict_resolver import ConflictResolver

# Create resolver instance
resolver = ConflictResolver('carcols.meta', 'carvariations.meta')

# Process specific vehicle
changes = resolver.resolve_carcols_conflicts('24valor18sedan')
print(f"Changed {len(changes['carcols'])} IDs")
```

### Batch Processing

```python
from meta_tool.conflict_resolver import ConflictResolver

# Create resolver instance
resolver = ConflictResolver('carcols.meta', 'carvariations.meta')

# Process all vehicles
changes = resolver.resolve_modkit_conflicts()
print(f"Updated {len(changes['carcols'])} modkit IDs")
