# MCP Duplicate Servers - Fix Applied

**Date**: 2025-11-30  
**Status**: ✅ **Fixed**

---

## Actions Taken

### ✅ Moved to Global Config (`~/.cursor/mcp.json`)

The following servers were moved to global configuration (available in all projects):

1. **agentic-tools** - Task management and agent memories
2. **context7** - Documentation lookup
3. **sequential_thinking** - Structured problem-solving
4. **tractatus_thinking** - Logical analysis

### ✅ Removed from Workspace Configs

These servers were removed from:
- `project-management-automation/.cursor/mcp.json`
- `ib_box_spread_full_universal/.cursor/mcp.json`

### ✅ Kept in Workspace Configs (Project-Specific)

These servers remain in their respective workspace configs:

**project-management-automation:**
- `filesystem` - Project-specific file operations
- `interactive` - Project-specific interactive prompts

**ib_box_spread_full_universal:**
- `exarp` - Project-specific automation
- `filesystem` - Project-specific file operations
- `notebooklm` - Project-specific research tool

---

## Result

- ✅ **4 duplicate servers fixed** (moved to global config)
- ⚠️ **1 expected duplicate remaining** (`filesystem` - project-specific paths)
- ✅ Common servers in global config (accessible from all projects)
- ✅ Project-specific servers in workspace configs
- ✅ Backups created before changes

### Note on `filesystem` Server

The `filesystem` server appears in both workspace configs because:
- Each workspace needs its own filesystem server with project-specific paths
- `project-management-automation`: Uses workspace path `/Volumes/SSD1_APFS/project-management-automation`
- `ib_box_spread_full_universal`: Uses its own workspace path

**This is expected behavior** - not a true duplicate, as each instance serves a different workspace.

---

## Next Steps

### ⚠️ IMPORTANT: Restart Cursor

1. **Quit Cursor completely** (not just reload window)
2. **Reopen Cursor**
3. **Verify in Settings**:
   - Settings → MCP Servers
   - Each server should appear only once
   - Global servers should be available in all projects

### Verification

After restarting, run:
```bash
python3 scripts/find_duplicate_mcp_servers.py
```

Should show: "✅ No duplicate server names found"

---

## Backup Files

Backups were created before changes:
- `~/.cursor/mcp.json.backup` - Global config backup
- `.cursor/mcp.json.backup` - Project config backup (if existed)

---

**Fix Applied**: 2025-11-30  
**Tool Used**: `scripts/fix_duplicate_mcp_servers.py --apply`

