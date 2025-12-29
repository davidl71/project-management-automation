# Todo2 MCP Server Configuration Guide

**Date**: 2025-12-29  
**Status**: ✅ Working Configuration Documented

---

## Overview

Todo2 is a Cursor extension that provides AI-powered task management with built-in MCP server integration. This guide documents the correct configuration to enable Todo2 MCP tools in Cursor.

---

## Prerequisites

1. **Todo2 Extension Installed**: The Todo2 extension must be installed in Cursor
   - Extension ID: `todo2.todo2`
   - Check installation: Cursor → Extensions → Search "Todo2"

2. **Node.js Available**: The MCP server is a Node.js script, so `node` must be available in your PATH

---

## Configuration

### Correct Configuration

Add the following to your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "todo2": {
      "command": "node",
      "args": [
        "/Users/YOUR_USERNAME/.cursor/extensions/todo2.todo2-VERSION/dist/mcp-server.js"
      ],
      "env": {
        "TODO2_WORKSPACE_PATH": "/path/to/your/project"
      },
      "description": "Todo2 MCP server for task management with workflow enforcement"
    }
  }
}
```

### Configuration Details

**Command**: `node`  
- Runs the JavaScript MCP server file

**Args**: Path to the MCP server file
- **Location**: `~/.cursor/extensions/todo2.todo2-VERSION/dist/mcp-server.js`
- **Version**: The version number in the path changes when the extension updates
- **Example**: `/Users/davidl/.cursor/extensions/todo2.todo2-0.0.9-universal/dist/mcp-server.js`

**Environment Variables**:
- `TODO2_WORKSPACE_PATH`: **Required** - Set to your project root directory
  - This tells Todo2 where to find/create the `.todo2/state.todo2.json` file

---

## Finding Your Extension Path

To find the correct path to your Todo2 extension:

```bash
# List Todo2 extensions
ls -la ~/.cursor/extensions/ | grep todo2

# Example output:
# drwxr-xr-x@ 10 user  staff  320 Dec  9 23:49 todo2.todo2-0.0.9-universal

# The full path would be:
# ~/.cursor/extensions/todo2.todo2-0.0.9-universal/dist/mcp-server.js
```

Or use this command to get the exact path:

```bash
find ~/.cursor/extensions -name "todo2.todo2-*" -type d | head -1 | xargs -I {} echo "{}/dist/mcp-server.js"
```

---

## Common Errors and Solutions

### Error: `extension-todo2` not found on npm

**Problem**: Cursor tries to auto-configure Todo2 using a non-existent npm package.

**Solution**: 
- ❌ **Don't use**: `"command": "npx", "args": ["-y", "extension-todo2"]`
- ✅ **Use**: Direct path to the extension's `mcp-server.js` file (see configuration above)

### Error: No server info found

**Problem**: The MCP server file path is incorrect or the extension was updated.

**Solution**:
1. Check if the extension path exists: `ls ~/.cursor/extensions/todo2.todo2-*/dist/mcp-server.js`
2. Update the path in `mcp.json` if the version number changed
3. Restart Cursor completely

### Error: TODO2_WORKSPACE_PATH not set

**Problem**: The environment variable is missing or incorrect.

**Solution**:
- Ensure `TODO2_WORKSPACE_PATH` is set to your project root (absolute path)
- Example: `"/Users/davidl/Projects/project-management-automation"`

---

## Verification

After configuration:

1. **Restart Cursor completely** (not just reload window)

2. **Check MCP Server Status**:
   - Cursor Settings → MCP Servers
   - Look for `todo2` in the list
   - Should show as "Connected" or "Running"

3. **Test Todo2 Tools**:
   The following tools should be available:
   - `mcp_extension-todo2_list_todos`
   - `mcp_extension-todo2_create_todos`
   - `mcp_extension-todo2_update_todos`
   - `mcp_extension-todo2_get_todo_details`
   - `mcp_extension-todo2_add_comments`
   - `mcp_extension-todo2_delete_todos`

4. **Verify Workspace File**:
   - Check that `.todo2/state.todo2.json` exists in your project root
   - This file is created automatically when Todo2 MCP server starts

---

## Updating After Extension Updates

When the Todo2 extension updates, the version number in the path changes:

**Before Update**:
```
~/.cursor/extensions/todo2.todo2-0.0.9-universal/dist/mcp-server.js
```

**After Update** (example):
```
~/.cursor/extensions/todo2.todo2-0.1.0-universal/dist/mcp-server.js
```

**Action Required**:
1. Find the new extension path (see "Finding Your Extension Path" above)
2. Update the path in `.cursor/mcp.json`
3. Restart Cursor

**Automation Script** (optional):

You can create a script to auto-update the path:

```bash
#!/bin/bash
# update_todo2_mcp_path.sh

EXT_PATH=$(find ~/.cursor/extensions -name "todo2.todo2-*" -type d | head -1)
MCP_FILE="$EXT_PATH/dist/mcp-server.js"
PROJECT_ROOT=$(pwd)

if [ -f "$MCP_FILE" ]; then
  # Update mcp.json with new path
  python3 << EOF
import json
import os

with open('.cursor/mcp.json', 'r') as f:
    config = json.load(f)

if 'todo2' in config.get('mcpServers', {}):
    config['mcpServers']['todo2']['args'] = ['$MCP_FILE']
    config['mcpServers']['todo2']['env']['TODO2_WORKSPACE_PATH'] = '$PROJECT_ROOT'
    
    with open('.cursor/mcp.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Updated Todo2 MCP path to: $MCP_FILE")
else:
    print("⚠️ Todo2 not found in mcp.json")
EOF
else
  echo "❌ Todo2 extension not found"
fi
```

---

## Available Todo2 MCP Tools

Once configured, the following tools are available:

### `mcp_extension-todo2_list_todos`
List all todos with optional filters (status, priority, tags, dependency readiness).

### `mcp_extension-todo2_create_todos`
Create one or more todo items with priority and tags (handles both single and bulk creation).

### `mcp_extension-todo2_update_todos`
Update one or more todos (content, priority, tags, status, dependencies) - handles both single and bulk updates.

### `mcp_extension-todo2_get_todo_details`
Get detailed information about one or more todos including all associated comments.

### `mcp_extension-todo2_add_comments`
Add one or more comments to a todo with specified types and markdown content.

### `mcp_extension-todo2_delete_todos`
Delete one or more todo items (handles both single and bulk deletion).

---

## Integration with Project

This project uses Todo2 MCP tools for:
- Task management and workflow enforcement
- Research protocol tracking
- Task status management (Todo → In Progress → Review → Done)
- Comment management (research_with_links, result, note, manualsetup)

See `.cursor/rules/todo2.mdc` for complete workflow requirements.

---

## Troubleshooting

### MCP Server Not Starting

1. **Check Node.js**: `node --version` (should be v16+)
2. **Check Extension Path**: Verify the path exists
3. **Check Environment Variable**: Ensure `TODO2_WORKSPACE_PATH` is set correctly
4. **Check Cursor Logs**: Look for MCP server errors in Cursor's output panel

### Tools Not Available

1. **Restart Cursor**: Completely quit and restart Cursor
2. **Check MCP Status**: Settings → MCP Servers → Verify `todo2` is connected
3. **Check Extension**: Ensure Todo2 extension is enabled in Cursor

### Workspace File Not Created

1. **Check Permissions**: Ensure you can write to the project directory
2. **Check Path**: Verify `TODO2_WORKSPACE_PATH` points to the correct directory
3. **Manual Creation**: Create `.todo2/` directory if needed (Todo2 will create the JSON file)

---

## References

- [Todo2 Extension](https://todo2.pro)
- [Cursor MCP Documentation](https://docs.cursor.com/context/model-context-protocol)
- [Todo2 MCP Integration Analysis](./TODO2_MCP_INTEGRATION_ANALYSIS.md)

---

## Summary

✅ **Working Configuration**:
- Command: `node`
- Args: Full path to `~/.cursor/extensions/todo2.todo2-VERSION/dist/mcp-server.js`
- Environment: `TODO2_WORKSPACE_PATH` set to project root
- Result: Todo2 MCP tools available in Cursor

❌ **Common Mistake**:
- Don't use: `npx -y extension-todo2` (package doesn't exist)
- Use: Direct path to extension's MCP server file

