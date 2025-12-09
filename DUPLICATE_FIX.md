# Duplicate Exarp MCP Instance - FIXED

**Date**: 2025-12-09  
**Status**: ✅ **Fixed**

---

## Problem Found

**Duplicate `exarp_pma` instance** in project-level config:
- User-level: `~/.cursor/mcp.json` ✅ (keep this one)
- Project-level: `/Users/davidl/Projects/project-management-automation/.cursor/mcp.json` ❌ (removed)

---

## Solution Applied

Removed `exarp_pma` from project-level config:
```bash
jq 'del(.mcpServers.exarp_pma)' .cursor/mcp.json > .cursor/mcp.json
```

**Result**: Only user-level instance remains

---

## Verification

### Before Fix
- User-level: 1 instance ✅
- Project-level: 1 instance ❌
- **Total**: 2 instances (duplicate)

### After Fix
- User-level: 1 instance ✅
- Project-level: 0 instances ✅
- **Total**: 1 instance (correct)

---

## Why This Happened

Cursor loads MCP servers from:
1. **User-level config** (`~/.cursor/mcp.json`) - Global settings
2. **Workspace-level config** (`.cursor/mcp.json` in project) - Project-specific overrides

Having `exarp_pma` in both created duplicate instances.

---

## Best Practice

**Keep MCP servers in user-level config only** unless:
- You need different settings per project
- You want to disable a server for a specific project

For Exarp, user-level config is sufficient since it uses `PROJECT_ROOT` environment variable to detect the current project.

---

## Next Steps

1. ✅ **Fixed**: Removed duplicate from project config
2. **Restart Cursor**: Quit and restart Cursor to clear duplicate instances
3. **Verify**: Check Cursor's MCP server list - should show only one `exarp_pma`

---

**Last Updated**: 2025-12-09  
**Status**: ✅ Fixed

