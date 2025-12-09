# Remaining Duplicate Investigation

**Date**: 2025-12-09  
**Status**: ⚠️ **Still Investigating**

---

## Current Status

User reports: **2 exarp_pma instances** visible in Cursor UI  
Config file shows: **1 exarp_pma instance** in `~/.cursor/mcp.json`

---

## Investigation Results

### Config File Analysis

**User-Level Config (`~/.cursor/mcp.json`)**:
- ✅ **1 exarp_pma instance** (verified multiple ways)
- Command: `/Users/davidl/Projects/project-management-automation/exarp-uvx-wrapper.sh`
- No duplicate keys in JSON structure

**Project-Level Config**:
- ✅ **0 exarp_pma instances** (removed in previous fix)

### Possible Causes

#### 1. Cursor Cache
Cursor may be caching old MCP server instances. The `mcp-cache.json` files might contain stale references.

**Solution**: Clear Cursor cache or restart Cursor completely.

#### 2. Multiple Running Processes
Cursor might be showing multiple processes as separate instances:
- PID 34114: `exarp --mcp` (active)
- PID 34088: `uvx --with-editable ... exarp` (wrapper)

**Solution**: Kill old processes and restart Cursor.

#### 3. Workspace-Specific Configs
There might be workspace configs in other projects that haven't been checked yet.

**Solution**: Check all workspace `.cursor/mcp.json` files.

#### 4. Extension Configs
Some Cursor extensions might register their own MCP servers.

**Solution**: Check extension configs.

---

## Verification Commands

### Check Config File
```bash
cat ~/.cursor/mcp.json | jq '[.mcpServers | to_entries[] | select(.key == "exarp_pma")] | length'
# Should return: 1
```

### Check Running Processes
```bash
ps aux | grep -E "exarp.*--mcp|exarp-uvx-wrapper" | grep -v grep
```

### Clear Cursor Cache
```bash
# Quit Cursor completely first, then:
rm -rf ~/.cursor/projects/*/mcp-cache.json
```

### Find All Config Files
```bash
find ~/.cursor ~/Projects -name "mcp.json*" 2>/dev/null | xargs grep -l "exarp_pma"
```

---

## Recommended Actions

1. **Quit Cursor completely** (not just close window)
2. **Kill all exarp processes**:
   ```bash
   pkill -f "exarp.*--mcp"
   pkill -f "exarp-uvx-wrapper"
   ```
3. **Clear MCP cache** (optional):
   ```bash
   rm -rf ~/.cursor/projects/*/mcp-cache.json
   ```
4. **Restart Cursor**
5. **Verify**: Check MCP server list - should show only 1 `exarp_pma`

---

## Next Steps

If 2 instances still appear after restart:
1. Check Cursor's MCP server status panel
2. Look for any workspace-specific configs
3. Check if Cursor is loading from multiple config sources
4. Verify no extension is registering duplicate servers

---

**Last Updated**: 2025-12-09  
**Status**: ⚠️ Awaiting user feedback after Cursor restart

