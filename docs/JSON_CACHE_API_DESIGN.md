# JSON Cache API Design

**Date**: 2025-12-21  
**Status**: Design Complete  
**Task**: Design JSON cache API and interface

---

## Overview

Unified JSON caching utility supporting:
- File modification time (mtime) invalidation
- TTL (time-to-live) expiration
- LRU eviction for cache size limits
- Decorator and context manager patterns
- Cache statistics and monitoring

---

## API Design

### Core Classes

#### `JsonFileCache`
Main caching class for file-based JSON caching.

```python
class JsonFileCache:
    """File-based JSON cache with mtime invalidation."""
    
    def __init__(
        self,
        file_path: Path,
        ttl: Optional[int] = None,
        max_size: Optional[int] = None,
        enable_stats: bool = True
    ):
        """
        Args:
            file_path: Path to JSON file to cache
            ttl: Time-to-live in seconds (None = no expiration)
            max_size: Maximum cache entries (None = unlimited)
            enable_stats: Enable statistics collection
        """
    
    def get(self) -> Optional[dict[str, Any]]:
        """Get cached data if valid, None if expired/missing."""
    
    def get_or_load(self) -> dict[str, Any]:
        """Get cached data or load from file."""
    
    def invalidate(self) -> None:
        """Manually invalidate cache."""
    
    def clear(self) -> None:
        """Clear all cache data."""
    
    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
```

#### `JsonCacheManager`
Global cache manager for multiple files.

```python
class JsonCacheManager:
    """Manages multiple JSON file caches."""
    
    _instance: Optional['JsonCacheManager'] = None
    _caches: dict[str, JsonFileCache]
    
    @classmethod
    def get_instance(cls) -> 'JsonCacheManager':
        """Get singleton instance."""
    
    def get_cache(
        self,
        file_path: Path,
        ttl: Optional[int] = None,
        max_size: Optional[int] = None
    ) -> JsonFileCache:
        """Get or create cache for file."""
    
    def invalidate_file(self, file_path: Path) -> None:
        """Invalidate cache for specific file."""
    
    def invalidate_all(self) -> None:
        """Invalidate all caches."""
    
    def get_all_stats(self) -> dict[str, dict[str, Any]]:
        """Get statistics for all caches."""
```

---

## Decorator Pattern

### Basic Usage

```python
from project_management_automation.utils.json_cache import json_file_cache

@json_file_cache(file_path=Path(".todo2/commits.json"), ttl=300)
def load_commits() -> list[dict]:
    """Load commits from file."""
    with open(".todo2/commits.json") as f:
        data = json.load(f)
        return data.get("commits", [])
```

### With Custom Configuration

```python
@json_file_cache(
    file_path=Path(".exarp/session_mode.json"),
    ttl=600,  # 10 minutes
    max_size=100,  # LRU eviction after 100 entries
    enable_stats=True
)
def load_session_mode() -> dict:
    """Load session mode data."""
    # Implementation...
```

### Function Signature

```python
def json_file_cache(
    file_path: Path,
    ttl: Optional[int] = None,
    max_size: Optional[int] = None,
    enable_stats: bool = True
) -> Callable:
    """
    Decorator for caching JSON file loads.
    
    Args:
        file_path: Path to JSON file
        ttl: Time-to-live in seconds (None = mtime only)
        max_size: Maximum cache size (None = unlimited)
        enable_stats: Enable statistics
    
    Returns:
        Decorated function with caching
    """
```

---

## Context Manager Pattern

### Basic Usage

```python
from project_management_automation.utils.json_cache import JsonFileCache

def load_data():
    cache = JsonFileCache(Path(".todo2/commits.json"), ttl=300)
    
    # Get cached or load
    data = cache.get_or_load()
    
    # Or check if cached
    if cache.get() is not None:
        data = cache.get()
    else:
        data = load_from_file()
        cache.set(data)  # If we had a set method
```

### With Automatic Loading

```python
from project_management_automation.utils.json_cache import json_file_cache_context

def load_data():
    with json_file_cache_context(Path(".todo2/commits.json")) as cache:
        data = cache.get_or_load()
        return data
```

---

## Configuration Options

### TTL (Time-To-Live)

```python
# No TTL - only mtime invalidation
cache = JsonFileCache(file_path, ttl=None)

# 5 minute TTL
cache = JsonFileCache(file_path, ttl=300)

# 1 hour TTL
cache = JsonFileCache(file_path, ttl=3600)
```

### Cache Size Limits

```python
# Unlimited cache
cache = JsonFileCache(file_path, max_size=None)

# Limit to 50 entries (LRU eviction)
cache = JsonFileCache(file_path, max_size=50)
```

### Statistics

```python
# Enable statistics (default)
cache = JsonFileCache(file_path, enable_stats=True)

# Disable statistics (slight performance gain)
cache = JsonFileCache(file_path, enable_stats=False)

# Get statistics
stats = cache.get_stats()
# Returns: {
#     "hits": 42,
#     "misses": 8,
#     "hit_rate": 0.84,
#     "invalidations": 3,
#     "size": 1,
#     "max_size": None
# }
```

---

## Error Handling

### File Not Found

```python
# Returns empty dict or None (configurable)
cache = JsonFileCache(file_path)
data = cache.get_or_load()  # Returns {} if file missing
```

### JSON Parse Errors

```python
# Logs error and returns default value
try:
    data = cache.get_or_load()
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON: {e}")
    return {}  # or raise, depending on configuration
```

### Permission Errors

```python
# Handles file locking gracefully
try:
    data = cache.get_or_load()
except PermissionError as e:
    logger.warning(f"File locked: {e}")
    return None  # or retry
```

### Configuration

```python
class JsonFileCache:
    def __init__(
        self,
        file_path: Path,
        default_value: Any = None,  # Return on error
        raise_on_error: bool = False,  # Raise vs return default
        retry_on_error: bool = True,  # Retry on transient errors
        max_retries: int = 3
    ):
        ...
```

---

## Example Usage Patterns

### Pattern 1: Simple File Caching

```python
@json_file_cache(file_path=Path(".todo2/commits.json"))
def load_commits() -> list[dict]:
    with open(".todo2/commits.json") as f:
        return json.load(f).get("commits", [])
```

### Pattern 2: TTL + Mtime

```python
@json_file_cache(
    file_path=Path(".exarp/session_mode.json"),
    ttl=600  # 10 minutes, or invalidate on file change
)
def load_session_mode() -> dict:
    with open(".exarp/session_mode.json") as f:
        return json.load(f)
```

### Pattern 3: Resource Handler

```python
@mcp.resource()
async def get_tasks_resource(ctx: Context) -> str:
    @json_file_cache(file_path=Path(".todo2/state.todo2.json"))
    def load_tasks():
        # Load logic...
        return tasks
    
    tasks = load_tasks()
    return json.dumps(tasks, separators=(',', ':'))
```

### Pattern 4: Context Manager

```python
def load_data_with_context():
    cache = JsonFileCache(Path(".todo2/commits.json"), ttl=300)
    
    data = cache.get_or_load()
    
    # Use data...
    
    # Cache automatically managed
```

---

## Statistics API

```python
# Get cache statistics
stats = cache.get_stats()

# Example output:
{
    "hits": 42,
    "misses": 8,
    "hit_rate": 0.84,
    "invalidations": 3,
    "invalidations_mtime": 2,
    "invalidations_ttl": 1,
    "evictions": 0,
    "size": 1,
    "max_size": None,
    "ttl": 300,
    "file_path": ".todo2/commits.json",
    "last_access": "2025-12-21T01:00:00Z",
    "last_invalidation": "2025-12-21T00:55:00Z"
}

# Global statistics
manager = JsonCacheManager.get_instance()
all_stats = manager.get_all_stats()
```

---

## Implementation Notes

### Thread Safety

- Use `threading.Lock` for thread-safe operations
- Consider `asyncio.Lock` for async operations
- Document thread-safety guarantees

### Memory Management

- LRU eviction uses `collections.OrderedDict`
- Track memory usage if needed
- Consider weak references for large objects

### Performance

- Minimize file stat calls (cache mtime)
- Use compact JSON for storage
- Lazy load statistics if not needed

---

## Migration Path

### Step 1: Create Utility
- Implement `JsonFileCache` class
- Implement decorator `@json_file_cache`
- Add tests

### Step 2: Migrate High-Priority Loaders
- Migrate memories loader
- Migrate commits loader
- Migrate session mode loader

### Step 3: Refactor Existing Caching
- Replace `tasks.py` caching with utility
- Maintain backward compatibility

### Step 4: Add Advanced Features
- Add dependency tracking
- Add cascade invalidation
- Add performance metrics

---

## Next Steps

1. ✅ API design complete
2. ⏭️ Implement `JsonFileCache` class
3. ⏭️ Implement decorator
4. ⏭️ Add tests
5. ⏭️ Migrate existing loaders
