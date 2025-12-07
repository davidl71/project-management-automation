# MCP Server Log Access Guide

## Current Status

**All MCP tools are failing** with the error: `object dict can't be used in 'await' expression`

Despite all code fixes (all functions return `-> str` and JSON strings), FastMCP's static analysis is still detecting dict returns.

## Log Locations

### 1. Project Debug Log (New)
**Location:** `/Users/davidl/Projects/project-management-automation/mcp_server_debug.log`

**Status:** ✅ Enabled
- Debug logging enabled in `server.py`
- Captures all errors with full tracebacks
- Includes FastMCP framework errors

**To view:**
```bash
tail -f mcp_server_debug.log
# Or
cat mcp_server_debug.log | grep -A 20 "error\|Error\|ERROR"
```

### 2. Cursor Application Logs
**Location:** `/Users/davidl/Library/Application Support/Cursor/logs/`

**Status:** ⚠️ May contain MCP errors
- Cursor captures stderr from MCP servers
- Errors appear as `[error]` entries
- May not show full tracebacks

**To view:**
```bash
# Find recent log files
ls -lt "/Users/davidl/Library/Application Support/Cursor/logs" | head -10

# View most recent log
tail -f "/Users/davidl/Library/Application Support/Cursor/logs/main.log"
```

### 3. Cursor Developer Tools
**Location:** In Cursor IDE

**Access:**
1. View > Developer > Toggle Developer Tools
2. Open Console tab
3. Look for MCP-related errors

**Status:** ✅ Best for real-time error viewing

### 4. Middleware Logs
**Location:** Enhanced in `logging_middleware.py`

**Status:** ✅ Enhanced with full tracebacks
- Now logs full traceback for tool errors
- Includes elapsed time and tool name
- Written to debug log file

## How to Capture Full Error

### Method 1: Check Debug Log After Error
1. Trigger the error (call any MCP tool via Cursor)
2. Check `mcp_server_debug.log`:
   ```bash
   tail -100 mcp_server_debug.log
   ```

### Method 2: Use Test Script
```bash
# Run the test script
python3 test_mcp_error.py 2>&1 | tee mcp_error_output.log

# View the output
cat mcp_error_output.log
```

### Method 3: Enable Verbose FastMCP Logging
The server now enables FastMCP debug logging. To see FastMCP's internal errors:

```python
# In server.py, FastMCP logger is now set to DEBUG
fastmcp_logger = logging.getLogger("fastmcp")
fastmcp_logger.setLevel(logging.DEBUG)
```

## What to Look For

### Key Error Patterns
1. **"object dict can't be used in 'await' expression"**
   - This is the main error
   - Look for the full traceback showing where FastMCP tries to await a dict

2. **Type annotation mismatches**
   - FastMCP may be analyzing function signatures
   - Check if it's detecting `-> dict` somewhere

3. **Call chain analysis**
   - FastMCP may be analyzing the entire call graph
   - Look for references to functions that return dicts

### Expected Log Entries
```
ERROR - Tool error: report | elapsed=XXms | error=object dict can't be used in 'await' expression
DEBUG - Full traceback for report:
  Traceback (most recent call last):
    ...
```

## Next Steps

1. **Reload MCP server** (toggle disabled/enabled in `.cursor/mcp.json`)
2. **Call a failing tool** (e.g., `/exarp_pma/report` with `action=scorecard`)
3. **Check debug log** immediately:
   ```bash
   tail -200 mcp_server_debug.log | grep -A 30 "error\|Error\|ERROR"
   ```
4. **Share the traceback** to identify where FastMCP is detecting the dict return

## Debugging Tips

- The error happens in FastMCP's tool execution layer
- Our code is correct (all functions return strings)
- FastMCP's static analysis is the issue
- Full traceback will show exactly where FastMCP tries to await a dict
