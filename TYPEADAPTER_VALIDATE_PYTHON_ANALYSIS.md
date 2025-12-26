# TypeAdapter.validate_python() Analysis

**Date**: 2025-12-26  
**Key Discovery**: `TypeAdapter.validate_python()` on a function **CALLS the function**!

## How TypeAdapter Works with Functions

When you create a `TypeAdapter` from a function:
```python
adapter = TypeAdapter(my_func)
result = adapter.validate_python(arguments)
```

**`validate_python()` actually CALLS the function** with the provided arguments and returns the function's result!

## FastMCP's Execution Flow

```python
async def run(self, arguments: dict[str, Any]) -> ToolResult:
    wrapper_fn = without_injected_parameters(self.fn)
    type_adapter = get_cached_typeadapter(wrapper_fn)  # TypeAdapter from function
    result = type_adapter.validate_python(arguments)    # ← CALLS the function!
    if inspect.isawaitable(result):                     # ← Checks result
        result = await result                           # ← Tries to await
```

## The Mystery Deepens

1. ✅ `TypeAdapter.validate_python()` calls the function
2. ✅ Function returns a dict (or string)
3. ✅ `inspect.isawaitable(dict)` returns `False` (we tested this)
4. ❌ But FastMCP still tries to await it!

## Possible Explanations

### 1. FastMCP Checks Before Function Execution
Maybe FastMCP checks `isawaitable()` on the function itself, not the result?

### 2. Result is Wrapped
Maybe FastMCP wraps the result in something that makes it appear awaitable?

### 3. TypeAdapter Returns Something Special
Maybe `TypeAdapter.validate_python()` on a function returns something other than the function's result?

### 4. FastMCP Bug
Maybe FastMCP has a bug where it always tries to await, regardless of `isawaitable()`?

## Test Results

- ✅ `TypeAdapter(func_str).validate_python({})` → `str`, `isawaitable: False`
- ✅ `TypeAdapter(func_dict).validate_python({})` → `dict`, `isawaitable: False`
- ✅ Normal dicts are NOT awaitable

## Conclusion

The error "object dict can't be used in 'await' expression" suggests FastMCP is trying to await a dict, but `inspect.isawaitable(dict)` correctly returns `False`. This means:

**Either:**
1. FastMCP is not using `inspect.isawaitable()` correctly
2. FastMCP is checking something else
3. FastMCP has a bug where it always tries to await

The fact that even the simplest tools fail suggests this is a fundamental bug in FastMCP's result processing logic.

