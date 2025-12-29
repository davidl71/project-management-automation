# FastMCP String Return Type Deep Analysis

## 🔍 Key Discovery

**Official FastMCP examples return plain strings, not JSON strings!**

### Official Example (from FastMCP docs):
```python
@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"  # ← Plain string, NOT JSON
```

**This is different from our implementation which returns JSON strings.**

## Our Current Pattern

```python
@mcp.tool()
def context(...) -> str:
    result = _context(...)  # Returns JSON string
    if isinstance(result, str):
        return result  # ← JSON string
    else:
        return json.dumps(result, indent=2)  # ← Convert dict to JSON
```

## Working Resource Example

```python
@mcp.resource("automation://status")
def get_automation_status() -> str:
    return json.dumps({
        "status": "ok",
        "version": __version__
    }, indent=2)  # ← Always returns JSON string
```

**This works because it ALWAYS returns a string, never a dict.**

## Critical Insight

**FastMCP can handle BOTH:**
1. ✅ Plain strings: `"Hello"` → FastMCP converts to PromptMessage
2. ✅ JSON strings: `'{"status": "ok"}'` → FastMCP uses as-is
3. ❌ Dicts: `{"status": "ok"}` → **CAUSES "dict can't be awaited" ERROR**

## Root Cause Hypothesis

The "dict can't be awaited" error occurs when:

1. **Runtime dict return**: Function actually returns `dict` at runtime (despite `-> str` annotation)
2. **Exception path**: Exception handler returns dict before defensive check
3. **FastMCP static analysis**: FastMCP analyzes function body and detects potential dict return paths

## The Problem with Our Current Tools

**All 29 tools have defensive checks INSIDE the function:**
```python
@mcp.tool()
def context(...) -> str:
    result = _context(...)  # ← Could return dict if _context is None or fails
    if isinstance(result, str):  # ← Defensive check
        return result
    else:
        return json.dumps(result, indent=2)
```

**But FastMCP might be analyzing the function BEFORE it runs:**
- Sees `result = _context(...)` 
- Doesn't know if `_context` returns str or dict
- Tries to await the result (if it looks like a coroutine)
- Fails with "dict can't be awaited"

## Solution: Decorator Pattern

**Use `@ensure_json_string` decorator to wrap the function BEFORE FastMCP sees it:**

```python
@ensure_json_string  # ← Wraps function, ensures str return
@mcp.tool()
def context(...) -> str:
    result = _context(...)
    if isinstance(result, str):
        return result
    else:
        return json.dumps(result, indent=2)
```

**The decorator ensures FastMCP only sees a function that ALWAYS returns str.**

## Why Decorator Works

1. **Function wrapping**: Decorator wraps the original function
2. **Type guarantee**: Wrapped function ALWAYS returns str (never dict)
3. **FastMCP sees wrapped version**: FastMCP analyzes the wrapped function, which has guaranteed str return
4. **Runtime safety**: Even if underlying function returns dict, decorator converts it

## Current Status

- ❌ **0 of 29 tools** use `@ensure_json_string` decorator
- ✅ **All 29 tools** have defensive checks inside function body
- ⚠️ **FastMCP static analysis** might still see potential dict returns

## Recommendation

**Add `@ensure_json_string` decorator to ALL 29 tools** to ensure FastMCP only sees functions with guaranteed str returns.

