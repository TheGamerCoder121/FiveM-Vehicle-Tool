# GTA V FiveM Meta File Conflict Resolution Tool - Architecture Design

## 1. High-Level Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Interface│     │  Core Processor  │     │   File Handler  │
│  (CLI/GUI)      │────▶│(ID Generator &   │────▶│(XML Parser &    │
│                 │     │ Conflict Resolver)│     │ Writer)         │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## 2. Component Design

### 2.1 File Handler Module
```python
class MetaFileHandler:
    def __init__(self)
    def load_meta_file(file_path) -> XMLDocument
    def save_meta_file(file_path, xml_doc)
    def backup_files(files) -> bool
    def validate_meta_file(file_path) -> bool
```

### 2.2 Core Processor Module
```python
class IDGenerator:
    def generate_carcols_id() -> int
    def generate_modkit_id() -> int
    def validate_id_availability(id, existing_ids) -> bool

class ConflictResolver:
    def __init__(self, carcols_path, carvariations_path)
    def resolve_carcols_conflicts(vehicle_name=None)
    def resolve_modkit_conflicts(vehicle_name=None)
    def get_existing_ids() -> Set[int]
```

### 2.3 User Interface Module
```python
class MetaToolCLI:
    def __init__()
    def prompt_for_files()
    def prompt_for_vehicle()
    def prompt_for_operation()
    def display_changes(changes)
    def confirm_changes() -> bool
```

## 3. Data Flow

### 3.1 Carcols Conflict Resolution Flow
1. User Input:
   - Select carcols.meta and carvariations.meta files
   - Choose single vehicle or all vehicles
   - Select Carcols ID resolution

2. Processing:
   ```
   Load Files → Backup → Parse XML → Generate New IDs → Update Files → Save
   ```

3. XML Processing Pattern:
   ```xml
   # carcols.meta
   <id value="OLD_ID"/> → <id value="NEW_ID"/>

   # carvariations.meta
   <sirenSettings value="OLD_ID"/> → <sirenSettings value="NEW_ID"/>
   ```

### 3.2 Modkit Conflict Resolution Flow
1. User Input:
   - Select meta files
   - Choose single vehicle or all vehicles
   - Select Modkit ID resolution

2. Processing:
   ```
   Load Files → Backup → Parse XML → Generate New IDs → Update Both Files → Save
   ```

3. XML Processing Pattern:
   ```xml
   # carcols.meta
   <kitName>OLD_ID_name_modkit</kitName>
   <id value="OLD_ID"/>
   ↓
   <kitName>NEW_ID_name_modkit</kitName>
   <id value="NEW_ID"/>

   # carvariations.meta
   <Item>OLD_ID_name_modkit</Item>
   ↓
   <Item>NEW_ID_name_modkit</Item>
   ```

## 4. Implementation Details

### 4.1 File Operations
- Always create backups before modifications
- Use lxml for XML parsing/writing to preserve formatting
- Validate XML structure before processing

### 4.2 ID Generation
- Carcols IDs: Random number generation with collision detection
- Modkit IDs: 2-6 digit numbers with validation
- Maintain registry of used IDs to prevent conflicts

### 4.3 Error Handling
- Validate input files
- Check file permissions
- Verify XML structure
- Handle parsing errors
- Provide clear error messages

### 4.4 User Interface Design
- Clear prompts for file selection
- Progress indicators for batch operations
- Preview of changes before applying
- Confirmation dialogs for important actions
- Clear success/error messages

## 5. Dependencies
- Python 3.8+
- lxml for XML processing
- click for CLI interface
- pathlib for file operations

## 6. Future Considerations
- GUI implementation
- Batch file processing
- Configuration files for default settings
- Logging system
- Auto-backup management
