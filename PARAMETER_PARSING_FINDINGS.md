# Parameter Parsing Analysis - Final Findings

**Date**: 2025-12-26  
**Question**: "Might it be something in the way we parse parameters?"

## Summary

**Answer: NO - Parameter parsing is NOT the issue.**

## Investigation Results

### 1. Parameter Type Comparison

**Working Tools:**
- ✅ No `list[str]` parameters
- ✅ Simple types only: `str`, `bool`, `int`, `Optional[str]`

**Broken Tools:**
- ❌ Some have `Optional[list[str]]` (e.g., `automation`)
- ❌ But most don't have list parameters either
- ✅ Same simple types as working tools

### 2. Parameter Parsing Tests

Tested `automation` tool (has `Optional[list[str]]` params) with:
- Empty args `{}` → ❌ Fails
- `None` values → ❌ Fails  
- Empty lists `[]` → ❌ Fails
- Actual lists `["task1"]` → ❌ Fails

**Conclusion**: All parameter combinations fail the same way - parameter types are NOT the issue.

### 3. FastMCP Parameter Processing

FastMCP uses Pydantic's `TypeAdapter` to validate parameters:

```python
type_adapter = get_cached_typeadapter(wrapper_fn)
result = type_adapter.validate_python(arguments)
if inspect.isawaitable(result):
    result = await result
```

This correctly:
- ✅ Validates arguments against function signature
- ✅ Generates proper JSON schemas for `Optional[list[str]]`
- ✅ Handles all parameter types correctly

### 4. Schema Generation

FastMCP correctly generates schemas:
```json
{
  "anyOf": [
    {"items": {"type": "string"}, "type": "array"},
    {"type": "null"}
  ]
}
```

This is correct and shouldn't cause issues.

## Real Issue Location

The error occurs **AFTER parameter parsing**, during **function execution and return value processing**:

1. ✅ FastMCP receives and validates parameters correctly
2. ✅ FastMCP calls the function
3. ✅ Function returns JSON string
4. ❌ **FastMCP processes return value** → ERROR OCCURS HERE

## FastMCP Return Value Processing

From `fastmcp/tools/tool.py`:

```python
async def run(self, arguments: dict[str, Any]) -> ToolResult:
    # ... validate arguments ...
    result = type_adapter.validate_python(arguments)  # Validates args
    if inspect.isawaitable(result):
        result = await result  # Calls function if async
    
    # Process return value
    unstructured_result = _convert_to_content(result, serializer=self.serializer)
    
    # Try to serialize as dict
    try:
        structured_content = pydantic_core.to_jsonable_python(result)
        if isinstance(structured_content, dict):
            return ToolResult(
                content=unstructured_result,
                structured_content=structured_content,
            )
```

**The issue**: FastMCP is trying to process the return value, and somewhere in this process it's detecting a dict and trying to await it.

## Conclusion

**Parameter parsing is working correctly.** The issue is in:
1. **Return value processing** - FastMCP's `_convert_to_content` or serialization
2. **Static analysis** - FastMCP detecting dict types in function call chains
3. **TypeAdapter behavior** - Something about how it processes the function signature

## Next Steps

1. Investigate `_convert_to_content` function
2. Check if FastMCP is doing static analysis on return types
3. Test if changing return type annotation affects the error
4. Check FastMCP's handling of JSON strings vs dicts

