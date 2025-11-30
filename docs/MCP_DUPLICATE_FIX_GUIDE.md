# Fix Duplicate MCP Servers

**Date**: 2025-11-30  
**Issue**: 5 duplicate MCP servers found across workspace configurations

---

## Problem Summary

You have **5 duplicate MCP servers** configured in both:
- `project-management-automation/.cursor/mcp.json`
- `ib_box_spread_full_universal/.cursor/mcp.json`

When Cursor merges configurations from multiple workspaces, these servers appear twice.

**Duplicate Servers:**
1. `agentic-tools`
2. `context7`
3. `filesystem`
4. `sequential_thinking`
5. `tractatus_thinking`

---

## Quick Fix

### Option 1: Automated Fix (Recommended)

```bash
cd /Users/davidl/Projects/project-management-automation
python3 scripts/fix_duplicate_mcp_servers.py --apply
```

This will:
- Move common servers to global config (`~/.cursor/mcp.json`)
- Remove duplicates from workspace configs
- Create backups before making changes

### Option 2: Manual Fix

1. **Move common servers to global config** (`~/.cursor/mcp.json`):
   - `agentic-tools`
   - `context7`
   - `sequential_thinking`
   - `tractatus_thinking`

2. **Remove these servers from**:
   - `project-management-automation/.cursor/mcp.json`
   - `ib_box_spread_full_universal/.cursor/mcp.json`

3. **Keep project-specific servers in workspace configs**:
   - `filesystem` (has project-specific paths)
   - `exarp` (project-specific)
   - `interactive` (project-specific)

---

## Verification

1. **Check for duplicates:**
   ```bash
   python3 scripts/find_duplicate_mcp_servers.py
   ```
   Should show: "✅ No duplicate server names found"

2. **Restart Cursor completely** (not just reload)

3. **Verify in Cursor**:
   - Settings → MCP Servers
   - Each server should appear only once

---

## Files Created

- ✅ `scripts/find_duplicate_mcp_servers.py` - Detect duplicates
- ✅ `scripts/fix_duplicate_mcp_servers.py` - Fix duplicates
- ✅ `docs/MCP_DUPLICATE_SERVERS_REPORT.md` - Full report

---

**Last Updated**: 2025-11-30

