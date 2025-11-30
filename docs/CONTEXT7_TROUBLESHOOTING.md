# Context7 MCP Troubleshooting Guide

> **Quick reference for diagnosing and fixing Context7 MCP issues**

**Date**: 2025-11-30  
**Status**: ✅ Context7 Configured

---

## ✅ Current Configuration

Context7 is **already configured** in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "uvx",
      "args": [
        "mcpower-proxy==0.0.87",
        "--wrapped-config",
        "{\"command\": \"npx\", \"args\": [\"-y\", \"@upstash/context7-mcp\"]}",
        "--name",
        "context7"
      ],
      "description": "Up-to-date documentation lookup for libraries and frameworks"
    }
  }
}
```

---

## Quick Verification

### 1. Check if Context7 is Available

```bash
# Test npx can run Context7
npx -y @upstash/context7-mcp --help

# Test uvx wrapper
uvx mcpower-proxy==0.0.87 --help
```

### 2. Verify MCP Configuration

```bash
# Check project config exists
cat .cursor/mcp.json | grep -A 10 context7

# Check global config (if using)
cat ~/.cursor/mcp.json | grep -A 10 context7
```

### 3. Check Cursor MCP Status

1. Open Cursor Settings (`Cmd+,` or `Ctrl+,`)
2. Go to **Features** → **MCP**
3. Look for `context7` in the list of MCP servers
4. Check if it shows as "Connected" or has any errors

---

## Common Issues & Solutions

### Issue 1: Context7 Not Appearing in Cursor

**Symptoms:**
- Context7 doesn't appear in MCP server list
- Prompts with "use context7" don't work

**Solutions:**

1. **Restart Cursor**
   - Fully quit and restart Cursor
   - MCP servers only load on startup

2. **Check Configuration Location**
   - Project config: `.cursor/mcp.json` (project root)
   - Global config: `~/.cursor/mcp.json` (home directory)
   - Cursor uses project config if it exists, otherwise global

3. **Verify JSON Syntax**
   ```bash
   # Check for JSON syntax errors
   python3 -m json.tool .cursor/mcp.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
   ```

4. **Check File Permissions**
   ```bash
   # Ensure file is readable
   ls -la .cursor/mcp.json
   ```

---

### Issue 2: Context7 Fails to Start

**Symptoms:**
- Context7 appears in list but shows error
- "Failed to connect" or "Server error" messages

**Solutions:**

1. **Test npx Directly**
   ```bash
   npx -y @upstash/context7-mcp --help
   ```
   - If this fails, check Node.js/npm installation

2. **Test uvx Wrapper**
   ```bash
   uvx mcpower-proxy==0.0.87 --help
   ```
   - If this fails, check uvx installation: `which uvx`

3. **Check Network Access**
   - Context7 needs internet to fetch documentation
   - Test: `curl -I https://context7.com`

4. **Check API Key (if required)**
   - Some Context7 features may need an API key
   - Set: `export CONTEXT7_API_KEY=your_key`
   - Or add to MCP config:
   ```json
   {
     "context7": {
       "command": "uvx",
       "args": [...],
       "env": {
         "CONTEXT7_API_KEY": "your_key"
       }
     }
   }
   ```

---

### Issue 3: Context7 Works But No Results

**Symptoms:**
- Context7 connects but returns empty results
- "Library not found" errors

**Solutions:**

1. **Use Correct Library Names**
   - Try: `pydantic`, `fastapi`, `pytest`
   - Not: `Pydantic`, `FastAPI` (case-sensitive sometimes)

2. **Check Prompt Format**
   ```
   ✅ "Get Pydantic documentation use context7"
   ✅ "Show me Pydantic examples use context7"
   ❌ "Get Pydantic docs" (missing "use context7")
   ```

3. **Try Different Topics**
   ```
   "Pydantic models use context7"
   "Pydantic validators use context7"
   "Pydantic v2 migration use context7"
   ```

---

### Issue 4: uvx or mcpower-proxy Not Found

**Symptoms:**
- "Command not found: uvx"
- "mcpower-proxy not found"

**Solutions:**

1. **Install uvx**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or via pip
   pip install uv
   ```

2. **Install mcpower-proxy**
   ```bash
   uvx mcpower-proxy==0.0.87 --help
   # This will auto-install if uvx is working
   ```

3. **Use Direct npx (Alternative Config)**
   
   If uvx isn't available, use direct npx:
   
   ```json
   {
     "mcpServers": {
       "context7": {
         "command": "npx",
         "args": ["-y", "@upstash/context7-mcp"],
         "description": "Up-to-date documentation lookup"
       }
     }
   }
   ```

---

## Testing Context7

### Test 1: Basic Connection

In Cursor chat, try:
```
"Test Context7 connection"
```

Should see Context7 tools available.

### Test 2: Get Documentation

```
"Get Pydantic documentation use context7"
```

Should return Pydantic docs.

### Test 3: Get Examples

```
"Show me Pydantic model examples use context7"
```

Should return code examples.

---

## Manual Testing (Command Line)

### Test Context7 MCP Server Directly

```bash
# Start Context7 in stdio mode
npx -y @upstash/context7-mcp --transport stdio

# In another terminal, test with MCP client
# (Requires MCP client tool)
```

### Test with curl (if HTTP mode)

```bash
# Start in HTTP mode
npx -y @upstash/context7-mcp --transport http --port 3000

# Test endpoint
curl http://localhost:3000/health
```

---

## Alternative: Use Cursor Doc Resources

If Context7 continues to have issues, you can index documentation directly:

1. **Add Pydantic Docs to Cursor**
   - Settings → Features → Docs
   - Add: `https://docs.pydantic.dev/`

2. **Reference in Prompts**
   ```
   "Using @Pydantic Documentation, show me model examples"
   ```

See [CURSOR_DOC_RESOURCES_SETUP.md](CURSOR_DOC_RESOURCES_SETUP.md) for details.

---

## Debugging Steps

### Step 1: Check Cursor Logs

1. Open Cursor
2. `Help` → `Toggle Developer Tools`
3. Check Console for MCP errors
4. Look for "context7" or "MCP" in error messages

### Step 2: Check MCP Server Logs

MCP servers log to:
- macOS: `~/Library/Logs/Cursor/mcp-*.log`
- Linux: `~/.config/Cursor/logs/mcp-*.log`
- Windows: `%APPDATA%\Cursor\logs\mcp-*.log`

### Step 3: Test Components Individually

```bash
# 1. Test Node.js/npx
node --version
npx --version

# 2. Test Context7 package
npx -y @upstash/context7-mcp --help

# 3. Test uvx
uvx --version

# 4. Test mcpower-proxy
uvx mcpower-proxy==0.0.87 --help
```

---

## Expected Behavior

### ✅ Working Correctly

- Context7 appears in Cursor MCP server list
- Status shows "Connected" or "Ready"
- Prompts with "use context7" return documentation
- No errors in Cursor console

### ❌ Not Working

- Context7 doesn't appear in list
- Shows "Error" or "Failed" status
- Prompts return "Context7 not available"
- Errors in Cursor console

---

## Getting Help

If Context7 still doesn't work after troubleshooting:

1. **Check Context7 Status**
   - Visit: https://context7.com
   - Check for service status

2. **Review MCP Configuration**
   - See: [MCP_SERVERS_USAGE_GUIDE.md](MCP_SERVERS_USAGE_GUIDE.md)
   - See: [CURSOR_DOC_RESOURCES_SETUP.md](CURSOR_DOC_RESOURCES_SETUP.md)

3. **Check Cursor MCP Documentation**
   - Cursor Settings → Help → Documentation
   - Search for "MCP" or "Model Context Protocol"

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npx -y @upstash/context7-mcp --help` | Test Context7 installation |
| `uvx mcpower-proxy==0.0.87 --help` | Test uvx wrapper |
| `cat .cursor/mcp.json \| grep context7` | Check configuration |
| Restart Cursor | Reload MCP servers |

---

**Last Updated**: 2025-11-30  
**Status**: Context7 configured and ready

