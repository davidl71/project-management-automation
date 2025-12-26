# Patching inspect.isawaitable() Analysis

**Date**: 2025-12-26  
**Question**: Can we hack `inspect.isawaitable` to always return `False`?

## Attempt 1: Patch Before FastMCP Import

**Result**: ❌ Failed - Error still occurs

**Analysis**: FastMCP imports `inspect` at module level (line 3 of `tool.py`), so it gets its own reference. Even patching before FastMCP import didn't work.

## Attempt 2: Patch in FastMCP's Namespace

**Result**: ❌ Failed - Error still occurs

**Analysis**: FastMCP might not expose `inspect` in its namespace, or it's using a cached reference.

## Key Finding

**The patch didn't work**, which suggests:

1. **FastMCP might not be using `inspect.isawaitable()`** - Maybe it has its own check
2. **FastMCP might be checking something else** - Function signature, return type annotation, etc.
3. **The error occurs before the check** - Maybe FastMCP always tries to await regardless

## FastMCP's Code

From `fastmcp/tools/tool.py`:
```python
import inspect  # Line 3 - module level import

async def run(self, arguments: dict[str, Any]) -> ToolResult:
    wrapper_fn = without_injected_parameters(self.fn)
    type_adapter = get_cached_typeadapter(wrapper_fn)
    result = type_adapter.validate_python(arguments)
    if inspect.isawaitable(result):  # ← Uses inspect.isawaitable
        result = await result       # ← Tries to await
```

## Conclusion

**Patching `inspect.isawaitable()` doesn't fix the issue**, which means:

1. FastMCP might be using a different check
2. FastMCP might have a bug where it always tries to await
3. The error might be coming from somewhere else entirely

**The workaround `EXARP_FORCE_STDIO=1` remains the only solution.**

