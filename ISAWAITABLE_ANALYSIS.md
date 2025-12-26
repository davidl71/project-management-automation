# inspect.isawaitable() Analysis

**Date**: 2025-12-26  
**Question**: How does `inspect.isawaitable()` work and why might it return `True` for a dict?

## Python's inspect.isawaitable() Implementation

```python
def isawaitable(object):
    """Return true if object can be passed to an ``await`` expression."""
    return (isinstance(object, types.CoroutineType) or
            isinstance(object, types.GeneratorType) and
                bool(object.gi_code.co_flags & CO_ITERABLE_COROUTINE) or
            isinstance(object, collections.abc.Awaitable))
```

## Test Results

### Normal Types
- ✅ `dict` → `isawaitable: False` (correct)
- ✅ `str` → `isawaitable: False` (correct)
- ✅ `list` → `isawaitable: False` (correct)
- ✅ `int` → `isawaitable: False` (correct)

### Coroutines
- ✅ `coroutine` → `isawaitable: True` (correct)
- ✅ Has `__await__` method

### TypeAdapter Results
- ✅ `TypeAdapter(func_str).validate_python({})` → `str`, `isawaitable: False`
- ✅ `TypeAdapter(func_dict).validate_python({})` → `dict`, `isawaitable: False`

## Key Finding

**Normal dicts are NOT awaitable** - `inspect.isawaitable(dict)` correctly returns `False`.

## The Mystery

If `inspect.isawaitable()` correctly returns `False` for dicts, why does FastMCP try to await them?

### Possible Explanations

1. **FastMCP is checking something else** - Maybe it's checking the function itself, not the result
2. **TypeAdapter returns something unexpected** - Maybe `validate_python()` returns a wrapped object
3. **FastMCP has a bug in its check** - Maybe it's not using `inspect.isawaitable()` correctly
4. **The result is wrapped in something** - Maybe FastMCP wraps the result in a way that makes it appear awaitable

## FastMCP's Code

From `fastmcp/tools/tool.py`:
```python
async def run(self, arguments: dict[str, Any]) -> ToolResult:
    wrapper_fn = without_injected_parameters(self.fn)
    type_adapter = get_cached_typeadapter(wrapper_fn)
    result = type_adapter.validate_python(arguments)
    if inspect.isawaitable(result):  # ← This check
        result = await result  # ← This fails
```

## Hypothesis

The error message says "object dict can't be used in 'await' expression", which means:
1. `inspect.isawaitable(result)` returned `True` (incorrectly)
2. FastMCP tried to `await result`
3. Python raised the error because dicts can't be awaited

**But our tests show `inspect.isawaitable(dict)` returns `False`!**

This suggests:
- FastMCP might be checking something other than the result
- Or the result is wrapped/modified in a way that makes it appear awaitable
- Or there's a bug in FastMCP's usage of `inspect.isawaitable()`

## Next Steps

1. Check what `type_adapter.validate_python(arguments)` actually returns in FastMCP's context
2. Check if FastMCP modifies the result before checking `isawaitable()`
3. Check if there's a wrapper or proxy that makes dicts appear awaitable

