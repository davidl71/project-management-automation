# Cache Issue Analysis

**Date**: 2025-12-26  
**Hypothesis**: Caching issue causing "await dict" error

## Cache Implementation

FastMCP uses `@lru_cache(maxsize=5000)` on `get_cached_typeadapter`:

```python
@lru_cache(maxsize=5000)
def get_cached_typeadapter(cls: T) -> TypeAdapter[T]:
    # Creates TypeAdapter from function/class
    # Caches based on function object identity
```

## Cache Key

The cache is keyed by **function object identity** (`id(function)`), which means:
- Same function object → same cache entry
- Wrapped function (from decorator) → different cache entry
- `without_injected_parameters()` → might create new function object

## Potential Issues

1. **Stale cache entries** - Old TypeAdapters cached before fixes
2. **Incorrect cache keying** - Wrapped functions get different cache entries
3. **TypeAdapter internal caching** - Pydantic's TypeAdapter might cache something incorrectly
4. **Function identity changes** - Decorators change function identity, causing cache misses

## Test Results

- ✅ Cache can be cleared with `get_cached_typeadapter.cache_clear()`
- ❌ Clearing cache doesn't fix the issue (cache was empty anyway)
- ⚠️ Cache might be repopulated incorrectly on first use

## Next Steps

1. Test if cache is populated incorrectly on first tool call
2. Check if `without_injected_parameters` affects function identity
3. Monitor cache during tool execution
4. Test with cache disabled (if possible)

