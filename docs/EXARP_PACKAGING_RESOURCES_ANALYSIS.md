# Exarp Packaging Resources Analysis

**Date**: 2025-11-26
**Question**: Which resources are unique to Exarp and should be packaged?

---

## Resources Overview

### ✅ **Should Be Packaged** (Exarp-Specific, Self-Contained)

1. **`resources/status.py`**
   - **Purpose**: Server status and health information
   - **Dependencies**: Checks for `tools/` directory existence (but doesn't import)
   - **Unique to Exarp**: ✅ Yes - Exarp server status
   - **Packaging**: ✅ Should be packaged - self-contained logic

2. **`resources/list.py`**
   - **Purpose**: List of available automation tools
   - **Dependencies**: None (hardcoded tool list)
   - **Unique to Exarp**: ✅ Yes - Exarp tool catalog
   - **Packaging**: ✅ Should be packaged - completely self-contained

3. **`prompts.py`**
   - **Purpose**: MCP prompt templates for Exarp workflows
   - **Dependencies**: None
   - **Unique to Exarp**: ✅ Yes - Exarp-specific prompts
   - **Packaging**: ✅ Should be packaged - self-contained templates

4. **`error_handler.py`**
   - **Purpose**: Centralized error handling and logging
   - **Dependencies**: Standard library only
   - **Unique to Exarp**: ✅ Yes - Exarp error handling
   - **Packaging**: ✅ Should be packaged - self-contained utilities

---

### ⚠️ **Should Be Packaged But Need Project Root Access** (Exarp-Specific, Project-Dependent)

5. **`resources/history.py`**
   - **Purpose**: Automation execution history
   - **Dependencies**: Reads from project's `scripts/.{name}_history.json` files
   - **Unique to Exarp**: ✅ Yes - Exarp history format
   - **Packaging**: ✅ Should be packaged - but needs project root detection
   - **Note**: Uses `_find_project_root()` to locate project-specific history files

6. **`resources/tasks.py`**
   - **Purpose**: Todo2 tasks resource access
   - **Dependencies**: Reads from project's `.todo2/state.todo2.json`
   - **Unique to Exarp**: ✅ Yes - Exarp Todo2 integration
   - **Packaging**: ✅ Should be packaged - but needs project root detection
   - **Note**: Uses `_find_project_root()` to locate Todo2 state file

7. **`resources/cache.py`**
   - **Purpose**: Cache status information
   - **Dependencies**: Reads from project's `.todo2/` and `scripts/` directories
   - **Unique to Exarp**: ✅ Yes - Exarp cache format
   - **Packaging**: ✅ Should be packaged - but needs project root detection
   - **Note**: Uses `_find_project_root()` to locate project-specific caches

---

## Tools Directory

**`tools/`** - Tool implementations
- **Status**: Already extracted to `project_management_automation/scripts/`
- **Packaging**: ✅ Already packaged
- **Note**: These reference project-specific files but are Exarp-specific implementations

---

## Summary

### ✅ **All Resources Should Be Packaged**

**Reasoning**:
1. All resources are **Exarp-specific** - they're part of Exarp's MCP server functionality
2. They provide **Exarp's unique features** - status, history, tasks, cache, prompts
3. Project-dependent resources use **project root detection** - they work with any project
4. They're **not shared** with the main project - they're Exarp's internal modules

### 📦 **Packaging Strategy**

1. **Move to Package**:
   - `resources/` → `project_management_automation/resources/`
   - `prompts.py` → `project_management_automation/prompts.py`
   - `error_handler.py` → `project_management_automation/error_handler.py`

2. **Update Imports**:
   - Change `from resources.` → `from project_management_automation.resources.`
   - Change `from prompts import` → `from project_management_automation.prompts import`
   - Change `from error_handler import` → `from project_management_automation.error_handler import`

3. **Update `pyproject.toml`**:
   - Ensure `resources/` is included in package
   - Ensure `prompts.py` is included
   - Ensure `error_handler.py` is included

---

## Benefits of Packaging

1. ✅ **Eliminates Import Warnings** - All modules available in package
2. ✅ **Cleaner Installation** - Everything in one place
3. ✅ **Better Portability** - Works regardless of source directory location
4. ✅ **Proper Package Structure** - Follows Python packaging best practices

---

## Current Issues

- ❌ Resources are in source directory, not in package
- ❌ Import warnings when package is installed
- ❌ Requires `WORKSPACE_PATH` or source directory detection

---

## Recommendation

**✅ Package all resources** - They're all unique to Exarp and should be part of the package.

**Next Steps**:
1. Move `resources/`, `prompts.py`, `error_handler.py` into `project_management_automation/`
2. Update all imports in `server.py` and other files
3. Update `pyproject.toml` to ensure they're included
4. Test installation - warnings should disappear

---

**Status**: Ready for implementation
