# Any Type Analysis

**Date**: 2025-12-26  
**Hypothesis**: `dict[str, Any]` or `Any` return types cause FastMCP to fail

## Discovery

Found that `memory_maint` has `-> dict[str, Any]` return type annotation in `consolidated.py`:
```python
def memory_maint(...) -> dict[str, Any]:
```

But in `server.py`, it's wrapped with `@ensure_json_string` and has `-> str`:
```python
@ensure_json_string
@mcp.tool()
def memory_maint(...) -> str:
```

## Key Question

**Does FastMCP analyze the underlying function's return type annotation, or just the wrapper?**

If FastMCP analyzes the underlying function:
- `memory_maint` would be broken (has `dict[str, Any]`)
- But it's reported as **working**!

If FastMCP only analyzes the wrapper:
- All tools should work (all wrappers have `-> str`)
- But many are broken!

## Test Results

Testing to see if changing `memory_maint` from `-> dict[str, Any]` to `-> str` in consolidated.py affects behavior.

## Conclusion

If `memory_maint` works with `-> dict[str, Any]` in the underlying function, then:
- Return type annotations in underlying functions are NOT the issue
- The problem must be elsewhere (dict returns in code, not annotations)

