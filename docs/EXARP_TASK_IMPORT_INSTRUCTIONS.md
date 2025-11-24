# Exarp Task Import Instructions

**Date**: 2025-01-27
**Status**: Ready for Manual Import
**Purpose**: Instructions for importing tasks into Exarp repository

---

## ✅ What's Been Done

### Main Repository (ib_box_spread_full_universal)

1. ✅ **Tasks Removed**: T-1 through T-5 removed from `.todo2/state.todo2.json`
2. ✅ **Import File Created**: `docs/EXARP_TASKS_IMPORT.json` with all task data
3. ✅ **Import Script Created**: `scripts/import_exarp_tasks.sh` for automated import

---

## 📋 Import File

**Location**: `docs/EXARP_TASKS_IMPORT.json`

**Contains**:
- 5 tasks (T-1 through T-5)
- Complete metadata (content, tags, priority, status, timestamps)
- Migration information

---

## 🚀 How to Import

### Option 1: Automated Import (Recommended)

1. **Navigate to Exarp repository**:
   ```bash
   cd /path/to/exarp-project-management
   ```

2. **Copy import file**:
   ```bash
   cp /path/to/ib_box_spread_full_universal/docs/EXARP_TASKS_IMPORT.json .
   ```

3. **Run import script from main repo**:
   ```bash
   cd /path/to/ib_box_spread_full_universal
   ./scripts/import_exarp_tasks.sh /path/to/exarp-project-management
   ```

   **Or** if Exarp repo is in parent directory:
   ```bash
   ./scripts/import_exarp_tasks.sh
   ```

---

### Option 2: Manual Import

1. **Copy import file to Exarp repository**:
   ```bash
   cp docs/EXARP_TASKS_IMPORT.json /path/to/exarp-project-management/
   ```

2. **Create/update Exarp's Todo2 state**:
   ```bash
   cd /path/to/exarp-project-management
   mkdir -p .todo2
   ```

3. **Run Python import script** (created by import script, or use this):

   ```python
   # scripts/import_tasks.py
   import json
   from datetime import datetime
   from pathlib import Path

   # Paths
   repo_root = Path(__file__).parent.parent
   import_file = repo_root / "EXARP_TASKS_IMPORT.json"
   todo2_file = repo_root / ".todo2" / "state.todo2.json"

   # Read import file
   with open(import_file, 'r') as f:
       import_data = json.load(f)

   # Read or create Todo2 state
   if todo2_file.exists():
       with open(todo2_file, 'r') as f:
           todo2_data = json.load(f)
   else:
       todo2_data = {"todos": []}

   # ID mapping
   id_mapping = {
       'T-1': 'EXARP-1',
       'T-2': 'EXARP-2',
       'T-3': 'EXARP-3',
       'T-4': 'EXARP-4',
       'T-5': 'EXARP-5'
   }

   # Import tasks
   for task in import_data['tasks']:
       old_id = task['id']
       new_id = id_mapping[old_id]

       # Update task
       task['id'] = new_id
       task['migrated_from'] = old_id
       task['migrated_at'] = datetime.now().isoformat()

       # Add to todos
       if 'todos' not in todo2_data:
           todo2_data['todos'] = []
       todo2_data['todos'].append(task)

   # Save
   with open(todo2_file, 'w') as f:
       json.dump(todo2_data, f, indent=2)

   print(f"✅ Imported {len(import_data['tasks'])} tasks")
   ```

---

## 📝 Tasks to Import

| Original ID | New ID | Description |
|-------------|--------|-------------|
| T-1 | EXARP-1 | Refactor sync_todo_tasks_tool to sync_tasks_tool (adapter pattern) |
| T-2 | EXARP-2 | Create TaskSourceAdapter and TaskTargetAdapter base classes |
| T-3 | EXARP-3 | Extend detect_duplicate_tasks_tool to support multiple sources |
| T-4 | EXARP-4 | Refactor analyze_todo2_alignment_tool to analyze_task_alignment_tool |
| T-5 | EXARP-5 | Extend simplify_rules_tool to support Cursor rules (.cursorrules) |

---

## ✅ Verification

After import, verify:

1. **Tasks exist in Exarp repository**:
   ```bash
   cd /path/to/exarp-project-management
   cat .todo2/state.todo2.json | grep -A 5 "EXARP-1"
   ```

2. **All 5 tasks imported**:
   ```bash
   cat .todo2/state.todo2.json | grep -c "EXARP-"
   # Should output: 5
   ```

3. **Task IDs are correct**:
   - EXARP-1 through EXARP-5
   - No duplicate IDs

---

## 📁 Files Created

1. **Import File**: `docs/EXARP_TASKS_IMPORT.json`
   - Contains all task data
   - Ready to copy to Exarp repository

2. **Import Script**: `scripts/import_exarp_tasks.sh`
   - Automated import script
   - Handles copying and importing

3. **Documentation**:
   - `docs/EXARP_TODO2_MIGRATION_COMPLETE.md` - Migration summary
   - `docs/EXARP_TODO2_MIGRATION_ANALYSIS.md` - Analysis
   - `docs/EXARP_TASK_IMPORT_INSTRUCTIONS.md` - This file

---

## 🎯 Quick Start

**If Exarp repository is already cloned locally**:

```bash
# From main repository
cd /Volumes/SSD1_APFS/ib_box_spread_full_universal
./scripts/import_exarp_tasks.sh /path/to/exarp-project-management
```

**If Exarp repository needs to be cloned**:

```bash
# Clone Exarp repository first
git clone git@github.com:davidl71/exarp-project-management.git
cd /Volumes/SSD1_APFS/ib_box_spread_full_universal
./scripts/import_exarp_tasks.sh ../exarp-project-management
```

---

**Status**: ✅ Ready for Import
**Next**: Copy import file to Exarp repository and run import script
