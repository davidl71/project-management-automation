# Dependency Graph Design

> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python and NetworkX, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use NetworkX for graph algorithms? use context7"
> - "Show me Python graph data structure examples use context7"
> - "Python NetworkX best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-12-21  
**Status**: Design Complete  
**Task**: Design dependency graph structure for cache invalidation

---

## Overview

Dependency graph tracks relationships between JSON files to enable cascade cache invalidation when dependent files change.

---

## Dependency Graph Structure

### Data Structure

```python
class DependencyGraph:
    """Tracks file dependencies for cache invalidation."""
    
    def __init__(self):
        # Direct dependencies: file -> set of dependent files
        self.dependencies: dict[Path, set[Path]] = {}
        
        # Reverse lookup: dependent file -> set of source files
        self.dependents: dict[Path, set[Path]] = {}
        
        # Cache keys for each file
        self.file_cache_keys: dict[Path, set[str]] = {}
```

### Example Dependencies

```python
# When .todo2/state.todo2.json changes:
# - Invalidate task indexes
# - Invalidate filtered task views
# - Invalidate task statistics

dependencies = {
    Path(".todo2/state.todo2.json"): {
        Path(".todo2/.cache/task_indexes.json"),  # If we cache indexes
        Path(".todo2/.cache/task_stats.json"),
    },
    
    Path(".exarp/memories/*.json"): {
        Path(".exarp/.cache/memory_indexes.json"),
    },
    
    Path("project_config.json"): {
        Path(".exarp/.cache/project_resources.json"),
    }
}
```

---

## Dependency Types

### 1. Direct Dependencies
One file directly depends on another.

```python
# Task indexes depend on task file
add_dependency(
    source=Path(".todo2/state.todo2.json"),
    dependent=Path(".todo2/.cache/task_indexes.json")
)
```

### 2. Transitive Dependencies
Dependencies that chain through multiple files.

```python
# Project resources depend on project config
# Project config depends on git config
# So project resources transitively depend on git config

# We track direct only, compute transitive on demand
```

### 3. Wildcard Dependencies
Dependencies on file patterns.

```python
# Memory indexes depend on any memory file
add_dependency(
    source=Path(".exarp/memories/*.json"),  # Pattern
    dependent=Path(".exarp/.cache/memory_indexes.json")
)
```

---

## Storage Format

### Option 1: In-Memory Only (Recommended)
```python
# Store in memory during runtime
# Rebuild from code/config on startup
# No persistence needed
```

**Pros:**
- Simple
- No file I/O
- Always up-to-date with code

**Cons:**
- Must be defined in code
- Not configurable at runtime

### Option 2: Configuration File
```python
# .exarp/cache_dependencies.json
{
    "dependencies": [
        {
            "source": ".todo2/state.todo2.json",
            "dependents": [
                ".todo2/.cache/task_indexes.json",
                ".todo2/.cache/task_stats.json"
        }
    },
    {
        "source": ".exarp/memories/*.json",
        "dependents": [
            ".exarp/.cache/memory_indexes.json"
        ]
    }
]
```

**Pros:**
- Configurable
- Can be modified without code changes

**Cons:**
- Extra file to manage
- Risk of inconsistency

### Recommendation: **In-Memory with Code Registration**

Define dependencies in code, register on startup:

```python
# In json_cache.py or cache_invalidation.py
def register_default_dependencies(manager: DependencyGraph):
    """Register default file dependencies."""
    
    # Task file dependencies
    manager.add_dependency(
        source=Path(".todo2/state.todo2.json"),
        dependents=[
            Path(".todo2/.cache/task_indexes.json"),
            Path(".todo2/.cache/task_stats.json"),
        ]
    )
    
    # Memory file dependencies
    manager.add_dependency(
        source=Path(".exarp/memories/*.json"),  # Pattern
        dependents=[
            Path(".exarp/.cache/memory_indexes.json"),
        ]
    )
```

---

## API Design

### Dependency Registration

```python
class DependencyGraph:
    def add_dependency(
        self,
        source: Path,
        dependent: Path,
        bidirectional: bool = False
    ) -> None:
        """
        Register a dependency relationship.
        
        Args:
            source: Source file (when this changes, invalidate dependent)
            dependent: Dependent file/cache (invalidated when source changes)
            bidirectional: If True, also register reverse dependency
        """
    
    def add_dependencies(
        self,
        source: Path,
        dependents: list[Path],
        bidirectional: bool = False
    ) -> None:
        """Register multiple dependents for one source."""
    
    def remove_dependency(
        self,
        source: Path,
        dependent: Path
    ) -> None:
        """Remove a dependency relationship."""
    
    def get_dependents(self, source: Path) -> set[Path]:
        """Get all files that depend on source."""
    
    def get_sources(self, dependent: Path) -> set[Path]:
        """Get all files that dependent depends on."""
```

### Pattern Matching

```python
def get_dependents_for_pattern(self, pattern: Path) -> set[Path]:
    """
    Get dependents for file pattern (e.g., *.json).
    
    Args:
        pattern: Path with wildcards (e.g., Path(".exarp/memories/*.json"))
    
    Returns:
        Set of dependent paths
    """
    # Match pattern against registered sources
    # Return union of all matching dependents
```

### Circular Dependency Detection

```python
def detect_cycles(self) -> list[list[Path]]:
    """
    Detect circular dependencies.
    
    Returns:
        List of cycles (each cycle is a list of paths)
    """
    # Use DFS to detect cycles
    # Return all cycles found
```

---

## Cascade Invalidation

### Implementation

```python
class CacheInvalidationManager:
    """Manages cascade cache invalidation."""
    
    def __init__(self, dependency_graph: DependencyGraph):
        self.dependency_graph = dependency_graph
        self.cache_manager = JsonCacheManager.get_instance()
    
    def invalidate_on_file_change(self, changed_file: Path) -> None:
        """
        Invalidate all dependent caches when a file changes.
        
        Args:
            changed_file: Path to file that changed
        """
        # Get all dependents
        dependents = self.dependency_graph.get_dependents(changed_file)
        
        # Also check pattern matches
        pattern_dependents = self._get_pattern_dependents(changed_file)
        dependents.update(pattern_dependents)
        
        # Invalidate each dependent cache
        for dependent in dependents:
            self.cache_manager.invalidate_file(dependent)
            logger.info(f"Invalidated {dependent} due to {changed_file} change")
    
    def _get_pattern_dependents(self, file_path: Path) -> set[Path]:
        """Get dependents for file matching patterns."""
        dependents = set()
        
        for pattern, pattern_dependents in self.dependency_graph.pattern_dependencies.items():
            if self._matches_pattern(file_path, pattern):
                dependents.update(pattern_dependents)
        
        return dependents
```

### Integration with File Watcher

```python
# Option 1: Manual invalidation
invalidation_manager = CacheInvalidationManager(dependency_graph)
invalidation_manager.invalidate_on_file_change(Path(".todo2/state.todo2.json"))

# Option 2: Automatic via file watcher (future)
# Watch for file changes, automatically invalidate
```

---

## Example Dependencies

### Task-Related Dependencies

```python
# When .todo2/state.todo2.json changes:
dependencies = {
    Path(".todo2/state.todo2.json"): [
        # Task indexes
        Path(".todo2/.cache/indexes/tasks_by_status.json"),
        Path(".todo2/.cache/indexes/tasks_by_project.json"),
        Path(".todo2/.cache/indexes/tasks_by_tag.json"),
        Path(".todo2/.cache/indexes/tasks_by_assignee.json"),
        
        # Task statistics
        Path(".todo2/.cache/stats/task_counts.json"),
        Path(".todo2/.cache/stats/status_distribution.json"),
        
        # Filtered views (if cached)
        Path(".todo2/.cache/views/pending_tasks.json"),
        Path(".todo2/.cache/views/high_priority_tasks.json"),
    ]
}
```

### Memory-Related Dependencies

```python
# When any .exarp/memories/*.json changes:
dependencies = {
    Path(".exarp/memories/*.json"): [  # Pattern
        Path(".exarp/.cache/indexes/memories_by_category.json"),
        Path(".exarp/.cache/indexes/memories_by_task.json"),
        Path(".exarp/.cache/stats/memory_counts.json"),
    ]
}
```

### Project Config Dependencies

```python
# When project config changes:
dependencies = {
    Path("pyproject.toml"): [
        Path(".exarp/.cache/project_metadata.json"),
    ],
    
    Path(".cursorrules"): [
        Path(".exarp/.cache/project_rules.json"),
    ]
}
```

---

## Configuration Examples

### Code-Based Registration

```python
# In cache_invalidation.py
def setup_dependencies():
    """Setup default dependency graph."""
    graph = DependencyGraph()
    
    # Task dependencies
    graph.add_dependencies(
        source=Path(".todo2/state.todo2.json"),
        dependents=[
            Path(".todo2/.cache/task_indexes.json"),
            Path(".todo2/.cache/task_stats.json"),
        ]
    )
    
    # Memory dependencies (pattern)
    graph.add_dependency(
        source=Path(".exarp/memories/*.json"),
        dependent=Path(".exarp/.cache/memory_indexes.json")
    )
    
    return graph
```

### Runtime Registration

```python
# When creating a cache, register dependencies
cache = JsonFileCache(
    file_path=Path(".todo2/.cache/task_indexes.json"),
    depends_on=[Path(".todo2/state.todo2.json")]
)

# Automatically registers dependency
```

---

## Circular Dependency Detection

### Example

```python
# Circular dependency (should be detected)
graph.add_dependency(A, B)  # A depends on B
graph.add_dependency(B, C)  # B depends on C
graph.add_dependency(C, A)  # C depends on A (cycle!)

cycles = graph.detect_cycles()
# Returns: [[A, B, C, A]]
```

### Prevention

```python
def add_dependency(self, source: Path, dependent: Path) -> None:
    """Add dependency with cycle detection."""
    # Check if adding would create cycle
    if self._would_create_cycle(source, dependent):
        raise ValueError(f"Circular dependency detected: {source} <-> {dependent}")
    
    # Add dependency
    self.dependencies[source].add(dependent)
```

---

## Next Steps

1. ✅ Dependency graph design complete
2. ⏭️ Implement `DependencyGraph` class
3. ⏭️ Implement cascade invalidation
4. ⏭️ Integrate with cache manager
5. ⏭️ Add tests
