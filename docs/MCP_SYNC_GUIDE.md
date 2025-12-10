# MCP Feature Synchronization Guide


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Purpose**: Keep FastMCP and stdio server features (tools, resources, prompts) in sync.

**Last Updated**: 2025-12-11

---

## Overview

This project supports two MCP server interfaces:

1. **FastMCP** (primary): Auto-registers features via decorators (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`)
2. **Stdio Server** (fallback): Manually lists features in handler functions

**Problem**: Features must be registered in BOTH systems, or they'll be missing in stdio mode.

**Solution**: Follow this guide to ensure all features are registered in both systems.

### FastMCP-Only Features

Some features are **FastMCP-only** and cannot be replicated in stdio server:

1. **Middleware** (FastMCP 2 feature)
   - `SecurityMiddleware`: Rate limiting, path validation, access control
   - `LoggingMiddleware`: Request timing and logging
   - `ToolFilterMiddleware`: Dynamic tool loading based on workflow mode

2. **Resource Templates** (FastMCP 2 feature)
   - Dynamic resource template registration

3. **Advanced Features**:
   - Context primer resources
   - Hint registry resources
   - Auto-primer tools
   - Session mode resources
   - Prompt discovery resources and tools
   - Assignee management resources and tools
   - Capabilities resources
   - Session handoff tools
   - Lifespan support (startup/shutdown hooks)

**Note**: These features enhance FastMCP but are not required for basic functionality. Stdio server provides core tools, resources, and prompts without these enhancements.

---

## Quick Reference Checklist

When adding a new MCP feature, ensure you:

- [ ] Register in FastMCP (decorator)
- [ ] Register in stdio server (manual list)
- [ ] Add handler in stdio server `call_tool()` if it's a tool
- [ ] Verify sync with verification script
- [ ] Update this guide if patterns change

---

## 1. Tools

### FastMCP Registration

```python
@mcp.tool()
@ensure_json_string  # Required: ensures return type is str
def my_tool(
    param1: str = "default",
    param2: bool = False,
    param3: Optional[int] = None,
) -> str:
    """
    [HINT: Tool hint. Brief description.]
    
    Detailed description of what the tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        param3: Description of param3
    
    Returns:
        JSON string with results
    """
    # Implementation
    result = {"status": "success", "data": "..."}
    return json.dumps(result, indent=2)
```

**Location**: `project_management_automation/server.py`, inside `if mcp:` block (around line 743+)

**Key Requirements**:
- Must have `@ensure_json_string` decorator
- Must return `str` (JSON string)
- Must include `[HINT: ...]` in docstring
- Use type hints for all parameters

### Stdio Server Registration

**Step 1**: Add to `list_tools()` function

```python
# In @stdio_server_instance.list_tools() async def list_tools():
Tool(
    name="my_tool",
    description="[HINT: Tool hint. Brief description.]",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "default": "default",
                "description": "Description of param1",
            },
            "param2": {
                "type": "boolean",
                "default": False,
                "description": "Description of param2",
            },
            "param3": {
                "type": "integer",
                "description": "Description of param3",
            },
        },
    },
),
```

**Location**: `project_management_automation/server.py`, inside `elif stdio_server_instance:` block, `list_tools()` function (around line 790+)

**Step 2**: Add handler in `call_tool()` function

```python
# In @stdio_server_instance.call_tool() async def call_tool(name, arguments):
elif name == "my_tool":
    from .tools.my_module import my_tool as _my_tool
    result = _my_tool(
        arguments.get("param1", "default"),
        arguments.get("param2", False),
        arguments.get("param3"),
    )
    if not isinstance(result, str):
        result = json.dumps(result, indent=2)
```

**Location**: `project_management_automation/server.py`, inside `call_tool()` function (around line 1271+)

**Type Mapping**:
- `str` → `"type": "string"`
- `bool` → `"type": "boolean"`
- `int` → `"type": "integer"`
- `float` → `"type": "number"`
- `list[str]` → `"type": "array", "items": {"type": "string"}`
- `Optional[T]` → omit `"default"`, make description clear it's optional

---

## 2. Resources

### FastMCP Registration

```python
@mcp.resource("automation://my-resource")
def get_my_resource() -> str:
    """Get my resource data."""
    from .resources.my_module import get_my_resource_data
    result = get_my_resource_data()
    return json.dumps(result, indent=2)
```

**Location**: `project_management_automation/server.py`, inside `if mcp:` block (around line 3217+)

**URI Pattern**: `automation://<resource-name>` (use kebab-case)

### Stdio Server Registration

**For simple resources** (no parameters):

```python
# In @stdio_server_instance.list_resources() async def list_resources():
Resource(
    uri="automation://my-resource",
    name="My Resource",
    description="Get my resource data.",
    mimeType="application/json",
),
```

**For parameterized resources** (with `{param}` in URI):

Parameterized resources are handled via pattern matching in `read_resource()`, not listed in `list_resources()`. FastMCP handles these automatically, but stdio server needs explicit pattern matching:

```python
# In @stdio_server_instance.read_resource() async def read_resource(uri):
# Pattern matching for parameterized resources
if uri.startswith("automation://my-resource/"):
    param = uri.replace("automation://my-resource/", "")
    from .resources.my_module import get_my_resource_data
    result = get_my_resource_data(param)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]
```

**Note**: Parameterized resources may show as "missing" in verification script, but they're actually handled via pattern matching. This is expected behavior.

**Location**: 
- `list_resources()`: `project_management_automation/server.py` ~line 4150+
- `read_resource()`: `project_management_automation/server.py` ~line 4179+

---

## 3. Prompts

### FastMCP Registration

```python
@mcp.prompt()
def my_prompt(
    context: str,
    task_id: Optional[str] = None,
) -> list[PromptMessage]:
    """
    [HINT: Prompt hint. Brief description.]
    
    Detailed description of the prompt.
    
    Args:
        context: Description of context parameter
        task_id: Optional task ID
    """
    from mcp.types import PromptMessage
    
    messages = [
        PromptMessage(
            role="user",
            content=PromptMessageText(
                type="text",
                text=f"Context: {context}\nTask: {task_id or 'general'}",
            ),
        ),
    ]
    return messages
```

**Location**: `project_management_automation/server.py`, inside `if mcp:` block (around line 2792+)

**Key Requirements**:
- Must return `list[PromptMessage]`
- Use `PromptMessageText` for text content
- Include `[HINT: ...]` in docstring

### Stdio Server Registration

```python
# In @stdio_server_instance.list_prompts() async def list_prompts():
Prompt(
    name="my_prompt",
    description="[HINT: Prompt hint. Brief description.]",
    arguments=[
        PromptArgument(
            name="context",
            description="Description of context parameter",
            required=True,
        ),
        PromptArgument(
            name="task_id",
            description="Optional task ID",
            required=False,
        ),
    ],
),
```

**Location**: `project_management_automation/server.py`, inside `elif stdio_server_instance:` block, `list_prompts()` function (around line 4100+)

**Handler**:

```python
# In @stdio_server_instance.get_prompt() async def get_prompt(name, arguments):
if name == "my_prompt":
    from .prompts.my_module import my_prompt as _my_prompt
    messages = _my_prompt(
        arguments.get("context", ""),
        arguments.get("task_id"),
    )
    return messages
```

**Location**: `project_management_automation/server.py`, inside `get_prompt()` function (around line 4120+)

---

## Verification

### Manual Check

Run this script to verify sync:

```bash
uv run python scripts/verify_mcp_sync.py
```

### Automated Check (Script)

Create `scripts/verify_mcp_sync.py`:

```python
#!/usr/bin/env python3
"""Verify MCP features are in sync between FastMCP and stdio server."""

import re
from pathlib import Path

def verify_sync():
    server_file = Path("project_management_automation/server.py")
    content = server_file.read_text()
    
    # Extract FastMCP tools
    fastmcp_tools = set()
    for match in re.finditer(r'@mcp\.tool\(\)', content):
        start = match.end()
        next_lines = content[start:start+500]
        if content[max(0, match.start()-100):match.start()].strip().endswith('#'):
            continue
        func_match = re.search(r'(?:async\s+)?def\s+(\w+)\(', next_lines)
        if func_match and func_match.group(1) != 'call_tool':
            fastmcp_tools.add(func_match.group(1))
    
    # Extract stdio server tools
    stdio_tools = set(re.findall(r'Tool\(\s*name=[\"\'](\w+)[\"\']', content))
    
    # Extract FastMCP resources
    fastmcp_resources = set(re.findall(r'@mcp\.resource\([\"\']([^\"\']+)[\"\']', content))
    
    # Extract stdio server resources
    stdio_resources = set(re.findall(r'Resource\(\s*uri=[\"\']([^\"\']+)[\"\']', content))
    
    # Extract FastMCP prompts
    fastmcp_prompts = set()
    for match in re.finditer(r'@mcp\.prompt\(\)', content):
        start = match.end()
        next_lines = content[start:start+500]
        if content[max(0, match.start()-100):match.start()].strip().endswith('#'):
            continue
        func_match = re.search(r'def\s+(\w+)\(', next_lines)
        if func_match:
            fastmcp_prompts.add(func_match.group(1))
    
    # Extract stdio server prompts
    stdio_prompts = set(re.findall(r'Prompt\(\s*name=[\"\'](\w+)[\"\']', content))
    
    # Compare
    issues = []
    
    # Tools
    missing_tools = fastmcp_tools - stdio_tools
    extra_tools = stdio_tools - fastmcp_tools - {'server_status'}  # server_status is stdio-only
    
    if missing_tools:
        issues.append(f"⚠ Tools in FastMCP but not in stdio: {sorted(missing_tools)}")
    if extra_tools:
        issues.append(f"⚠ Tools in stdio but not in FastMCP: {sorted(extra_tools)}")
    
    # Resources
    missing_resources = fastmcp_resources - stdio_resources
    extra_resources = stdio_resources - fastmcp_resources
    
    if missing_resources:
        issues.append(f"⚠ Resources in FastMCP but not in stdio: {sorted(missing_resources)}")
    if extra_resources:
        issues.append(f"⚠ Resources in stdio but not in FastMCP: {sorted(extra_resources)}")
    
    # Prompts
    missing_prompts = fastmcp_prompts - stdio_prompts
    extra_prompts = stdio_prompts - fastmcp_prompts
    
    if missing_prompts:
        issues.append(f"⚠ Prompts in FastMCP but not in stdio: {sorted(missing_prompts)}")
    if extra_prompts:
        issues.append(f"⚠ Prompts in stdio but not in FastMCP: {sorted(extra_prompts)}")
    
    # Report
    if issues:
        print("❌ Sync issues found:\n")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("✅ All MCP features are in sync!")
        print(f"  Tools: {len(fastmcp_tools)} FastMCP, {len(stdio_tools)} stdio")
        print(f"  Resources: {len(fastmcp_resources)} FastMCP, {len(stdio_resources)} stdio")
        print(f"  Prompts: {len(fastmcp_prompts)} FastMCP, {len(stdio_prompts)} stdio")
        return True

if __name__ == "__main__":
    import sys
    success = verify_sync()
    sys.exit(0 if success else 1)
```

---

## Common Patterns

### Async Tools

If your tool is async:

```python
# FastMCP
@mcp.tool()
async def my_async_tool(param: str) -> str:
    result = await some_async_operation(param)
    return json.dumps(result, indent=2)

# Stdio handler
elif name == "my_async_tool":
    from .tools.my_module import my_async_tool as _my_async_tool
    result = await _my_async_tool(arguments.get("param", ""))
    if not isinstance(result, str):
        result = json.dumps(result, indent=2)
```

### Tools with Context

Some tools need `ctx` parameter (FastMCP only):

```python
@mcp.tool()
async def my_tool_with_context(
    param: str,
    ctx: Any = None,  # FastMCP provides this automatically
) -> str:
    # ctx is available in FastMCP, not in stdio
    if ctx:
        # Use ctx for notifications, etc.
        pass
    return json.dumps({"result": "..."}, indent=2)
```

**Note**: `ctx` is not available in stdio server, so handle gracefully.

### Consolidated Tools

Some tools use action-based consolidation:

```python
@mcp.tool()
def consolidated_tool(
    action: str = "default",
    param1: Optional[str] = None,
    param2: Optional[int] = None,
) -> str:
    """[HINT: Consolidated tool. action=default|other. Description.]"""
    if action == "default":
        from .tools.module1 import default_action
        return default_action(param1, param2)
    elif action == "other":
        from .tools.module2 import other_action
        return other_action(param1, param2)
```

**Stdio registration**: Same as regular tool, but include `action` enum in `inputSchema`.

---

## Known Differences

Some features may appear as "missing" in verification but are actually handled correctly:

1. **Parameterized Resources**: Resources with `{param}` in URI (e.g., `automation://memories/category/{category}`) are handled via pattern matching in stdio server's `read_resource()`, not listed in `list_resources()`. This is expected.

2. **Legacy Prompts**: Some prompts may exist in stdio server but not FastMCP if they're being phased out or migrated. Check if they're still needed.

## Troubleshooting

### Tool Not Appearing in Cursor

1. **Check both registrations**: Ensure tool is in both FastMCP and stdio server
2. **Verify handler**: Check `call_tool()` handler exists for stdio server
3. **Check return type**: Must return `str` (JSON string)
4. **Reload Cursor**: Full restart (not just reload) may be needed

### Resource Not Accessible

1. **Check URI format**: Must match exactly between FastMCP and stdio
2. **Verify handler**: Check `read_resource()` handler exists
3. **Check MIME type**: Should be `application/json` for JSON resources

### Prompt Not Showing

1. **Check both registrations**: Ensure prompt is in both systems
2. **Verify arguments**: Check `PromptArgument` definitions match function signature
3. **Check return type**: Must return `list[PromptMessage]`

---

## Maintenance

### Before Committing

1. Run verification script: `uv run python scripts/verify_mcp_sync.py`
2. Test in both modes (if possible):
   - FastMCP mode (default)
   - Stdio mode (`EXARP_FORCE_STDIO=1`)
3. Check for duplicates: Ensure no tool/resource/prompt is registered twice

### When Adding Features

1. **Add to FastMCP first** (primary system)
2. **Copy to stdio server** (use this guide)
3. **Add handler** (if needed for stdio)
4. **Verify sync** (run script)
5. **Test both modes** (if possible)

### When Removing Features

1. **Remove from FastMCP** (decorator)
2. **Remove from stdio server** (manual list)
3. **Remove handler** (if exists)
4. **Verify sync** (run script)

---

## File Locations Reference

| Feature Type | FastMCP Location | Stdio Server Location |
|-------------|------------------|----------------------|
| Tools | `server.py` ~line 743+ (inside `if mcp:`) | `server.py` ~line 790+ (`list_tools()`) |
| Tool Handlers | N/A (auto-handled) | `server.py` ~line 1271+ (`call_tool()`) |
| Resources | `server.py` ~line 3217+ (inside `if mcp:`) | `server.py` ~line 4150+ (`list_resources()`) |
| Resource Handlers | N/A (auto-handled) | `server.py` ~line 4179+ (`read_resource()`) |
| Prompts | `server.py` ~line 2792+ (inside `if mcp:`) | `server.py` ~line 4100+ (`list_prompts()`) |
| Prompt Handlers | N/A (auto-handled) | `server.py` ~line 4120+ (`get_prompt()`) |

---

## Examples

See existing implementations in `project_management_automation/server.py`:

- **Tool example**: `improve_task_clarity` (line ~2630 FastMCP, ~1389 stdio)
- **Resource example**: `automation://tools` (line ~3227 FastMCP, ~4154 stdio)
- **Prompt example**: `start_day` (line ~2792 FastMCP, ~4100 stdio)

---

## Questions?

- Check existing implementations in `server.py`
- Run verification script to find sync issues
- Review this guide for patterns
- See [FastMCP-Only Features](FASTMCP_ONLY_FEATURES.md) for features that don't need stdio equivalents
- Ask team for help if stuck

---

**Remember**: When in doubt, register in BOTH systems. It's better to have duplicates than missing features!
