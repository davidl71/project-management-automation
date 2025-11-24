# Exarp Cleanup Plan

**Date**: 2025-01-27
**Status**: Action Plan
**Purpose**: Remove Exarp leftovers from ib_box_spread_full_universal repository

---

## Overview

The `project-management-automation` MCP server has been split into a separate repository called **Exarp** (`exarp-project-management`). This document outlines the cleanup plan to remove leftovers from the main repository.

---

## Current Status

### Directory Structure

**Found**: `mcp-servers/project-management-automation/` directory exists
- **Status**: Separate Git repository (has `.git` directory)
- **Size**: TBD
- **Tracked in main repo**: Checking...

**Decision**: Remove completely (Exarp is now a separate repository, installed via PyPI)

---

### Configuration References

#### MCP Configuration (`.cursor/mcp.json`)

**Status**: Should reference Exarp package installation

**Current**: Needs verification - should use:
```json
{
  "exarp": {
    "command": "python3",
    "args": ["-m", "exarp_project_management.server"],
    "description": "Exarp - Project management automation tools"
  }
}
```

**Action**: Verify and update if needed

---

#### Cursor Rules

**Found References**:
1. `.cursor/rules/project-automation.mdc` - References old path
2. `.cursor/rules/automation-tool-suggestions.mdc` - References old path

**Action**: Update references to Exarp and PyPI installation

---

#### Global Docs

**Found Reference**:
- `.cursor/global-docs.json` - References `mcp-servers/project-management-automation/USAGE.md`

**Action**: Remove or update to point to Exarp repository documentation

---

## Cleanup Actions

### Step 1: Remove Directory

**If directory is not tracked in main repo** (separate Git repo):

```bash
# Remove the entire directory
rm -rf mcp-servers/project-management-automation/
```

**If directory is tracked in main repo**:

```bash
# Remove from Git tracking
git rm -r mcp-servers/project-management-automation/
```

---

### Step 2: Update Configuration Files

#### Update `.cursor/rules/project-automation.mdc`

**Remove/Update**:
- Old path references: `mcp-servers/project-management-automation/`
- Old installation instructions
- Old server location references

**Add**:
- PyPI installation: `pip install exarp-automation-mcp`
- Git installation: `pip install git+ssh://git@github.com/davidl71/exarp-project-management.git`
- Package name: `exarp_project_management`

---

#### Update `.cursor/rules/automation-tool-suggestions.mdc`

**Remove/Update**:
- Reference to `mcp-servers/project-management-automation/USAGE.md`

**Update to**:
- Reference to Exarp repository: `https://github.com/davidl71/exarp-project-management`

---

#### Update `.cursor/global-docs.json`

**Remove**:
- `mcp-servers/project-management-automation/USAGE.md` entry

**Or Update to**:
- Exarp repository documentation URL

---

### Step 3: Update Documentation

**Files to Update**:
- `docs/MCP_SERVERS.md` (if exists)
- `README.md` (if references Exarp)
- Any setup guides

**Action**: Update references from local directory to PyPI package

---

### Step 4: Update .gitignore

**Check if needed**:
- If directory is removed, no `.gitignore` update needed
- If keeping as reference, add to `.gitignore`

**Recommendation**: No update needed (directory will be removed)

---

## Verification

### After Cleanup

```bash
# Verify directory is removed
[ ! -d "mcp-servers/project-management-automation/" ] && echo "✅ Directory removed" || echo "❌ Directory still exists"

# Verify no references remain
grep -r "project-management-automation" .cursor/ docs/ --exclude-dir=.git 2>/dev/null | grep -v "EXARP" | wc -l

# Verify MCP config is correct
grep -A 5 '"exarp"' .cursor/mcp.json
```

---

## Recommended Approach

### Option: Complete Removal (Recommended)

**Rationale**:
- Exarp is now a separate repository
- Installed via PyPI or Git
- No need for local directory
- Cleaner repository structure

**Steps**:
1. Remove `mcp-servers/project-management-automation/` directory
2. Update configuration references
3. Update documentation references
4. Commit changes

---

## Execution Plan

### Phase 1: Preparation

1. ✅ Verify Exarp is working via PyPI/Git installation
2. ✅ Backup any local changes (if any)
3. ✅ Document current state

### Phase 2: Remove Directory

1. Remove `mcp-servers/project-management-automation/` directory
2. Verify removal

### Phase 3: Update References

1. Update `.cursor/rules/project-automation.mdc`
2. Update `.cursor/rules/automation-tool-suggestions.mdc`
3. Update `.cursor/global-docs.json`
4. Update documentation files

### Phase 4: Verification

1. Verify Exarp still works
2. Verify no broken references
3. Commit changes

---

## Files to Update

### Configuration Files

1. `.cursor/rules/project-automation.mdc`
   - Remove: `mcp-servers/project-management-automation/` references
   - Update: Installation instructions to PyPI
   - Update: Server location references

2. `.cursor/rules/automation-tool-suggestions.mdc`
   - Remove: `mcp-servers/project-management-automation/USAGE.md` reference
   - Update: Reference to Exarp repository

3. `.cursor/global-docs.json`
   - Remove: `mcp-servers/project-management-automation/USAGE.md` entry

### Documentation Files

1. `docs/MCP_SERVERS.md` (if exists)
   - Update: Exarp installation instructions
   - Remove: Local directory references

2. `README.md` (if references Exarp)
   - Update: Installation instructions

---

## Summary

### What to Remove

- ✅ `mcp-servers/project-management-automation/` directory (complete removal)
- ✅ References to local directory in configuration files
- ✅ References to local directory in documentation

### What to Keep/Update

- ✅ MCP configuration (`.cursor/mcp.json`) - Keep, verify it's correct
- ✅ Cursor rules - Update references to Exarp
- ✅ Documentation - Update to reference Exarp repository

### What NOT to Do

- ❌ Don't create Git submodule (Exarp is installed via PyPI)
- ❌ Don't keep directory as reference (unnecessary)
- ❌ Don't update .gitignore (directory will be removed)

---

## Related Documentation

- [Exarp Migration Leftovers Analysis](EXARP_MIGRATION_LEFTOVERS_ANALYSIS.md) - Detailed analysis
- [Exarp Repository](https://github.com/davidl71/exarp-project-management) - Exarp repository

---

**Status**: Action Plan Complete
**Recommendation**: Complete removal (cleanest approach)
**Next Steps**: Execute cleanup plan
