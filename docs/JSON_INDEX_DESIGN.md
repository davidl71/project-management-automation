# JSON Index Design

**Date**: 2025-12-21  
**Status**: Design Complete  
**Task**: Design index data structures for common query patterns

---

## Overview

In-memory indexes for frequently queried JSON data to avoid O(n) full-file scans.

---

## Index Data Structures

### Tasks Indexes

#### 1. Tasks by Status
```python
# Structure: dict[str, list[str]]
# Key: status value (e.g., "pending", "in-progress", "done", "blocked")
# Value: List of task IDs with that status

status_index: dict[str, list[str]] = {
    "pending": ["task-1", "task-3", "task-7"],
    "in-progress": ["task-2", "task-5"],
    "done": ["task-4", "task-6"],
    "blocked": ["task-8"]
}
```

#### 2. Tasks by Project ID
```python
# Structure: dict[str, list[str]]
# Key: project_id
# Value: List of task IDs for that project

project_index: dict[str, list[str]] = {
    "project-1": ["task-1", "task-2", "task-3"],
    "project-2": ["task-4", "task-5"]
}
```

#### 3. Tasks by Tags
```python
# Structure: dict[str, list[str]]
# Key: tag name
# Value: List of task IDs with that tag

tags_index: dict[str, list[str]] = {
    "bug": ["task-1", "task-5"],
    "enhancement": ["task-2", "task-3", "task-7"],
    "documentation": ["task-4"]
}
```

**Note**: Tasks can have multiple tags, so a task ID may appear in multiple tag lists.

#### 4. Tasks by Assignee
```python
# Structure: dict[str, list[str]]
# Key: assignee name/ID
# Value: List of task IDs assigned to that person

assignee_index: dict[str, list[str]] = {
    "alice": ["task-1", "task-3"],
    "bob": ["task-2", "task-5"],
    "unassigned": ["task-4", "task-6"]
}
```

### Memories Indexes

#### 5. Memories by Category
```python
# Structure: dict[str, list[str]]
# Key: category (e.g., "debug", "research", "architecture")
# Value: List of memory IDs in that category

category_index: dict[str, list[str]] = {
    "debug": ["memory-1", "memory-3"],
    "research": ["memory-2", "memory-5"],
    "architecture": ["memory-4"]
}
```

#### 6. Memories by Linked Task ID
```python
# Structure: dict[str, list[str]]
# Key: task_id
# Value: List of memory IDs linked to that task

linked_task_index: dict[str, list[str]] = {
    "task-1": ["memory-1", "memory-2"],
    "task-2": ["memory-3"]
}
```

**Note**: Memories can be linked to multiple tasks, so a memory ID may appear in multiple task lists.

---

## Combined Index Structure

```python
class JsonIndexes:
    """Container for all indexes."""
    
    def __init__(self):
        # Task indexes
        self.tasks_by_status: dict[str, list[str]] = {}
        self.tasks_by_project: dict[str, list[str]] = {}
        self.tasks_by_tag: dict[str, list[str]] = {}
        self.tasks_by_assignee: dict[str, list[str]] = {}
        
        # Memory indexes
        self.memories_by_category: dict[str, list[str]] = {}
        self.memories_by_task: dict[str, list[str]] = {}
        
        # Metadata
        self.built_at: datetime
        self.source_file: Path
        self.version: int = 1
```

---

## Update Strategy

### Option 1: Full Rebuild (Simple)
```python
def rebuild_indexes(data: dict[str, Any]) -> JsonIndexes:
    """Rebuild all indexes from scratch."""
    indexes = JsonIndexes()
    
    # Build task indexes
    for task in data.get("todos", []):
        task_id = task["id"]
        
        # Status index
        status = task.get("status", "unknown")
        indexes.tasks_by_status.setdefault(status, []).append(task_id)
        
        # Project index
        project_id = task.get("projectId")
        if project_id:
            indexes.tasks_by_project.setdefault(project_id, []).append(task_id)
        
        # Tags index
        for tag in task.get("tags", []):
            indexes.tasks_by_tag.setdefault(tag, []).append(task_id)
        
        # Assignee index
        assignee = task.get("assignee", "unassigned")
        indexes.tasks_by_assignee.setdefault(assignee, []).append(task_id)
    
    return indexes
```

**Pros:**
- Simple to implement
- Always consistent
- No incremental update complexity

**Cons:**
- O(n) rebuild on every change
- Slower for large datasets

### Option 2: Incremental Update (Complex)
```python
def update_indexes(
    indexes: JsonIndexes,
    old_data: dict[str, Any],
    new_data: dict[str, Any]
) -> JsonIndexes:
    """Incrementally update indexes based on changes."""
    # Compare old vs new
    # Add new entries
    # Remove deleted entries
    # Update modified entries
    ...
```

**Pros:**
- Faster for small changes
- Better for large datasets

**Cons:**
- Complex to implement
- Risk of inconsistency
- Need to track changes

### Recommendation: **Full Rebuild**
- Current data size: ~1.5MB (small)
- Rebuild time: <50ms estimated
- Simplicity > Performance at this scale
- Can optimize later if needed

---

## Memory Usage Estimates

### Current Data Size
- Tasks: ~538 tasks
- Memories: ~10-50 memories (estimated)

### Index Memory Usage

**Tasks Indexes:**
- Status index: ~538 task IDs × 4 statuses = ~2KB
- Project index: ~538 task IDs × 1 project = ~1KB
- Tags index: ~538 task IDs × 2 tags avg = ~2KB
- Assignee index: ~538 task IDs × 1 assignee = ~1KB
- **Total: ~6KB**

**Memories Indexes:**
- Category index: ~50 memory IDs × 5 categories = ~1KB
- Linked task index: ~50 memory IDs × 2 tasks avg = ~1KB
- **Total: ~2KB**

**Total Index Memory: ~8KB** (negligible)

**Conclusion**: Memory usage is minimal, full rebuild is acceptable.

---

## Query API Design

### Task Queries

```python
def get_tasks_by_status(status: str, full_data: bool = False) -> list[dict]:
    """
    Get tasks by status using index.
    
    Args:
        status: Status to filter by
        full_data: If True, return full task objects; if False, return IDs only
    
    Returns:
        List of tasks or task IDs
    """
    task_ids = indexes.tasks_by_status.get(status, [])
    
    if full_data:
        # Load full task data (from cache)
        tasks = load_tasks()
        return [t for t in tasks if t["id"] in task_ids]
    else:
        return task_ids

def get_tasks_by_project(project_id: str, full_data: bool = False) -> list[dict]:
    """Get tasks by project ID using index."""
    task_ids = indexes.tasks_by_project.get(project_id, [])
    # Similar implementation...

def get_tasks_by_tag(tag: str, full_data: bool = False) -> list[dict]:
    """Get tasks by tag using index."""
    task_ids = indexes.tasks_by_tag.get(tag, [])
    # Similar implementation...

def get_tasks_by_assignee(assignee: str, full_data: bool = False) -> list[dict]:
    """Get tasks by assignee using index."""
    task_ids = indexes.tasks_by_assignee.get(assignee, [])
    # Similar implementation...
```

### Memory Queries

```python
def get_memories_by_category(category: str, full_data: bool = False) -> list[dict]:
    """Get memories by category using index."""
    memory_ids = indexes.memories_by_category.get(category, [])
    # Similar implementation...

def get_memories_by_task(task_id: str, full_data: bool = False) -> list[dict]:
    """Get memories linked to a task using index."""
    memory_ids = indexes.memories_by_task.get(task_id, [])
    # Similar implementation...
```

### Combined Queries

```python
def get_tasks_by_status_and_tag(status: str, tag: str) -> list[dict]:
    """Get tasks matching both status and tag."""
    status_ids = set(indexes.tasks_by_status.get(status, []))
    tag_ids = set(indexes.tasks_by_tag.get(tag, []))
    matching_ids = status_ids & tag_ids  # Set intersection
    # Return full task data...
```

---

## Integration with Cache

```python
class JsonFileCache:
    def __init__(self, file_path: Path, build_indexes: bool = True):
        self.file_path = file_path
        self.build_indexes = build_indexes
        self.indexes: Optional[JsonIndexes] = None
    
    def get_or_load(self) -> dict[str, Any]:
        """Load data and build indexes if enabled."""
        data = self._load_data()
        
        if self.build_indexes:
            self.indexes = rebuild_indexes(data)
        
        return data
    
    def get_indexes(self) -> Optional[JsonIndexes]:
        """Get indexes (must call get_or_load first)."""
        return self.indexes
```

---

## Performance Comparison

### Without Indexes (Current)
```python
# O(n) scan through all tasks
tasks = load_tasks()
pending = [t for t in tasks if t.get("status") == "pending"]
# Time: ~10-20ms for 538 tasks
```

### With Indexes (Proposed)
```python
# O(1) lookup + O(k) where k = number of matching tasks
indexes = cache.get_indexes()
pending_ids = indexes.tasks_by_status.get("pending", [])
pending = [t for t in tasks if t["id"] in pending_ids]
# Time: <1ms for lookup + ~2-5ms for data retrieval
```

**Speedup: ~5-10x** for status queries

---

## Next Steps

1. ✅ Index schema design complete
2. ⏭️ Implement index builder
3. ⏭️ Implement query API
4. ⏭️ Integrate with cache utility
5. ⏭️ Add tests
