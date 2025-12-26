# inspect.isawaitable() Final Analysis

**Date**: 2025-12-26  
**Question**: How does `inspect.isawaitable()` work and why does FastMCP try to await dicts?

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
- ✅ `coroutine` → `isawaitable: True` (correct)

### TypeAdapter Behavior
- ✅ `TypeAdapter(sync_func).validate_python({})` → function result, `isawaitable: False`
- ✅ `TypeAdapter(async_func).validate_python({})` → coroutine, `isawaitable: True`

### Our Tools
- ✅ Our tools are sync functions → return dicts/strings → `isawaitable: False`
- ✅ `@ensure_json_string` doesn't make functions async
- ✅ `without_injected_parameters` doesn't make functions async

## The Mystery

**If `inspect.isawaitable(dict)` returns `False`, why does FastMCP try to await it?**

### Possible Explanations

1. **FastMCP checks something else** - Maybe it checks the function, not the result?
2. **FastMCP has a bug** - Maybe it always tries to await regardless of the check?
3. **Result is wrapped** - Maybe FastMCP wraps the result in something awaitable?
4. **Race condition** - Maybe the result changes between check and await?

## FastMCP's Code

```python
async def run(self, arguments: dict[str, Any]) -> ToolResult:
    wrapper_fn = without_injected_parameters(self.fn)
    type_adapter = get_cached_typeadapter(wrapper_fn)
    result = type_adapter.validate_python(arguments)  # Calls function, returns result
    if inspect.isawaitable(result):                   # Should be False for dict
        result = await result                         # Shouldn't execute for dict
```

## Conclusion

**`inspect.isawaitable()` works correctly** - it returns `False` for dicts.

**The bug must be in FastMCP's logic** - either:
1. FastMCP is not using `inspect.isawaitable()` correctly
2. FastMCP is checking something other than the result
3. FastMCP has a bug where it always tries to await

The fact that even the simplest tools fail suggests FastMCP has a fundamental bug in its result processing logic.

