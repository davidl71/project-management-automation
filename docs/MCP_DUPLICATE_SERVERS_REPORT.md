# MCP Duplicate Servers Report

**Date**: 2025-11-30  
**Status**: ⚠️ **5 Duplicate Servers Found**

---

## Problem

MCP servers are configured in **multiple workspace configurations**, causing them to appear as duplicates in Cursor. Cursor merges configurations from all open workspaces, so servers defined in multiple places appear multiple times.

---

## Duplicates Found

### ⚠️ 5 Duplicate Servers

| Server Name | Location 1 | Location 2 | Status |
|-------------|-----------|-----------|--------|
| **agentic-tools** | project-management-automation | ib_box_spread_full_universal | ⚠️ Duplicate |
| **context7** | project-management-automation | ib_box_spread_full_universal | ⚠️ Duplicate |
| **filesystem** | project-management-automation | ib_box_spread_full_universal | ⚠️ Duplicate |
| **sequential_thinking** | project-management-automation | ib_box_spread_full_universal | ⚠️ Duplicate |
| **tractatus_thinking** | project-management-automation | ib_box_spread_full_universal | ⚠️ Duplicate |

---

## Configuration Locations

### 1. Project: `project-management-automation/`
**File**: `.cursor/mcp.json`

**Servers (6):**
- `agentic-tools` (uvx)
- `context7` (uvx)
- `filesystem` (uvx)
- `interactive` (npx)
- `sequential_thinking` (uvx)
- `tractatus_thinking` (uvx)

### 2. Project: `ib_box_spread_full_universal/`
**File**: `.cursor/mcp.json`

**Servers:**
- `agentic-tools` (npx) ⚠️ **DUPLICATE**
- `context7` (npx) ⚠️ **DUPLICATE**
- `exarp` (run_server.sh)
- `filesystem` (npx) ⚠️ **DUPLICATE**
- `notebooklm` (npx)
- `sequential_thinking` (npx) ⚠️ **DUPLICATE**
- `tractatus_thinking` (npx) ⚠️ **DUPLICATE**

### 3. Global Configuration
**File**: `~/.cursor/mcp.json`

**Servers (1):**
- `GitKraken`

---

## Why This Happens

1. **Multiple Workspaces Open**: Cursor merges MCP configs from all open workspaces
2. **Same Servers in Multiple Projects**: Common servers (like `context7`, `tractatus_thinking`) are defined in both projects
3. **Workspace-Scoped Servers**: Some servers (like `filesystem`) are configured per-project with different paths

---

## Solutions

### Option 1: Move Common Servers to Global Config (Recommended)

Move universal servers (not project-specific) to global config:

**Servers to move to `~/.cursor/mcp.json`:**
- `agentic-tools` - Universal tool
- `context7` - Universal documentation lookup
- `sequential_thinking` - Universal tool
- `tractatus_thinking` - Universal tool

**Keep in project configs:**
- `filesystem` - Project-specific paths
- `exarp` - Project-specific
- `notebooklm` - Project-specific
- `interactive` - Project-specific

### Option 2: Remove from One Workspace

Remove duplicate servers from one workspace config, keeping them in the other.

### Option 3: Use Global Config Only

Move all common servers to global config, keep only project-specific ones in workspace configs.

---

## Recommended Actions

### Immediate Fix

1. **Move common servers to global config** (`~/.cursor/mcp.json`):
   - `agentic-tools`
   - `context7`
   - `sequential_thinking`
   - `tractatus_thinking`

2. **Remove these servers from workspace configs**

3. **Keep project-specific servers in workspace configs**:
   - `filesystem` (has project-specific paths)
   - `exarp` (project-specific)
   - `interactive` (project-specific)

### Long-Term Strategy

1. **Global Config** (`~/.cursor/mcp.json`): Universal servers used across all projects
2. **Workspace Config** (`.cursor/mcp.json`): Project-specific servers only

---

## Verification

After fixing:
1. Run: `python3 scripts/find_duplicate_mcp_servers.py`
2. Should show: "✅ No duplicate server names found"
3. Restart Cursor completely
4. Check Cursor Settings → MCP Servers

---

**Last Updated**: 2025-11-30  
**Tool**: `scripts/find_duplicate_mcp_servers.py`

