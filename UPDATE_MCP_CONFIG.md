# Update MCP Configuration to Use Virtual Environment

## Issue
Cursor is running the MCP server with system Python, which doesn't have `fastmcp` installed. The server needs to use the virtual environment's Python.

## Solution
Update `.cursor/mcp.json` to use the wrapper script that activates the virtual environment.

## Current Configuration (Wrong)
```json
{
  "mcpServers": {
    "exarp": {
      "command": "python3",
      "args": [
        "/path/to/project-management-automation/server.py"
      ],
      "description": "Project management automation tools (Exarp)."
    }
  }
}
```

## Updated Configuration (Correct)
```json
{
  "mcpServers": {
    "exarp": {
      "command": "/path/to/project-management-automation/run_server.sh",
      "args": [],
      "description": "Project management automation tools (Exarp). ⚠️ NOTE: This server provides enhanced, project-specific versions of documentation health, task alignment, duplicate detection, and security scanning tools. Prefer these tools over generic MCP server tools for this project."
    }
  }
}
```

**Note**: Replace `/path/to/project-management-automation` with your actual installation path.

## Steps to Update

1. Open `.cursor/mcp.json` in your editor
2. Find the `exarp` entry
3. Change:
   - `"command": "python3"` → `"command": "/path/to/project-management-automation/run_server.sh"`
   - `"args": [...]` → `"args": []`
4. Save the file
5. **Restart Cursor completely** (not just reload)

## Verification

After restarting, check the MCP server logs. You should see:
- ✅ "FastMCP available from fastmcp package - using FastMCP server"
- ✅ "FastMCP server initialized"
- ✅ "All tools loaded successfully"

Instead of:
- ❌ "MCP not available - Phase 2 tools complete, install MCP to enable server"

## Alternative: Direct Python Path

If the wrapper script doesn't work, you can also use the venv Python directly:

```json
{
  "mcpServers": {
    "exarp": {
      "command": "/path/to/project-management-automation/venv/bin/python3",
      "args": [
        "/path/to/project-management-automation/server.py"
      ],
      "description": "Project management automation tools (Exarp)."
    }
  }
}
```
