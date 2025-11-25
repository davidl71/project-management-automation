# Auto-Fix Usage Guide

**Date**: 2025-11-25  
**Tool**: `detect_duplicate_tasks` with `auto_fix=True`

---

## Overview

The **auto-fix** feature automatically consolidates duplicate tasks found by the duplicate detection tool. When enabled, it:

1. **Selects the "best" task** from each duplicate group (based on status, comments, dependencies)
2. **Merges relevant data** from other duplicates into the best task
3. **Updates dependencies** in other tasks to point to the best task
4. **Removes duplicate tasks** from the Todo2 state

---

## ⚠️ Important Notes

- **Experimental Feature**: Auto-fix is marked as experimental
- **Review Recommended**: Always review duplicates before auto-fixing in production
- **Backup Recommended**: Consider backing up `.todo2/state.todo2.json` before auto-fixing
- **Dry Run First**: Test with `auto_fix=False` first to see what would be fixed

---

## Usage

### Via MCP Tool (Cursor)

```
/exarp/detect_duplicate_tasks?similarity_threshold=0.85&auto_fix=true
```

Or in chat:
```
"Detect and auto-fix duplicate tasks"
"Use detect_duplicate_tasks with auto_fix enabled"
```

### Via Python Script

```bash
# Run with auto-fix enabled
python3 project_management_automation/scripts/automate_todo2_duplicate_detection.py --auto-fix

# Custom threshold with auto-fix
python3 project_management_automation/scripts/automate_todo2_duplicate_detection.py --threshold 0.90 --auto-fix
```

### Via Configuration File

```json
{
  "output_path": "docs/TODO2_DUPLICATE_DETECTION_REPORT.md",
  "similarity_threshold": 0.85,
  "auto_fix": true
}
```

---

## Auto-Fix Logic

### 1. Selecting the "Best" Task

The best task is selected based on:
- **Status priority**: Done > In Progress > Review > Todo
- **Comments count**: More comments = more information
- **Dependencies**: Tasks with dependencies are prioritized
- **Age**: Older tasks are preferred (more context)

### 2. Merging Data

From duplicate tasks into the best task:
- **Comments**: All comments are merged
- **Tags**: All tags are merged (deduplicated)
- **Priority**: Highest priority is kept
- **Dependencies**: All dependencies are merged

### 3. Updating Dependencies

Other tasks that depend on duplicate tasks are updated to point to the best task.

### 4. Removing Duplicates

Duplicate tasks are removed from the Todo2 state file after consolidation.

---

## Example Workflow

### Step 1: Review Duplicates (No Auto-Fix)

```bash
# Detect duplicates without fixing
python3 scripts/automate_todo2_duplicate_detection.py
```

Review the report to see what would be fixed.

### Step 2: Auto-Fix Duplicates

```bash
# Now auto-fix the duplicates
python3 scripts/automate_todo2_duplicate_detection.py --auto-fix
```

### Step 3: Verify Results

Check the report to see:
- Tasks removed count
- Tasks merged count
- Dependencies updated count

---

## Safety Recommendations

1. **Always Review First**: Run with `auto_fix=False` first
2. **Backup State File**: Copy `.todo2/state.todo2.json` before auto-fixing
3. **Use Dry Run**: Test with dry-run mode if available
4. **Check Git Status**: Verify changes after auto-fix
5. **Review Report**: Always read the auto-fix report

---

## Troubleshooting

### Syntax Error

If you see:
```
unmatched ')' (automate_todo2_duplicate_detection.py, line 41)
```

**Solution**: Rebuild and reinstall the package:
```bash
cd project-management-automation
source .build-env/bin/activate
python3 -m build --wheel
pip install --force-reinstall --no-deps dist/*.whl
```

Then restart Cursor to reload the MCP server.

### Auto-Fix Not Working

1. Check that duplicates were actually found
2. Verify `auto_fix=True` is set correctly
3. Check file permissions on `.todo2/state.todo2.json`
4. Review error logs for specific issues

---

## Current Status

**Status**: ✅ Syntax Fixed, Package Rebuild Needed

The syntax error has been fixed in the source code, but Cursor may be using a cached version. Rebuild and reinstall the package to update the MCP server.

---

**Last Updated**: 2025-11-25

