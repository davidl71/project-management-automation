# FastMCP Return Type Requirements

**Date**: 2025-12-01  
**Status**: ✅ Enforced  
**Priority**: 🚨 CRITICAL

---

## Overview

All MCP tools and resources **MUST** return JSON strings, never dicts. This prevents FastMCP errors like "object dict can't be used in 'await' expression".

---

## 🚨 CRITICAL Rules

### Tools (`@mcp.tool()`)

**MUST return `str` (JSON string), NEVER `dict`**

```python
@mcp.tool()
def my_tool(...) -> str:  # ✅ str, not dict
    """Tool description."""
    try:
        result = some_function()
        # Ensure we always return a JSON string
        if isinstance(result, str):
            return result
        elif isinstance(result, dict):
            return json.dumps(result, indent=2)
        else:
            return json.dumps({"result": str(result)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
```

### Resources (`@mcp.resource()`)

**MUST return `str` (JSON string), NEVER `dict`**

```python
@mcp.resource("automation://my-resource")
def my_resource(...) -> str:  # ✅ str, not dict
    """Resource description."""
    result = get_data()
    if isinstance(result, dict):
        return json.dumps(result, indent=2)
    return json.dumps({"result": str(result)}, indent=2)
```

### Prompts (`@mcp.prompt()`)

**Already correct** - Prompts return template strings (already `str`)

---

## Defensive Pattern (Recommended)

Always use this pattern to ensure type safety:

```python
def ensure_json_string(result: Any) -> str:
    """Ensure result is always a JSON string."""
    if isinstance(result, str):
        # Already a string, verify it's valid JSON
        try:
            json.loads(result)  # Validate
            return result
        except json.JSONDecodeError:
            # Not valid JSON, wrap it
            return json.dumps({"content": result}, indent=2)
    elif isinstance(result, dict):
        return json.dumps(result, indent=2)
    else:
        return json.dumps({"result": str(result)}, indent=2)
```

---

## Common Mistakes

### ❌ Wrong: Returning dict directly

```python
@mcp.tool()
def bad_tool() -> dict:  # ❌ WRONG
    return {"success": True, "data": {...}}
```

### ❌ Wrong: Union return type

```python
@mcp.tool()
def bad_tool() -> dict | str:  # ❌ WRONG
    if condition:
        return {"data": "..."}  # Returns dict
    return json.dumps({...})  # Returns str
```

### ✅ Correct: Always return str

```python
@mcp.tool()
def good_tool() -> str:  # ✅ CORRECT
    result = {"success": True, "data": {...}}
    return json.dumps(result, indent=2)
```

---

## Files Fixed

1. **Tools:**
   - `project_management_automation/tools/auto_primer.py` - `auto_prime_session`, `get_task_context`
   - `project_management_automation/tools/consolidated.py` - `recommend`, `task_discovery`

2. **Resources:**
   - `project_management_automation/resources/templates.py` - 8 resources fixed

3. **Server Wrappers:**
   - `project_management_automation/server.py` - Added defensive coding to tool wrappers

---

## Testing

When creating new tools/resources:

1. ✅ Verify return type annotation is `-> str`
2. ✅ Test that function returns JSON string
3. ✅ Add defensive type checking
4. ✅ Test error cases return JSON strings

---

## Related Documentation

- `.cursorrules` - Updated with return type requirements
- `.cursor/rules/project-development.mdc` - Updated tool pattern
- `docs/FASTMCP_ERROR_INVESTIGATION_COMPLETE.md` - Error investigation

---

## Why This Matters

FastMCP expects all tool/resource functions to return strings. When a dict is returned:
- FastMCP tries to await it (causing "object dict can't be used in 'await' expression")
- Type checking fails
- MCP protocol violations occur

**Always return JSON strings to ensure compatibility.**

