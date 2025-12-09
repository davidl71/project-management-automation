# Finding Duplicate Exarp MCP Instances

**Date**: 2025-12-09  
**Status**: Investigating user report of multiple instances

---

## Investigation Results

### Config File Analysis

**User-Level Config (`~/.cursor/mcp.json`)**:
- ✅ **1 exarp_pma instance found**
- Command: `/Users/davidl/Projects/project-management-automation/exarp-uvx-wrapper.sh`
- Args: `["--mcp"]`

**Total MCP Servers**: 8
- GitKraken
- agentic-tools
- context7
- devwisdom
- **exarp_pma** ← Only one
- notebooklm
- sequential_thinking
- tractatus_thinking

### Project-Level Configs

**Checked**: All project-specific configs in `~/.cursor/projects/`
- ✅ **0 exarp_pma instances found**

**Checked**: All workspace configs in project directories
- ✅ **0 exarp_pma instances found**

### Running Processes

Found **4 running Exarp processes**:
1. PID 34114: `exarp --mcp` (active MCP server)
2. PID 34088: `uvx --with-editable ... exarp --mcp` (wrapper)
3. PID 33624: `exarp` (previous instance)
4. PID 33613: `uvx --with-editable ... exarp` (previous wrapper)

**Note**: Multiple processes are expected when:
- Cursor has multiple MCP connections
- Server is restarting
- Old processes haven't been cleaned up

---

## Possible Reasons for "Multiple Instances"

### 1. Running Processes (Not Config Duplicates)

If you see multiple instances in Cursor's MCP server list, it might be showing:
- **Active connections** (multiple Cursor windows/workspaces)
- **Cached connections** (old processes not cleaned up)
- **Restart attempts** (server restarting)

**Solution**: Kill old processes:
```bash
# Find all exarp processes
ps aux | grep exarp | grep -v grep

# Kill specific PIDs
kill <PID>

# Or kill all exarp processes
pkill -f "exarp.*--mcp"
```

### 2. Workspace-Specific Configs

Cursor might be loading workspace-specific configs that override user-level config.

**Check**: Look for `.cursor/mcp.json` in your workspace directories:
```bash
find ~/Projects -name ".cursor" -type d | xargs find -name "mcp.json*"
```

### 3. Extension Configs

Some Cursor extensions might register their own MCP servers.

**Check**: Extension configs in `~/.cursor/extensions/`

---

## Verification Commands

### Count Exarp Instances in Config
```bash
cat ~/.cursor/mcp.json | jq '[.mcpServers | to_entries[] | select(.key | contains("exarp") or .value.command | contains("exarp"))] | length'
```

### List All Exarp-Related Servers
```bash
cat ~/.cursor/mcp.json | jq -r '.mcpServers | to_entries[] | select(.key | contains("exarp") or .value.command | contains("exarp")) | "\(.key): \(.value.command)"'
```

### Check Running Processes
```bash
ps aux | grep -E "exarp|project_management_automation" | grep -v grep
```

### Find All MCP Config Files
```bash
find ~/.cursor ~/Projects -name "mcp.json*" 2>/dev/null | xargs grep -l "exarp"
```

---

## Next Steps

If you're seeing multiple instances in Cursor's UI:

1. **Check Cursor's MCP Server Status**:
   - Open Cursor Settings
   - Go to MCP Servers section
   - Count how many "exarp_pma" entries you see

2. **Check Running Processes**:
   ```bash
   ps aux | grep exarp | grep -v grep
   ```

3. **Restart Cursor**:
   - Quit Cursor completely
   - Kill any remaining exarp processes
   - Restart Cursor

4. **Check for Workspace Configs**:
   - Look in your current workspace for `.cursor/mcp.json`
   - Check if it has an `exarp_pma` entry

---

## Current Status

✅ **Config File**: Only 1 `exarp_pma` instance  
✅ **Project Configs**: 0 duplicates found  
⚠️ **Running Processes**: 4 processes (may appear as multiple instances in UI)

**Recommendation**: If you see multiple instances in Cursor's UI, it's likely due to running processes, not config duplicates. Try restarting Cursor and killing old processes.

---

**Last Updated**: 2025-12-09

