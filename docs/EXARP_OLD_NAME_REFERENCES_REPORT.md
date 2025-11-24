# Exarp Old Name References Report

**Date**: 2025-01-27
**Status**: Analysis Complete

---

## Summary

### "project_management_automation" / "project-management-automation"

**Status**: ✅ **Keep as-is** (Package/Directory Name)

**Reasoning**:
- This is the **Python package name** (`project_management_automation`) - descriptive and correct
- This is the **directory name** (`project-management-automation`) - descriptive and correct
- The **MCP server ID is already "exarp"** (which is what matters for users)
- Changing these would require massive refactoring with no benefit

**Exceptions** (User-facing references that should mention "Exarp"):
- Documentation that describes the server to users
- Status/resource responses that show server name
- Comments that describe what the server is

---

### "automa" / "Automa" / "AUTOMA"

**Status**: ❌ **Replace with "Exarp"** (Old Project Name)

**Found in**:
1. **Code Files** (Critical):
   - `server.py` line 270: `FastMCP("automa")` → should be `"exarp"`
   - `server.py` line 273: `Server("automa")` → should be `"exarp"`
   - `resources/status.py` line 40, 69: `"server": "project-management-automation"` → should be `"exarp"`

2. **Documentation Files** (Update):
   - `README.md`: Multiple references to "automa" in workflow descriptions
   - `RESOURCES.md`: References to "automa MCP server"
   - `NAME_CHANGE.md`: Historical document (can update or archive)
   - `INTENTIONAL_DUPLICATES.md`: References to "automa MCP server"
   - `DUPLICATE_ANALYSIS.md`: References to "automa MCP server"
   - `USAGE.md`: References to "automa" in descriptions

3. **Cursor Rules** (Already Updated):
   - `.cursor/rules/project-automation.mdc`: ✅ Already updated
   - `.cursor/rules/automation-tool-suggestions.mdc`: ✅ Already updated

---

## Critical Fixes Needed

### 1. Code Files

**Priority: HIGH** - These affect runtime behavior:

1. **`server.py`**:
   - Line 270: `mcp = FastMCP("automa")` → `mcp = FastMCP("exarp")`
   - Line 273: `stdio_server_instance = Server("automa")` → `stdio_server_instance = Server("exarp")`

2. **`resources/status.py`**:
   - Line 40: `"server": "project-management-automation"` → `"server": "exarp"`
   - Line 69: `"server": "project-management-automation"` → `"server": "exarp"`

### 2. Documentation Files

**Priority: MEDIUM** - User-facing documentation:

1. **`README.md`**:
   - Line 23: "Use BEFORE automa tools" → "Use BEFORE Exarp tools"
   - Line 29: "converts automa analysis" → "converts Exarp analysis"
   - Line 34: "Use **automa** tools" → "Use **Exarp** tools"

2. **`RESOURCES.md`**:
   - Replace "automa MCP server" with "Exarp MCP server"
   - Replace "automa" with "Exarp" in examples

3. **Other Documentation**:
   - `INTENTIONAL_DUPLICATES.md`
   - `DUPLICATE_ANALYSIS.md`
   - `USAGE.md`

---

## Files to Update

### Critical (Code - Affects Runtime)
- [ ] `project_management_automation/server.py` (2 occurrences)
- [ ] `project_management_automation/resources/status.py` (2 occurrences)

### Important (Documentation - User-Facing)
- [ ] `README.md` (3+ occurrences)
- [ ] `RESOURCES.md` (5+ occurrences)
- [ ] `INTENTIONAL_DUPLICATES.md` (2+ occurrences)
- [ ] `DUPLICATE_ANALYSIS.md` (1+ occurrences)
- [ ] `USAGE.md` (1+ occurrences)

### Optional (Historical/Internal)
- [ ] `NAME_CHANGE.md` (can update or archive)
- [ ] Other internal documentation

---

## Package/Directory Name Decision

**Recommendation**: ✅ **Keep `project_management_automation` as package name**

**Reasons**:
1. It's descriptive and clear
2. Changing would require massive refactoring
3. The MCP server ID is already "exarp" (what users see)
4. Python package names are often descriptive, not branded
5. Directory names are often descriptive, not branded

**Examples**:
- `django` package → `django` directory
- `flask` package → `flask` directory
- `requests` package → `requests` directory

**Conclusion**: Package/directory name stays as-is. Only user-facing references need updating.

---

**Status**: Ready for fixes
