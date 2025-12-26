# Cache Analysis - Final Findings

**Date**: 2025-12-26  
**Hypothesis**: Caching issue causing "await dict" error

## Cache Implementation

FastMCP uses `@lru_cache(maxsize=5000)` on `get_cached_typeadapter`:

```python
@lru_cache(maxsize=5000)
def get_cached_typeadapter(cls: T) -> TypeAdapter[T]:
    # Creates TypeAdapter from function/class
    # Cache key: function object identity (id(function))
```

## Key Findings

1. **Cache can be cleared** - `get_cached_typeadapter.cache_clear()` works
2. **Cache was empty** - Clearing didn't help (cache size was 0)
3. **Cache is repopulated on first use** - New entries created when tools are called
4. **Function identity matters** - Cache key is based on function object `id()`

## Potential Cache Issues

### 1. Function Identity Changes

When functions are wrapped with decorators:
- Original function: `id(func1)`
- Wrapped function: `id(wrapper)` ≠ `id(func1)`
- `without_injected_parameters(wrapper)`: Might create yet another function

**Result**: Different cache entries for same logical function

### 2. Annotation Processing

`get_cached_typeadapter` processes annotations:
- Resolves forward references
- Converts `Annotated[Type, "string"]` to `Annotated[Type, Field(...)]`
- **Creates NEW function** if annotations change

**Result**: Modified function cached, but might not match actual execution

### 3. Cache Key Collision

If two different functions have same identity (unlikely but possible):
- Cache hit returns wrong TypeAdapter
- TypeAdapter expects different signature

## Test Results

- ✅ `TypeAdapter(function).validate_python()` works correctly in isolation
- ✅ Cache clearing works
- ❌ Clearing cache doesn't fix the issue
- ⚠️ Cache monitoring didn't show activity (monkey-patch didn't work)

## Conclusion

**Cache is likely NOT the issue**, but there might be:
1. **Stale cache entries** from before fixes (but cache was empty)
2. **Incorrect cache keying** due to function wrapping
3. **TypeAdapter internal state** cached incorrectly

## Next Steps

1. Test with cache completely disabled (if possible)
2. Check if `without_injected_parameters` creates functions that affect cache
3. Monitor cache during actual tool execution (need different approach)
4. Check if Pydantic's TypeAdapter has internal caching issues

