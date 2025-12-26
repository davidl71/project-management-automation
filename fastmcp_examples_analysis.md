# FastMCP 2.x Examples Analysis

**Date**: 2025-12-26  
**Goal**: Understand how FastMCP 2.x examples handle return types

## Key Findings

### Return Type Patterns in FastMCP Examples

1. **Simple Python Types** ✅
   ```python
   @mcp.tool()
   def greet(name: str) -> str:
       return f"Hello, {name}!"
   ```
   - Returns: Plain `str`
   - Works: ✅

2. **TypedDict/Pydantic Models** ✅
   ```python
   @mcp.tool()
   def post(text: str) -> PostResult:  # PostResult is TypedDict
       return _atproto.create_post(...)  # Returns dict
   ```
   - Returns: TypedDict/dict
   - Works: ✅

3. **ToolResult Objects** ✅
   ```python
   @mcp.tool()
   def echo(text: str) -> ToolResult:
       return ToolResult(
           content=f"Echoed: {text}",
           structured_content=result,
           meta={...}
       )
   ```
   - Returns: `ToolResult` object
   - Works: ✅

4. **JSON Strings** ❓
   - **NOT FOUND in examples** - No examples return JSON strings
   - Our code returns: JSON strings
   - **This might be the issue!**

## Critical Discovery

**FastMCP examples do NOT return JSON strings!**

They return:
- Plain Python types (`str`, `int`, `float`)
- Python dicts/TypedDicts
- Pydantic models
- `ToolResult` objects

**FastMCP handles serialization internally** - it expects Python objects, not pre-serialized JSON strings.

## Our Code vs Examples

### Our Pattern (Current)
```python
@mcp.tool()
def session(...) -> str:
    result = _session(...)  # Returns JSON string
    return result  # Returns JSON string
```

### FastMCP Example Pattern
```python
@mcp.tool()
def post(...) -> PostResult:  # TypedDict
    return _atproto.create_post(...)  # Returns dict
```

## Hypothesis

**The bug might be caused by returning JSON strings instead of Python dicts!**

FastMCP expects Python objects and serializes them internally. When we return JSON strings:
1. FastMCP might try to parse them back to dicts
2. Then try to serialize them again
3. This double-processing might cause the "await dict" error

## Recommendation

**Test returning Python dicts instead of JSON strings:**

```python
@mcp.tool()
def session(...) -> dict:
    result_str = _session(...)  # Get JSON string
    result_dict = json.loads(result_str)  # Parse to dict
    return result_dict  # Return dict, let FastMCP serialize
```

This matches the FastMCP example pattern!

