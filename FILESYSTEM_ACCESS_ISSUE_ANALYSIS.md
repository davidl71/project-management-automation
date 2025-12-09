# File System Access Issue Analysis

**Date**: 2025-12-09  
**Issue**: Exarp scorecard tool failing with "Interrupted system call" errors

---

## Problem Summary

The Exarp `project_scorecard` tool was attempting to access paths **outside the project directory**, specifically:

1. `/Users/davidl/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/Message/Media/...`
2. `/Users/davidl/Library/Containers/com.apple.speech.MacinTalkFramework.MacinTalkAUSP/Data/Library/Logs`

These are **macOS system directories** in the user's Library folder, not part of the project.

---

## Root Cause

### Issue: Incorrect Project Root Detection

The `find_project_root()` function was returning `/Users/davidl` (the home directory) instead of `/Users/davidl/Projects/project-management-automation` (the actual project directory).

**Evidence from health check**:
```json
{
  "project_root": "/Users/davidl"  // ❌ Wrong!
}
```

### Why This Happened

When `find_project_root()` is called from the MCP server context:
1. It searches up from current working directory (`/Users/davidl`)
2. If there's a `.git` or `.todo2` in the home directory, it returns that
3. Or it falls back to `/Users/davidl` as the current working directory

### Impact

When `project_scorecard.py` calls:
```python
project_root = find_project_root()  # Returns /Users/davidl
py_files = list(project_root.rglob('*.py'))  # Scans entire home directory!
```

This recursively searches **the entire home directory**, including:
- `Library/` (system directories)
- `Documents/`
- `Downloads/`
- `Desktop/`
- All user files

When it hits protected system directories (like WhatsApp containers), macOS returns "Interrupted system call" errors.

---

## Solution Applied

### 1. Added Safety Check in `project_scorecard.py`

```python
project_root = find_project_root()

# Safety check: Ensure we're not scanning the entire home directory
if str(project_root) == str(Path.home()) or str(project_root) == '/Users/davidl':
    # Try to find the actual project by looking for project_management_automation package
    potential_root = Path(__file__).parent.parent.parent
    if (potential_root / 'project_management_automation').exists():
        project_root = potential_root
    else:
        # Last resort: use current working directory if it looks like a project
        cwd = Path.cwd()
        if (cwd / 'project_management_automation').exists() or (cwd / '.git').exists():
            project_root = cwd
```

### 2. Added Path Filtering

Added exclusions for system directories in all `rglob()` calls:

```python
py_files = [f for f in py_files 
            if 'venv' not in str(f) 
            and '.build-env' not in str(f)
            and '__pycache__' not in str(f)
            and 'Library' not in str(f)  # Exclude macOS Library directories
            and 'Containers' not in str(f)  # Exclude app containers
            and 'Group Containers' not in str(f)  # Exclude group containers
            and '.Trash' not in str(f)  # Exclude trash
            and str(f).startswith(str(project_root))]  # Ensure file is within project
```

Applied to:
- Python files (`*.py`)
- C++ files (`*.cpp`)
- Rust files (`*.rs`)
- TypeScript files (`*.ts`, `*.tsx`)
- Swift files (`*.swift`)
- Markdown files (`*.md`)

---

## Paths That Were Being Accessed

### Outside Project Directory

1. **WhatsApp Containers**:
   - `/Users/davidl/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/Message/Media/...`
   - These are protected system directories

2. **macOS System Directories**:
   - `/Users/davidl/Library/Containers/com.apple.speech.MacinTalkFramework...`
   - System application containers

3. **User Home Directory**:
   - `/Users/davidl/` (entire home directory was being scanned)

### Why These Failed

- **Protected Directories**: macOS protects certain Library directories
- **Permission Issues**: Some containers require special permissions
- **System Calls**: Accessing these triggers "Interrupted system call" (EINTR)

---

## Prevention Measures

### 1. Project Root Validation

Added check to ensure project root is not the home directory:
```python
if str(project_root) == str(Path.home()):
    # Fix project root detection
```

### 2. Path Filtering

All file searches now exclude:
- `Library/` directories
- `Containers/` directories
- `Group Containers/` directories
- `.Trash/` directories
- Files outside project root (via `str(f).startswith(str(project_root))`)

### 3. Better Project Root Detection

The safety check tries multiple fallbacks:
1. Check if project root is home directory
2. Try package location (`__file__` based)
3. Try current working directory
4. Verify with existence checks

---

## Testing

To verify the fix:

```python
from project_management_automation.utils.project_root import find_project_root
from pathlib import Path

root = find_project_root()
print(f"Project root: {root}")
print(f"Is home dir: {root == Path.home()}")
print(f"Has project_management_automation: {(root / 'project_management_automation').exists()}")
```

**Expected**: Project root should be `/Users/davidl/Projects/project-management-automation`

---

## Related Files

- `project_management_automation/utils/project_root.py` - Project root detection
- `project_management_automation/tools/project_scorecard.py` - Scorecard tool (fixed)
- Any tool using `find_project_root()` + `rglob()` - May need similar fixes

---

## Recommendations

1. ✅ **Fixed**: Added safety checks in `project_scorecard.py`
2. ⚠️ **Review**: Check other tools using `rglob()` for similar issues
3. ⚠️ **Improve**: Enhance `find_project_root()` to be more reliable in MCP context
4. ✅ **Document**: This issue and fix documented

---

**Status**: ✅ **Fixed**  
**Last Updated**: 2025-12-09

