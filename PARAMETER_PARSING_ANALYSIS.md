# Parameter Parsing Analysis

**Date**: 2025-12-26  
**Hypothesis**: FastMCP parameter parsing might be causing the "await dict" error

## Findings

### Parameter Type Comparison

**Working Tools (7):**
- ✅ No `list[str]` parameters
- ✅ Only simple types: `str`, `bool`, `int`, `Optional[str]`
- ✅ Average: 14.7 parameters per tool

**Broken Tools (20):**
- ❌ Some have `Optional[list[str]]` parameters (e.g., `automation`)
- ❌ But most don't have list parameters either
- ✅ Average: 9.3 parameters per tool

### Key Discovery

The `automation` tool has `Optional[list[str]]` parameters:
- `tasks: Optional[list[str]] = None`
- `tag_filter: Optional[list[str]] = None`

But testing shows:
- ❌ Fails with empty args `{}`
- ❌ Fails with `None` values
- ❌ Fails with empty lists `[]`
- ❌ Fails with actual lists `["task1", "task2"]`

**Conclusion**: Parameter types are NOT the issue - all parameter combinations fail the same way.

### Schema Generation

FastMCP correctly generates JSON schemas for `Optional[list[str]]`:
```json
{
  "anyOf": [
    {
      "items": {"type": "string"},
      "type": "array"
    },
    {
      "type": "null"
    }
  ]
}
```

This is correct and shouldn't cause issues.

## Real Issue

The error occurs **during function execution**, not parameter parsing:

1. FastMCP receives parameters correctly
2. FastMCP calls the function
3. Function returns JSON string
4. **FastMCP tries to process/validate the return value**
5. **ERROR OCCURS HERE** - FastMCP detects a dict somewhere

## Hypothesis

FastMCP might be:
1. **Inspecting the return value** before our decorator processes it
2. **Trying to validate** the return against a schema
3. **Attempting to serialize** an already-serialized JSON string
4. **Detecting dict types** in intermediate function calls during execution

## Next Steps

1. Check how FastMCP processes return values in `tool.py`
2. Look for return value validation/serialization code
3. Check if FastMCP is doing runtime type checking on return values
4. Investigate if `@ensure_json_string` decorator order matters

