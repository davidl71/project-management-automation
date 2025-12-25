# Performance Improvement Opportunities


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**P25-12-25  
**Status**: Low-Hanging Fruit Identified

---

## Quick Wins (Low Effort, High Impact)

### 1. ✅ Cache `find_project_root()` Calls ⭐⭐⭐

**Impact**: Medium-High  
**Effort**: Very Low  
**Files**: `project_management_automation/utils/project_root.py`

**Problem**: `find_project_root()` walks up the directory tree on every call. It's called 30+ times across the codebase.

**Solution**: Add simple module-level cache (only invalidates on process restart, which is fine):

```python
# In project_root.py
_cached_project_root: Optional[Path] = None

def find_project_root(start_path: Optional[Path] = None) -> Path:
    global _cached_project_root
    
    # If explicit start_path, don't use cache
    if start_path is not None:
        result = _search_up(Path(start_path))
        return result if result else Path(start_path).resolve()
    
    # Use cached value if available
    if _cached_project_root is not None:
        return _cached_project_root
    
    # ... existing logic ...
    _cached_project_root = result
    return result
```

**Estimated Speedup**: 2-5x for functions that call it repeatedly

---

### 2. ✅ Use Compact JSON for Resources ⭐⭐⭐

**Impact**: High  
**Effort**: Very Low  
**Files**: All `project_management_automation/resources/*.py`

**Problem**: All resources use `json.dumps(..., indent=2)` which is:
- **~6x slower** to serialize (13.79ms vs 2.33ms for 100 tasks)
- **~68% larger** (8399 vs 4991 bytes for 100 tasks)
- **Worse for AI** (more tokens to process)

**Solution**: Use compact JSON for AI consumption (resources are for AI, not humans):

```python
# Before
return json.dumps(result, indent=2)

# After
return json.dumps(result, separators=(',', ':'))
```

**Files to Update** (20+ instances):
- `resources/tasks.py` (2 instances)
- `resources/assignees.py` (6 instances)
- `resources/cache.py` (1 instance)
- `resources/history.py` (1 instance)
- `resources/hint_registry.py` (3 instances)
- `resources/memories.py` (multiple)
- `resources/prompt_discovery.py` (5 instances)
- `resources/session.py` (4 instances)
- `resources/status.py` (1 instance)
- `resources/list.py` (1 instance)
- `resources/templates.py` (multiple)

**Estimated Speedup**: 5-6x JSON serialization, 68% size reduction, fewer tokens for AI

---

### 3. ✅ Cache Todo2 State in Resources ⭐⭐

**Impact**: Medium  
**Effort**: Low  
**Files**: `project_management_automation/resources/tasks.py`

**Problem**: `_load_todo2_state()` is called multiple times:
- Once in `get_tasks_resource()`
- Once in `get_agents_resource()`
- File is ~2400 lines, 538 tasks - expensive to parse repeatedly

**Solution**: Add simple file modification time cache:

```python
_todo2_cache: Optional[dict[str, Any]] = None
_todo2_cache_mtime: Optional[float] = None

def _load_todo2_state() -> dict[str, Any]:
    global _todo2_cache, _todo2_cache_mtime
    
    project_root = find_project_root()
    todo2_file = project_root / '.todo2' / 'state.todo2.json'
    
    if not todo2_file.exists():
        return {"todos": []}
    
    # Check if file was modified
    current_mtime = todo2_file.stat().st_mtime
    if _todo2_cache is not None and _todo2_cache_mtime == current_mtime:
        return _todo2_cache
    
    # Load and cache
    try:
        with open(todo2_file) as f:
            data = json.load(f)
            _todo2_cache = data
            _todo2_cache_mtime = current_mtime
            return data
    except Exception as e:
        logger.error(f"Error loading Todo2 state: {e}")
        return {"todos": [], "error": str(e)}
```

**Estimated Speedup**: 2-3x for repeated resource calls (if file hasn't changed)

---

### 4. ✅ Optimize Status Count Calculation ⭐

**Impact**: Low-Medium  
**Effort**: Very Low  
**Files**: `project_management_automation/resources/tasks.py:125-129`

**Problem**: Status counting iterates through already-filtered tasks list twice.

**Current Code**:
```python
# Limit results
tasks = tasks[:limit]

# Count by status (only current project tasks)
status_counts = {}
for task in tasks:  # Iterate again
    task_status = task.get('status', 'Unknown')
    status_counts[task_status] = status_counts.get(task_status, 0) + 1
```

**Solution**: Count during filtering, or use `collections.Counter`:

```python
# Count during filtering (before limit)
status_counts = {}
for task in tasks:  # Before [:limit]
    task_status = task.get('status', 'Unknown')
    status_counts[task_status] = status_counts.get(task_status, 0) + 1

# Limit results
tasks = tasks[:limit]
```

**Estimated Speedup**: Small (~5-10%) but easy win

---

## Implementation Priority

1. **Compact JSON** (⭐⭐⭐) - Easiest, biggest impact, affects token usage
2. **Cache `find_project_root()`** (⭐⭐⭐) - Very easy, good impact
3. **Cache Todo2 state** (⭐⭐) - Easy, medium impact
4. **Optimize status counting** (⭐) - Very easy, small impact

---

## Performance Measurements

### JSON Formatting (100 iterations, 100 tasks):
- `indent=2`: 13.79ms
- `separators=(',', ':')`: 2.33ms
- **Speedup: 5.93x faster**
- **Size: 68% larger with indent**

### Todo2 File Size:
- ~2400 lines
- 538 tasks
- Estimated parse time: ~10-20ms per load

---

## Future Optimizations (Not Low-Hanging)

1. **Resource-level caching** - Cache entire resource responses with TTL
2. **Lazy loading** - Only load fields needed for filtering
3. **Indexing** - Build indexes for common queries (status, project_id, tags)
4. **Streaming JSON** - For very large task lists
5. **Connection pooling** - Already implemented for MCP calls ✅
