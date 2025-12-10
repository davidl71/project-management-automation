# Exarp MCP Configuration Fix


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-30  
**Status**: ✅ **Fixed**

---

## Problem

The exarp MCP server was showing an old version because:

1. **Wrong Source**: The MCP configuration was using `uvx exarp --mcp`, which pulls from PyPI or a globally installed version
2. **Python Version Mismatch**: System Python 3.9.6 doesn't support `str | None` syntax (requires Python 3.10+)
3. **Not Using Local Code**: The configuration wasn't pointing to the local project directory

---

## Solution

Updated the MCP configuration in `ib_box_spread_full_universal/.cursor/mcp.json` to use the local project directory:

### Before:
```json
{
  "exarp": {
    "command": "uvx",
    "args": ["exarp", "--mcp"],
    "description": "..."
  }
}
```

### After:
```json
{
  "exarp": {
    "command": "uvx",
    "args": [
      "--from",
      "/Users/davidl/Projects/project-management-automation",
      "exarp",
      "--mcp"
    ],
    "description": "..."
  }
}
```

---

## Benefits

1. ✅ **Always Latest**: Uses code directly from the project directory
2. ✅ **Correct Python**: `uvx` automatically uses Python 3.10+ (from `pyproject.toml`)
3. ✅ **Version Match**: Version matches the current git commit (`a0e18c1d`)
4. ✅ **No Installation Needed**: No need to install to PyPI or globally

---

## Verification

After restarting Cursor:

1. **Check Version**: The exarp tools should show version `0.1.18.dev...ga0e18c1d`
2. **Test Tools**: Run an exarp tool (e.g., `exarp project scorecard`) to verify it works
3. **Check MCP Logs**: Verify the server starts without Python version errors

---

## ⚠️ IMPORTANT: Restart Required

**Restart Cursor completely** (not just reload) for the MCP configuration changes to take effect:

1. **Quit Cursor**: `Cmd + Q` (macOS) or exit completely
2. **Reopen Cursor**
3. **MCP Server Reloads**: The exarp server will restart with the new configuration

---

## Related Files

- `ib_box_spread_full_universal/.cursor/mcp.json` - Updated MCP configuration
- `pyproject.toml` - Requires Python 3.10+ (`requires-python = ">=3.10"`)
- `project_management_automation/version.py` - Version information

---

**Fix Applied**: 2025-11-30  
**Configuration File**: `ib_box_spread_full_universal/.cursor/mcp.json`

