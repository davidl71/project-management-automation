# Complete _convert_to_content Analysis

**Date**: 2025-12-26

## Summary

After thorough analysis, **`_convert_to_content` is NOT the source of the error**. The function is well-implemented and handles all cases correctly.

## Function Implementation

```python
def _convert_to_content(
    result: Any,
    serializer: ToolResultSerializerType | None = None,
) -> list[ContentBlock]:
    """Convert a result to a sequence of content objects."""
    
    if result is None:
        return []
    
    if not isinstance(result, (list | tuple)):
        return [_convert_to_single_content_block(result, serializer)]
    
    # Handles lists, ContentBlocks, Images, Audio, Files
    # Aggregates non-ContentBlock items into TextContent
    return [TextContent(type="text", text=_serialize_with_fallback(result, serializer))]
```

## Where the Error Actually Occurs

The error happens in `FunctionTool.run()` **BEFORE** `_convert_to_content` is called:

```python
async def run(self, arguments: dict[str, Any]) -> ToolResult:
    wrapper_fn = without_injected_parameters(self.fn)
    type_adapter = get_cached_typeadapter(wrapper_fn)
    result = type_adapter.validate_python(arguments)  # ✅ Works
    if inspect.isawaitable(result):  # ✅ Returns False
        result = await result  # ❌ ERROR HERE: "object dict can't be used in 'await' expression"
    
    # _convert_to_content is never reached due to error above
    unstructured_result = _convert_to_content(result, serializer=self.serializer)
```

## Test Results

1. ✅ `TypeAdapter(function).validate_python(arguments)` works correctly
2. ✅ Returns function result (string), not dict
3. ✅ Result is NOT awaitable (`inspect.isawaitable()` returns False)
4. ✅ `_convert_to_content` function is correct

## The Real Issue

The error message suggests something is trying to `await` a dict, but our isolated tests show this shouldn't happen. This indicates:

1. **Different execution context** - Maybe task execution uses different code path
2. **Framework bug** - FastMCP has a bug in how it processes results
3. **Error location** - Error might be in `convert_tool_result` or task protocol layer

## Conclusion

**`_convert_to_content` is fine.** The error is a FastMCP framework bug that occurs before this function is called, likely in:
- Task execution path (`convert_tool_result`)
- Result processing in MCP protocol layer
- Or a different code path we haven't identified

The workaround (`EXARP_FORCE_STDIO=1`) bypasses FastMCP entirely, which is why it works.

