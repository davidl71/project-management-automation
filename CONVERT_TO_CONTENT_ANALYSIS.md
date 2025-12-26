# _convert_to_content Function Analysis

**Date**: 2025-12-26  
**Focus**: Understanding how FastMCP processes tool return values

## Key Discovery

Looking at the `run` method in `FunctionTool`:

```python
async def run(self, arguments: dict[str, Any]) -> ToolResult:
    """Run the tool with arguments."""
    wrapper_fn = without_injected_parameters(self.fn)
    type_adapter = get_cached_typeadapter(wrapper_fn)
    result = type_adapter.validate_python(arguments)  # ⚠️ THIS LINE!
    if inspect.isawaitable(result):
        result = await result  # ⚠️ ERROR HAPPENS HERE!
    
    if isinstance(result, ToolResult):
        return result
    
    unstructured_result = _convert_to_content(result, serializer=self.serializer)
    # ... rest of processing
```

## The Problem

**Line 388: `result = type_adapter.validate_python(arguments)`**

This line is calling `validate_python` on the **arguments dict**, but `type_adapter` was created from the **function itself** (`get_cached_typeadapter(wrapper_fn)`).

When you create a `TypeAdapter` from a function:
- It validates the arguments against the function signature
- **It then calls the function with those arguments**
- Returns the function's return value

So `type_adapter.validate_python(arguments)` should:
1. Validate `arguments` dict against function parameters
2. Call the function: `wrapper_fn(**arguments)`
3. Return the function result

## The Error Location

The error "object dict can't be used in 'await' expression" happens at:

```python
if inspect.isawaitable(result):
    result = await result  # ❌ ERROR: result is a dict, not awaitable
```

This suggests that `type_adapter.validate_python(arguments)` is returning a **dict** instead of calling the function, OR the function is returning a dict that FastMCP thinks is awaitable.

## _convert_to_content Function

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
    
    # ... handles lists, ContentBlocks, etc.
```

This function is called **AFTER** the error occurs, so it's not the source of the problem.

## Hypothesis

The issue is in `type_adapter.validate_python(arguments)`:

1. **TypeAdapter from function** - When created from a function, it should validate args and call the function
2. **But something goes wrong** - It might be returning a dict (the validated arguments?) instead of calling the function
3. **FastMCP tries to await it** - `inspect.isawaitable(result)` might incorrectly return True for a dict, OR the result is somehow marked as awaitable

## Next Steps

1. Test what `TypeAdapter(function).validate_python(arguments)` actually returns
2. Check if `inspect.isawaitable()` incorrectly identifies dicts as awaitable
3. Investigate `get_cached_typeadapter` to see how it processes functions
4. Check if there's a bug in Pydantic's TypeAdapter when used with functions

