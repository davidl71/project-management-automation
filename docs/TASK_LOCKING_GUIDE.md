# Task Locking Guide

**Purpose**: Prevent concurrent task assignment using file-based locking

---

## Overview

The task locking system uses OS-level file locks to prevent race conditions when multiple agents try to assign the same task simultaneously. This ensures that only one agent can claim a task at a time.

---

## How It Works

### File-Based Locking

Uses OS-level file locking (`fcntl` on Unix, `msvcrt` on Windows) to coordinate access:
- **Task-specific locks**: `.todo2/locks/task_{task_id}.lock`
- **State file lock**: `.todo2/state.todo2.json.lock` (for batch operations)

### Lock Hierarchy

1. **Task-level locks**: Lock individual tasks for assignment
2. **State file lock**: Lock entire state file for batch operations

---

## Usage Patterns

### Pattern 1: Atomic Task Assignment

```python
from project_management_automation.utils.task_locking import atomic_assign_task

# Try to assign a task atomically
success, error = atomic_assign_task(
    task_id="T-123",
    assignee_name="backend-agent",
    assignee_type="agent",
    timeout=5.0
)

if success:
    print("Task assigned successfully")
else:
    print(f"Assignment failed: {error}")
    # Task might already be assigned or not found
```

### Pattern 2: Check and Assign

```python
from project_management_automation.utils.task_locking import atomic_check_and_assign

# Check if available and assign
result = atomic_check_and_assign(
    task_id="T-123",
    assignee_name="backend-agent",
    assignee_type="agent"
)

if result["assigned"]:
    print("Task assigned successfully")
elif result.get("existing_assignee"):
    print(f"Task already assigned to: {result['existing_assignee']}")
else:
    print(f"Assignment failed: {result['reason']}")
```

### Pattern 3: Context Manager (Manual Control)

```python
from project_management_automation.utils.file_lock import task_lock

# Lock task for custom operations
with task_lock(task_id="T-123", timeout=5.0):
    # Load state
    state = _load_todo2_state()
    
    # Find and modify task
    task = find_task(state, "T-123")
    if not task.get("assignee"):
        task["assignee"] = {"name": "agent-1", "type": "agent"}
        _save_todo2_state(state)
```

### Pattern 4: Batch Assignment

```python
from project_management_automation.utils.task_locking import atomic_batch_assign

# Assign multiple tasks atomically
result = atomic_batch_assign(
    task_ids=["T-123", "T-456", "T-789"],
    assignee_name="backend-agent",
    assignee_type="agent"
)

print(f"Assigned: {result['assigned']}")
print(f"Failed: {result['failed']}")
```

### Pattern 5: State File Lock (Multiple Tasks)

```python
from project_management_automation.utils.file_lock import state_file_lock

# Lock entire state file for complex operations
with state_file_lock(timeout=10.0):
    state = _load_todo2_state()
    
    # Modify multiple tasks
    for task in state["todos"]:
        if should_modify(task):
            modify_task(task)
    
    _save_todo2_state(state)
```

---

## Integration with Existing Code

### Update `task_assignee.py`

Replace direct assignment with atomic operations:

```python
# Before
task["assignee"] = assignee
_save_todo2_state(state)

# After
from ..utils.task_locking import atomic_assign_task

success, error = atomic_assign_task(
    task_id=task["id"],
    assignee_name=assignee["name"],
    assignee_type=assignee["type"],
    hostname=assignee.get("hostname")
)
```

### Update `nightly_task_automation.py`

Use atomic assignment in task distribution:

```python
# Before
task['assignee'] = {
    'type': 'host',
    'name': host_key,
    ...
}

# After
from ..utils.task_locking import atomic_assign_task

success, error = atomic_assign_task(
    task_id=task['id'],
    assignee_name=host_key,
    assignee_type='host',
    hostname=host_info['hostname'],
    assigned_by='nightly_automation'
)

if not success:
    logger.warning(f"Failed to assign {task['id']}: {error}")
    continue  # Skip this task, try next
```

---

## Lock Files

Lock files are created in `.todo2/locks/`:
- `task_{task_id}.lock` - Per-task locks
- `state.todo2.json.lock` - Global state file lock

**Note**: Lock files are automatically cleaned up when processes exit. Stale locks (from crashed processes) are handled by timeout mechanisms.

---

## Error Handling

### Lock Timeout

If a lock cannot be acquired within the timeout:
- Returns `(False, "Lock timeout")`
- Indicates another process is holding the lock
- Retry with exponential backoff if needed

### Task Already Assigned

If task already has an assignee:
- Returns `(False, "Task already assigned to agent:name")`
- Check `existing_assignee` in result for details

### Task Not Found

If task doesn't exist:
- Returns `(False, "Task not found")`
- Verify task ID is correct

---

## Performance Considerations

### Lock Granularity

- **Task-level locks**: Better for parallel operations (multiple tasks)
- **State file lock**: Required for batch operations (all-or-nothing)

### Timeout Values

- **Short timeout (1-2s)**: For quick checks
- **Medium timeout (5s)**: Default for assignments
- **Long timeout (10s+)**: For batch operations

### Lock Cleanup

Locks are automatically released when:
- Context manager exits (normal flow)
- Process terminates (OS cleanup)
- Explicit `release()` called

---

## Best Practices

1. **Always use atomic operations** for task assignment
2. **Check return values** - don't assume assignment succeeded
3. **Use appropriate timeouts** - balance between responsiveness and reliability
4. **Handle lock timeouts gracefully** - retry or skip task
5. **Use task-level locks** when possible (better parallelism)
6. **Use state file lock** only for batch operations

---

## Example: Safe Task Assignment Loop

```python
from project_management_automation.utils.task_locking import atomic_check_and_assign

def assign_available_tasks(task_ids: list[str], agent_name: str):
    """Safely assign available tasks to an agent."""
    assigned = []
    failed = []
    
    for task_id in task_ids:
        result = atomic_check_and_assign(
            task_id=task_id,
            assignee_name=agent_name,
            assignee_type="agent",
            timeout=2.0
        )
        
        if result["assigned"]:
            assigned.append(task_id)
        elif result.get("existing_assignee"):
            # Task already taken - skip
            failed.append({
                "task_id": task_id,
                "reason": "Already assigned",
                "to": result["existing_assignee"]
            })
        else:
            # Other error
            failed.append({
                "task_id": task_id,
                "reason": result["reason"]
            })
    
    return {
        "assigned": assigned,
        "failed": failed,
        "total": len(task_ids)
    }
```

---

## Testing

Test locking with multiple processes:

```python
# Process 1
atomic_assign_task("T-123", "agent-1")

# Process 2 (simultaneous)
atomic_assign_task("T-123", "agent-2")
# Should fail: "Task already assigned to agent:agent-1"
```

---

## Migration Path

1. ✅ Create locking utilities (`file_lock.py`, `task_locking.py`)
2. ⏭️ Update `task_assignee.py` to use atomic operations
3. ⏭️ Update `nightly_task_automation.py` to use atomic operations
4. ⏭️ Add tests for concurrent assignment scenarios
5. ⏭️ Document in main README

---

**Status**: Utilities created, ready for integration  
**Created**: 2025-12-21
