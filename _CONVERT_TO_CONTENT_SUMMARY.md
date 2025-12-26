# _convert_to_content Analysis Summary

**Date**: 2025-12-26

## Key Finding

**`_convert_to_content` is NOT the problem.** The error occurs **before** this function is called.

## Code Flow in `FunctionTool.run()`

```python
async def run(self, arguments: dict[str, Any]) -> ToolResult:
    wrapper_fn = without_injected_parameters(self.fn)
    type_adapter = get_cached_typeadapter(wrapper_fn)
    result = type_adapter.validate_python(arguments)  # ✅ Works correctly
    if inspect.isawaitable(result):  # ✅ Returns False for our tools
        result = await result  # ❌ ERROR: "object dict can't be used in 'await' expression"
    
    # _convert_to_content is called AFTER the error
    unstructured_result = _convert_to_content(result, serializer=self.serializer)
```

## Test Results

1. ✅ `TypeAdapter(function).validate_python(arguments)` works correctly
   - Calls the function
   - Returns function result (string)
   - Result is NOT awaitable

2. ✅ `inspect.isawaitable(dict)` returns `False`
   - Dicts are correctly identified as non-awaitable

3. ✅ `_convert_to_content` function is straightforward
   - Handles None, single values, lists correctly
   - Uses `_serialize_with_fallback` for serialization

## The Mystery

The error "object dict can't be used in 'await' expression" suggests:
- Something is trying to `await` a dict
- But our isolated tests show this shouldn't happen
- The error must be in a different code path or context

## Possible Locations

1. **`convert_tool_result` in tasks/protocol.py** (line 236)
   - Called with `await convert_tool_result(...)`
   - Might be processing tool results incorrectly

2. **Task execution path**
   - If tools are executed as tasks, different code path
   - Might have different error handling

3. **MCP protocol layer**
   - Error might be in how FastMCP communicates with MCP client
   - Might be in result serialization/deserialization

## Conclusion

The `_convert_to_content` function itself is fine. The error is likely in:
- Task execution path (`convert_tool_result`)
- MCP protocol communication
- Or a different code path we haven't identified yet

The error message suggests FastMCP is trying to await something that's a dict, but our isolated tests show this shouldn't happen. This points to a bug in FastMCP's framework code.

