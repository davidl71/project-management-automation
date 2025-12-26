# FastMCP Return Type Fix - Based on Examples

**Date**: 2025-12-26  
**Discovery**: FastMCP examples return Python objects, NOT JSON strings!

## Key Finding

**FastMCP 2.x examples return:**
- ✅ Plain Python types: `str`, `int`, `float`
- ✅ Python dicts/TypedDicts: `PostResult`, `FollowResult`
- ✅ Pydantic models: `File`, custom models
- ✅ `ToolResult` objects: For advanced cases
- ❌ **NOT JSON strings!**

## Our Current Pattern (WRONG?)

```python
@mcp.tool()
def session(...) -> str:
    result = _session(...)  # Returns JSON string
    return result  # Returns JSON string to FastMCP
```

## FastMCP Example Pattern (CORRECT)

```python
@mcp.tool()
def post(...) -> PostResult:  # TypedDict
    return _atproto.create_post(...)  # Returns dict, FastMCP serializes
```

## Hypothesis

**FastMCP expects Python objects and handles serialization internally.**

When we return JSON strings:
1. FastMCP might detect it's JSON
2. Try to parse it back to dict
3. Then try to serialize it again
4. This double-processing causes the "await dict" error

## Proposed Fix

**Change tools to return Python dicts instead of JSON strings:**

```python
@mcp.tool()
def session(...) -> dict:  # Change return type
    result_str = _session(...)  # Get JSON string from underlying function
    result_dict = json.loads(result_str)  # Parse to dict
    return result_dict  # Return dict, let FastMCP serialize
```

Or better yet, change underlying functions to return dicts directly!

## Next Steps

1. Test returning dicts instead of JSON strings
2. Update `@ensure_json_string` decorator to convert JSON strings to dicts
3. Or modify underlying functions to return dicts directly

