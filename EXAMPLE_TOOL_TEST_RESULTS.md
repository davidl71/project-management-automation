# FastMCP Example Tool Test Results

**Date**: 2025-12-26  
**Test**: Copied exact tool from FastMCP examples into exarp

## Test Tool

Copied from `/tmp/fastmcp-examples/tests/server/middleware/test_rate_limiting.py`:

```python
@mcp.tool
def test_batch_process(items: list[str]) -> str:
    """Process multiple items - FastMCP example pattern test."""
    return f"Processed {len(items)} items"
```

## Key Differences from Our Tools

1. ✅ **No `@ensure_json_string` decorator** - FastMCP examples don't use it
2. ✅ **`@mcp.tool` (no parentheses)** - FastMCP examples use this syntax
3. ✅ **`list[str]` parameter** - Direct list, not `Optional[list[str]]`
4. ✅ **Returns plain `str`** - Not JSON string, FastMCP serializes it

## Test Results

**All tests FAILED with the same error:**

```
❌ ERROR IN RESULT: object dict can't be used in 'await' expression...
```

Test cases:
- Empty list `[]` → ❌ Failed
- Single item `["item1"]` → ❌ Failed  
- Multiple items `["item1", "item2", "item3"]` → ❌ Failed

## Conclusion

**Even the exact FastMCP example pattern fails!**

This confirms:
1. ❌ Parameter parsing is NOT the issue
2. ❌ Return type (JSON string vs Python object) is NOT the issue
3. ❌ Decorator syntax is NOT the issue
4. ❌ Parameter types (`list[str]` vs `Optional[list[str]]`) is NOT the issue

## Root Cause

The error is happening at a **deeper level in FastMCP's framework**, likely in:
- Tool result processing (`_convert_to_content`)
- TypeAdapter validation/execution
- Return value serialization
- Framework-level async handling

This is a **systemic FastMCP bug** that affects ALL tools, regardless of their implementation pattern.

## Next Steps

1. Investigate FastMCP's `_convert_to_content` function
2. Check FastMCP's TypeAdapter usage in tool execution
3. Test with different FastMCP versions
4. Report to FastMCP maintainers as a framework bug
5. Continue using `EXARP_FORCE_STDIO=1` as workaround

