# Portability Analysis and Improvements

## Overview

This document identifies hardcoded paths in the codebase and provides solutions to make the code more portable across different machines and environments.

## Issues Found

### 🔴 Critical: Hardcoded Paths in Git-Tracked Files

1. **`.cursor/mcp.json`** (Lines 41, 59, 65)
   - Hardcoded: `/home/david/project-management-automation`
   - Impact: MCP server won't work on other machines
   - Status: ⚠️ **MUST FIX**

2. **`scripts/assign_mode002_agents.sh`** (Line 7)
   - Hardcoded: `PROJECT_ROOT="/home/david/project-management-automation"`
   - Impact: Script fails on other machines
   - Status: ⚠️ **MUST FIX**

### 🟡 Medium: Standard System Paths

3. **`server.py`** and **`path_validation.py`**
   - Hardcoded: `Path("/tmp")`, `Path("/var/tmp")`
   - Impact: Works on Unix/Linux, but not Windows
   - Status: ⚠️ **SHOULD FIX** for cross-platform support

### 🟢 Low Priority: Documentation Examples

4. **Documentation files** contain example paths
   - Impact: Examples only, not executed code
   - Status: ✅ **OK** (examples are fine)

## Solutions

### Solution 1: Fix `.cursor/mcp.json`

**Problem**: Cursor's MCP config requires absolute paths, but we can't hardcode them.

**Approach**: Use a setup script or environment variable substitution.

**Options**:
- **Option A**: Use a template file (`.cursor/mcp.json.template`) and a setup script
- **Option B**: Use environment variable substitution in a wrapper script
- **Option C**: Document manual configuration (current approach in `PORTABILITY.md`)

**Recommendation**: **Option A** - Template + setup script for best portability.

### Solution 2: Fix `scripts/assign_mode002_agents.sh`

**Problem**: Hardcoded `PROJECT_ROOT`.

**Solution**: Use script-relative path detection (like other scripts).

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
```

### Solution 3: Improve Cross-Platform Temp Directory Handling

**Problem**: Hardcoded `/tmp` and `/var/tmp` don't work on Windows.

**Solution**: Use Python's `tempfile` module for cross-platform support.

```python
import tempfile
temp_dir = Path(tempfile.gettempdir())
```

## Implementation Plan

### Phase 1: Critical Fixes (Immediate)

1. ✅ Fix `scripts/assign_mode002_agents.sh` - Use dynamic path detection
2. ✅ Create `.cursor/mcp.json.template` - Template with placeholders
3. ✅ Create `scripts/setup_mcp_config.sh` - Auto-generate config from template
4. ✅ Update `.gitignore` - Ignore generated `.cursor/mcp.json` (or document it's machine-specific)

### Phase 2: Cross-Platform Improvements (Optional)

5. ⏳ Update `server.py` - Use `tempfile.gettempdir()` instead of `/tmp`
6. ⏳ Update `path_validation.py` - Use `tempfile.gettempdir()` instead of `/tmp`
7. ⏳ Add Windows path handling tests

### Phase 3: Documentation (Optional)

8. ⏳ Update `PORTABILITY.md` - Document new setup process
9. ⏳ Add portability section to `README.md`

## Files to Modify

### Must Fix (Critical)
- [ ] `scripts/assign_mode002_agents.sh` - Line 7
- [ ] `.cursor/mcp.json` - Lines 41, 59, 65 (create template)

### Should Fix (Cross-Platform)
- [ ] `project_management_automation/server.py` - Line 93
- [ ] `project_management_automation/middleware/path_validation.py` - Line 31

## Testing Checklist

After fixes:
- [ ] Scripts work when run from different directories
- [ ] Scripts work on different machines (test on clean clone)
- [ ] MCP config can be generated automatically
- [ ] Cross-platform temp directory handling works (if implemented)

## Notes

- **`.cursor/mcp.json`** is inherently machine-specific (Cursor requires absolute paths)
- Best practice: Keep template in git, generate actual config per-machine
- Alternative: Document manual configuration (current approach)
- Consider: Using environment variables for project root detection
