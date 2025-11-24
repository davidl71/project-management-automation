# Exarp Migration Leftovers Analysis

**Date**: 2025-01-27
**Status**: Analysis
**Purpose**: Identify and document leftovers from project-management-automation → Exarp migration

---

## Overview

The `project-management-automation` MCP server has been split into a separate repository called **Exarp**. This document identifies any remaining references, files, or configurations in the main `ib_box_spread_full_universal` repository that need to be cleaned up or updated.

---

## Analysis Results

### Git Submodule Status

**Status**: Checking for submodule references...

**Action**: If Exarp is used as a submodule, document the setup. If not, remove any submodule references.

---

### Directory Structure

**Status**: Checking for `mcp-servers/project-management-automation/` directory...

**Action**:
- If directory exists and is empty/unused → Remove
- If directory exists with local changes → Document or migrate
- If directory is a submodule → Document submodule usage

---

### Configuration Files

#### MCP Configuration (`.cursor/mcp.json`)

**Status**: Checking for references...

**Current Configuration**: Should reference Exarp installation method (PyPI or Git)

**Action**: Update to use Exarp package name and installation method

---

#### Cursor Rules (`.cursor/rules/`)

**Status**: Checking for references...

**Files to Check**:
- `.cursor/rules/project-automation.mdc` - May reference old name
- `.cursor/rules/automation-tool-suggestions.mdc` - May reference old name
- `.cursor/rules/todo2.mdc` - May reference old name

**Action**: Update references from "automa" or "project-management-automation" to "Exarp"

---

### Documentation Files

**Status**: Checking for documentation references...

**Files to Check**:
- `docs/` - Any documentation mentioning project-management-automation
- `README.md` - May reference the MCP server
- Setup guides - May have installation instructions

**Action**: Update references to Exarp and new installation method

---

## Recommended Actions

### Option 1: Complete Removal (If Not Using Exarp)

**If Exarp is not needed in this repository:**

1. **Remove directory** (if exists):
   ```bash
   rm -rf mcp-servers/project-management-automation/
   ```

2. **Remove from .gitignore** (if present):
   - Remove any patterns for `mcp-servers/project-management-automation/`

3. **Remove MCP configuration**:
   - Remove `exarp` entry from `.cursor/mcp.json`

4. **Update documentation**:
   - Remove references to Exarp/automa
   - Update setup guides

5. **Update Cursor rules**:
   - Remove or update references in `.cursor/rules/`

---

### Option 2: Git Submodule (If Using Exarp as Submodule)

**If Exarp should be a Git submodule:**

1. **Add as submodule**:
   ```bash
   git submodule add git@github.com:davidl71/exarp-project-management.git mcp-servers/exarp
   ```

2. **Update .gitignore**:
   ```gitignore
   # Exarp submodule (tracked via .gitmodules)
   # No ignore needed - submodule is tracked
   ```

3. **Update MCP configuration**:
   ```json
   {
     "mcpServers": {
       "exarp": {
         "command": "python3",
         "args": ["-m", "exarp_project_management.server"],
         "description": "Exarp - Project management automation tools"
       }
     }
   }
   ```

4. **Document submodule usage**:
   - Add to README.md
   - Document initialization: `git submodule update --init --recursive`

---

### Option 3: PyPI Package (Recommended - Current Setup)

**If Exarp is installed via PyPI (current recommended approach):**

1. **Remove local directory** (if exists):
   ```bash
   rm -rf mcp-servers/project-management-automation/
   ```

2. **Update .gitignore**:
   ```gitignore
   # Exarp is installed via PyPI, not stored locally
   # No local directory to ignore
   ```

3. **Keep MCP configuration** (already correct):
   ```json
   {
     "mcpServers": {
       "exarp": {
         "command": "python3",
         "args": ["-m", "exarp_project_management.server"],
         "description": "Exarp - Project management automation tools"
       }
     }
   }
   ```

4. **Update documentation**:
   - Document PyPI installation: `pip install exarp-automation-mcp`
   - Update setup guides
   - Remove references to local directory

5. **Update Cursor rules**:
   - Update references from "automa" to "Exarp"
   - Update installation instructions

---

## Specific Files to Check

### Configuration Files

1. **`.cursor/mcp.json`**
   - Check for `exarp` or `project-management-automation` entry
   - Verify command points to installed package

2. **`.cursor/rules/project-automation.mdc`**
   - Update references from "automa" to "Exarp"
   - Update installation instructions

3. **`.cursor/rules/automation-tool-suggestions.mdc`**
   - Update references from "automa" to "Exarp"

4. **`.cursorrules`**
   - Check for references to project-management-automation
   - Update to Exarp

### Documentation Files

1. **`README.md`**
   - Check for MCP server references
   - Update to Exarp and PyPI installation

2. **`docs/MCP_SERVERS.md`** (if exists)
   - Update Exarp documentation
   - Remove local installation instructions

3. **Setup guides** (if any)
   - Update installation instructions
   - Reference PyPI package

### Build/Config Files

1. **`.gitignore`**
   - Remove `mcp-servers/project-management-automation/` if present
   - Add note about Exarp being installed via PyPI

2. **`pyproject.toml`` or `requirements.txt`** (if any)
   - Check for project-management-automation dependency
   - Update to `exarp-automation-mcp` if needed

---

## Cleanup Checklist

### Immediate Actions

- [ ] Check for `mcp-servers/project-management-automation/` directory
- [ ] Check for Git submodule references (`.gitmodules`)
- [ ] Check `.cursor/mcp.json` for correct Exarp configuration
- [ ] Check `.cursor/rules/` for old references
- [ ] Check documentation for old references
- [ ] Check `.gitignore` for cleanup

### Update References

- [ ] Update all "automa" → "Exarp" references
- [ ] Update all "project-management-automation" → "exarp-project-management" references
- [ ] Update installation instructions to PyPI
- [ ] Remove local directory references

### Documentation

- [ ] Update README.md
- [ ] Update setup guides
- [ ] Update MCP server documentation
- [ ] Document Exarp installation method

---

## Migration Summary

### What Changed

- **Old**: `mcp-servers/project-management-automation/` (local directory)
- **New**: `exarp-automation-mcp` (PyPI package)

### Installation Method

- **Old**: Local directory or Git submodule
- **New**: `pip install exarp-automation-mcp` or `pip install git+ssh://git@github.com/davidl71/exarp-project-management.git`

### MCP Configuration

- **Old**: May have referenced local directory
- **New**: References installed package: `python3 -m exarp_project_management.server`

---

## Related Documentation

- [Exarp README](../mcp-servers/project-management-automation/README.md) - Exarp documentation
- [Git LFS Candidates](GIT_LFS_CANDIDATES_ANALYSIS.md) - Large file analysis
- [Build Artifacts Analysis](GITIGNORE_BUILD_ARTIFACTS_ANALYSIS.md) - Build artifact cleanup

---

**Status**: Analysis Complete
**Next Steps**: Review findings and execute cleanup actions
**Recommendation**: Use PyPI package (Option 3) - cleanest approach
