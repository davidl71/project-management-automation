# Cursor Doc Resources Setup Guide

> **Guide for indexing external developer documentation in Cursor IDE**

**Date**: 2025-11-30  
**Status**: ✅ Complete

---

## Overview

This guide explains how to set up external developer documentation as Cursor "Doc" resources. You have two options:

1. **Cursor Doc Resources** - Index documentation directly in Cursor
2. **Context7 MCP** - Use MCP server for up-to-date library docs (recommended for many libraries)

---

## Option 1: Cursor Doc Resources (Direct Indexing)

### What to Index

Based on project dependencies and usage, index these resources:

#### Essential (Must Have)

1. **FastMCP Documentation**
   - URL: `https://gofastmcp.com`
   - Why: Primary MCP framework
   - Always index - project-specific

2. **Model Context Protocol Specification**
   - URL: `https://modelcontextprotocol.io`
   - Why: Core protocol reference
   - Always index - protocol spec

3. **VS Code Extension API**
   - URL: `https://code.visualstudio.com/api`
   - Why: For Cursor extension development
   - Index if working on extensions

#### Recommended (If Not Using Context7)

4. **Pydantic Documentation**
   - URL: `https://docs.pydantic.dev/`
   - Why: Data validation (v2.0+)
   - **Note**: Context7 provides this - skip if using Context7

5. **Python Documentation**
   - URL: `https://docs.python.org/3/`
   - Why: Standard library reference
   - **Note**: Context7 provides this - skip if using Context7

6. **pytest Documentation**
   - URL: `https://docs.pytest.org/`
   - Why: Testing framework
   - **Note**: Context7 provides this - skip if using Context7

#### Optional

7. **Ruff Documentation** - `https://docs.astral.sh/ruff/`
8. **Black Documentation** - `https://black.readthedocs.io/`
9. **mypy Documentation** - `https://mypy.readthedocs.io/`
10. **setuptools Documentation** - `https://setuptools.pypa.io/`

---

## How to Add Doc Resources in Cursor

### Method 1: Via Settings UI

1. **Open Cursor Settings**
   - `Cmd+,` (macOS) or `Ctrl+,` (Windows/Linux)
   - Or: `Cursor` → `Settings` → `Features` → `Docs`

2. **Add Doc Resource**
   - Click "Add Doc Resource" or "+"
   - Enter the URL (e.g., `https://gofastmcp.com`)
   - Cursor will automatically index the documentation

3. **Verify Indexing**
   - Check `Context` → `Codebase Indexing` in Cursor
   - Wait for indexing to complete (may take a few minutes)

### Method 2: Via Configuration File

1. **Create `.cursor/docs.json`** (already created in this project)
   - See `.cursor/docs.json` for the configuration
   - Cursor may auto-detect this file

2. **Manual Configuration** (if needed)
   - Add to Cursor settings JSON:
   ```json
   {
     "cursor.docResources": [
       {
         "url": "https://gofastmcp.com",
         "name": "FastMCP Documentation"
       },
       {
         "url": "https://modelcontextprotocol.io",
         "name": "MCP Specification"
       }
     ]
   }
   ```

---

## Option 2: Context7 MCP (Recommended for Library Docs)

### Why Use Context7?

Context7 MCP provides:
- ✅ **Always up-to-date** (2025)
- ✅ **Version-specific** API references
- ✅ **Real code examples** (no hallucinations)
- ✅ **Current best practices**

### Current Status

✅ **Context7 is already configured** in this project!

**Configuration**: `.cursor/mcp.json` (or global `~/.cursor/mcp.json`)

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

### How to Use Context7

**In your prompts, append `use context7`:**

```
"How do I use Pydantic patterns? use context7"
"Show me Pydantic examples use context7"
"Pydantic best practices 2025 use context7"
"What's the latest FastMCP API? use context7"
```

### What Context7 Covers

Context7 provides documentation for:
- ✅ Pydantic
- ✅ Python (standard library)
- ✅ pytest
- ✅ FastMCP
- ✅ Most popular Python libraries

**You don't need to index these in Cursor Docs if using Context7!**

---

## Recommended Setup Strategy

### Hybrid Approach (Best of Both Worlds)

1. **Use Context7 for Library Docs**
   - Pydantic, Python, pytest, etc.
   - Always up-to-date, version-specific

2. **Index in Cursor Docs for Project-Specific**
   - FastMCP docs (project-specific framework)
   - MCP Protocol spec (core reference)
   - VS Code Extension API (if working on extensions)

### Minimal Setup (Context7 Only)

If you're using Context7, you only need to index:

1. **FastMCP Documentation** - `https://gofastmcp.com`
2. **MCP Protocol Specification** - `https://modelcontextprotocol.io`
3. **VS Code Extension API** - `https://code.visualstudio.com/api` (if needed)

Everything else can come from Context7!

---

## Using Doc Resources in Cursor

### Reference in Prompts

Once indexed, reference docs using `@Doc`:

```
"Using @FastMCP Documentation, show me how to create a tool with async context"
"According to @MCP Specification, what are the resource URI patterns?"
"Based on @VS Code Extension API, how do I create a status bar item?"
```

### Automatic Context

Cursor automatically includes relevant doc context when:
- You mention library names in prompts
- You ask about API patterns
- You reference concepts from the docs

---

## Verification

### Check if Context7 is Working

```bash
# In Cursor chat, try:
"Get FastMCP documentation use context7"
```

If Context7 responds with documentation, it's working!

### Check if Doc Resources are Indexed

1. Open Cursor Settings
2. Go to `Features` → `Docs`
3. Verify resources are listed
4. Check indexing status

---

## Configuration Reference

See `.cursor/docs.json` for the complete configuration of recommended resources.

---

## Troubleshooting

### Doc Resources Not Indexing

1. **Check URL accessibility** - Ensure URLs are accessible
2. **Wait for indexing** - Large docs may take time
3. **Check Cursor logs** - Look for indexing errors
4. **Try manual refresh** - Re-index from settings

### Context7 Not Working

1. **Verify MCP config** - Check `.cursor/mcp.json` or `~/.cursor/mcp.json`
2. **Check npx** - Ensure `npx` is available: `which npx`
3. **Test manually** - Try: `npx -y @upstash/context7-mcp`
4. **Restart Cursor** - MCP servers load on startup

### Both Not Working

1. **Check Cursor version** - Ensure latest version
2. **Check MCP support** - Verify MCP is enabled in settings
3. **Check network** - Ensure internet access for Context7
4. **Review logs** - Check Cursor developer console

---

## Quick Start Checklist

- [ ] **Verify Context7 is configured** (check `.cursor/mcp.json`)
- [ ] **Test Context7** ("Get Pydantic docs use context7")
- [ ] **Index FastMCP docs** (add `https://gofastmcp.com` to Cursor Docs)
- [ ] **Index MCP spec** (add `https://modelcontextprotocol.io` to Cursor Docs)
- [ ] **Index VS Code API** (if working on extensions)
- [ ] **Verify indexing** (check Cursor settings)
- [ ] **Test in prompts** (use `@Doc` references)

---

## Related Documentation

- [CONTEXT7_MCP_INTEGRATION_STATUS.md](CONTEXT7_MCP_INTEGRATION_STATUS.md) - Context7 integration details
- [EXARP_FASTMCP_SETUP.md](EXARP_FASTMCP_SETUP.md) - FastMCP setup guide
- [MCP_SERVERS_USAGE_GUIDE.md](MCP_SERVERS_USAGE_GUIDE.md) - MCP server usage patterns
- [RECOMMENDED_MCP_COMPANIONS.md](RECOMMENDED_MCP_COMPANIONS.md) - Recommended MCP servers

---

**Last Updated**: 2025-11-30  
**Status**: ✅ Complete

