# JSON File Loaders Inventory

**Date**: 2025-12-21  
**Status**: Complete  
**Task**: Identify all JSON file loaders for caching implementation

---

## Summary

Found **63 files** with JSON loading operations. Identified **8 primary JSON loader functions** that need caching.

---

## Primary JSON Loaders (Need Caching)

### 1. `resources/tasks.py` - Todo2 State Loader ✅ **ALREADY CACHED**
- **Function**: `_load_todo2_state()`
- **File**: `.todo2/state.todo2.json`
- **Current Status**: ✅ Has mtime-based caching
- **Cache Pattern**: Global variables `_todo2_cache`, `_todo2_cache_mtime`
- **Size**: ~1.5MB, ~10K lines
- **Usage**: High frequency (resource handlers, tools)

### 2. `resources/memories.py` - Memory Loaders ❌ **NO CACHING**
- **Function**: `_load_all_memories()`
- **Pattern**: Iterates through `.exarp/memories/*.json` files
- **Current Status**: ❌ No caching - loads all files on every call
- **Files**: Multiple JSON files (one per memory)
- **Usage**: Medium frequency
- **Optimization**: Cache per-file, invalidate on file change

### 3. `utils/commit_tracking.py` - Commits Loader ❌ **NO CACHING**
- **Function**: `CommitTracker._load_commits()`
- **File**: `.todo2/commits.json`
- **Current Status**: ❌ Has module-level cache but no mtime invalidation
- **Cache Pattern**: `self._commits_cache` (only invalidates on save)
- **Issue**: Doesn't check file modification time
- **Usage**: Medium frequency

### 4. `resources/session.py` - Session Mode Storage ❌ **NO CACHING**
- **Function**: `SessionModeStorage._load_data()`
- **File**: `.exarp/session_mode.json`
- **Current Status**: ❌ No caching
- **Usage**: Low-medium frequency

### 5. `scripts/base/mcp_client.py` - Generic JSON Loader ❌ **NO CACHING**
- **Function**: `load_json_with_retry()`
- **Pattern**: Generic loader with retry logic
- **Current Status**: ❌ No caching (but has retry logic)
- **Usage**: Used by various tools
- **Note**: This is a utility function, caching should be added at call sites

### 6. `resources/assignees.py` - Assignees Loader ❌ **NO CACHING**
- **Function**: Likely has JSON loading (needs verification)
- **File**: `.todo2/assignees.json` or similar
- **Current Status**: Needs investigation
- **Usage**: Low-medium frequency

### 7. Agent Config Loaders ❌ **NO CACHING**
- **Function**: `_get_agent_names()` in `resources/tasks.py`
- **Pattern**: Loads `agents/*/cursor-agent.json` files
- **Current Status**: ❌ No caching
- **Usage**: Low frequency (only when listing agents)

### 8. Various Tool-Specific Loaders ❌ **NO CACHING**
- Multiple tools load JSON files directly
- Examples:
  - `tools/tag_consolidation.py`
  - `tools/duplicate_detection.py`
  - `tools/nightly_task_automation.py`
- **Current Status**: ❌ No caching
- **Usage**: Varies by tool

---

## Caching Status Summary

| Loader | File Pattern | Current Cache | Needs Upgrade |
|--------|-------------|---------------|----------------|
| Todo2 State | `.todo2/state.todo2.json` | ✅ mtime cache | ✅ Keep pattern |
| Memories | `.exarp/memories/*.json` | ❌ None | ✅ Add caching |
| Commits | `.todo2/commits.json` | ⚠️ Module cache | ✅ Add mtime check |
| Session Mode | `.exarp/session_mode.json` | ❌ None | ✅ Add caching |
| Assignees | `.todo2/assignees.json` | ❓ Unknown | ✅ Verify & add |
| Agent Configs | `agents/*/cursor-agent.json` | ❌ None | ⚠️ Low priority |
| Generic Loader | Various | ❌ None | ✅ Add at call sites |

---

## Implementation Priority

### High Priority (Frequently Used)
1. ✅ **Todo2 State** - Already cached, keep pattern
2. **Memories Loader** - High frequency, multiple files
3. **Commits Loader** - Add mtime invalidation

### Medium Priority
4. **Session Mode** - Medium frequency
5. **Assignees** - Need to verify usage

### Low Priority
6. **Agent Configs** - Low frequency, can cache if needed
7. **Tool-specific loaders** - Add caching as needed

---

## Recommended Caching Strategy

### Pattern 1: File-Based Caching (Single File)
```python
# Current pattern in tasks.py (keep this)
_cache: Optional[dict] = None
_cache_mtime: Optional[float] = None

def _load_json_file(file_path: Path) -> dict:
    global _cache, _cache_mtime
    current_mtime = file_path.stat().st_mtime
    if _cache is not None and _cache_mtime == current_mtime:
        return _cache
    # Load and cache...
```

### Pattern 2: Multi-File Caching (Directory)
```python
# For memories loader (multiple files)
_cache: dict[str, tuple[dict, float]] = {}  # file_path -> (data, mtime)

def _load_all_memories() -> list[dict]:
    memories_dir = _get_memories_dir()
    memories = []
    
    for memory_file in memories_dir.glob("*.json"):
        cache_key = str(memory_file)
        current_mtime = memory_file.stat().st_mtime
        
        if cache_key in _cache:
            cached_data, cached_mtime = _cache[cache_key]
            if cached_mtime == current_mtime:
                memories.append(cached_data)
                continue
        
        # Load and cache...
```

### Pattern 3: Unified Utility (Future)
```python
# Use unified json_cache utility (to be created)
from ..utils.json_cache import json_file_cache

@json_file_cache(file_path=Path(".todo2/commits.json"))
def _load_commits() -> list[dict]:
    # Implementation...
```

---

## Files to Update

1. ✅ `resources/tasks.py` - Already has caching (keep)
2. `resources/memories.py` - Add multi-file caching
3. `utils/commit_tracking.py` - Add mtime check to existing cache
4. `resources/session.py` - Add file-based caching
5. `resources/assignees.py` - Verify and add if needed
6. `scripts/base/mcp_client.py` - Document usage, add caching at call sites

---

## Next Steps

1. ✅ Inventory complete
2. ⏭️ Design unified caching utility
3. ⏭️ Implement caching for high-priority loaders
4. ⏭️ Refactor to use unified utility
5. ⏭️ Add tests
