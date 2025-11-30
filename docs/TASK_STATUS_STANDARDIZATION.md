# Task Status Standardization

**Date**: 2025-11-30  
**Status**: Analysis Complete  
**Purpose**: Document status value inconsistencies and provide standardization recommendations

---

## Executive Summary

The codebase uses **inconsistent status values** across different modules, leading to potential bugs where tasks are not properly recognized. This document catalogs all status checks and provides a standardization plan.

---

## Current Status Values in Todo2

**Actual values found in `.todo2/state.todo2.json`:**
- `'completed'`: 55 tasks
- `'done'`: 4 tasks  
- `'todo'`: 14 tasks

**Total**: 73 tasks

---

## Status Checks Across Codebase

### 1. Project Scorecard (`project_scorecard.py`)

**Location**: Lines 193-195

```python
pending = [t for t in todos if t.get('status', '').lower() in ['pending', 'in_progress', 'todo', 'in-progress']]
completed = [t for t in todos if t.get('status', '').lower() in ['completed', 'done']]
```

**Issues**:
- ✅ Case-insensitive (good)
- ✅ Handles both `'completed'` and `'done'` (good)
- ❌ Checks for `'pending'` and `'in_progress'` which don't exist in actual data
- ❌ Checks for `'in-progress'` (hyphenated) which doesn't exist

**Also checks** (line 375):
```python
security_tasks = [t for t in todos if 'security' in t.get('tags', []) and t.get('status') == 'pending']
```
- ❌ Case-sensitive check for `'pending'` (doesn't exist)

---

### 2. Nightly Task Automation (`nightly_task_automation.py`)

**Location**: Lines 228-233

```python
# Skip if not in Todo status
if status not in ['Todo', 'todo']:
    return False

# Skip Review status (already reviewed)
if status == 'Review':
    return False
```

**Issues**:
- ❌ Case-sensitive check (`'Todo'` vs `'todo'`)
- ❌ Checks for `'Review'` which doesn't exist in actual data
- ✅ Handles both `'Todo'` and `'todo'` (but inconsistently)

**Also checks** (line 459):
```python
if task.get('status') in ['Todo', 'todo']:
```

**Also checks** (lines 547, 572):
```python
review_tasks_before = [t for t in todos if t.get('status') == 'Review']
review_tasks_after = [t for t in todos if t.get('status') == 'Review']
```
- ❌ Case-sensitive check for `'Review'` (doesn't exist)

---

### 3. Sprint Automation (`automate_sprint.py`)

**Location**: Lines 553-554

```python
actionable_statuses = ['Todo', 'todo', 'pending', 'Pending']
if status not in actionable_statuses:
    return False
```

**Issues**:
- ❌ Checks for `'pending'` and `'Pending'` which don't exist
- ❌ Case-sensitive checks mixed with case-insensitive logic
- ✅ Includes `'Todo'` and `'todo'` (but should be normalized)

---

### 4. Todo Sync (`automate_todo_sync.py`)

**Location**: Lines 47-56

```python
self.status_map = {
    'pending': 'Todo',
    'in_progress': 'In Progress',
    'completed': 'Done',
    'Todo': 'pending',
    'In Progress': 'in_progress',
    'Done': 'completed',
    'Review': 'in_progress',  # Review maps to in_progress in shared TODO
    'Cancelled': 'completed'  # Cancelled maps to completed
}
```

**Issues**:
- ✅ Has mapping (good for sync)
- ❌ Maps to values that don't exist in Todo2 (`'In Progress'`, `'Done'`)
- ❌ Maps from values that don't exist (`'Review'`, `'Cancelled'`)

---

### 5. Todo2 Alignment (`automate_todo2_alignment_v2.py`)

**Location**: Line 220

```python
'status': task.get('status', 'pending').replace('-', '_'),  # in-progress -> in_progress
```

**Issues**:
- ✅ Normalizes hyphenated statuses (good)
- ❌ Defaults to `'pending'` which doesn't exist in Todo2

---

### 6. Task Hierarchy Analyzer (`task_hierarchy_analyzer.py`)

**Location**: Lines 151-152

```python
pending = [t for t in matching_tasks if t.get('status') in ['pending', 'in_progress', 'in-progress']]
completed = [t for t in matching_tasks if t.get('status') in ['completed', 'done']]
```

**Issues**:
- ❌ Checks for `'pending'`, `'in_progress'`, `'in-progress'` which don't exist
- ✅ Handles both `'completed'` and `'done'` (good)

---

### 7. Task Assignee (`task_assignee.py`)

**Location**: Line 635

```python
if task.get("status") not in ["Todo", "todo"]:
    continue
```

**Issues**:
- ❌ Case-sensitive check
- ✅ Handles both cases (but should normalize)

**Also checks** (lines 461-464, 489-496):
```python
if status == "In Progress":
    unassigned["in_progress"] += 1
elif status == "Todo":
    unassigned["todo"] += 1
# ...
elif status == "Done":
    bucket[aname]["done"] += 1
elif status == "Review":
    bucket[aname]["review"] += 1
```

**Issues**:
- ❌ Checks for `"In Progress"`, `"Done"`, `"Review"` which don't exist
- ❌ Case-sensitive checks

---

### 8. Task Clarification Resolution (`task_clarification_resolution.py`)

**Location**: Line 258

```python
review_tasks = [t for t in todos if t.get('status') == 'Review']
```

**Issues**:
- ❌ Case-sensitive check for `'Review'` (doesn't exist)

---

### 9. Resources/Tasks (`resources/tasks.py`)

**Location**: Line 120

```python
if status:
    tasks = [t for t in tasks if t.get('status', '').lower() == status.lower()]
```

**Issues**:
- ✅ Case-insensitive comparison (good)

---

### 10. Project Overview (`project_overview.py`)

**Location**: Lines 210, 283

```python
if status in ['pending', 'in_progress', 'Todo']:
    remaining_hours += hours
# ...
and t.get('status') in ['pending', 'Todo', 'in_progress']]
```

**Issues**:
- ❌ Checks for `'pending'` and `'in_progress'` which don't exist
- ❌ Case-sensitive check for `'Todo'` (should be lowercase)

---

## Summary of Inconsistencies

### Status Values That Don't Exist in Actual Data

1. **`'pending'`** - Used in 8+ places, but actual value is `'todo'`
2. **`'in_progress'`** - Used in 5+ places, but doesn't exist
3. **`'in-progress'`** - Used in 3+ places, but doesn't exist
4. **`'Review'`** - Used in 4+ places, but doesn't exist
5. **`'In Progress'`** - Used in 2+ places, but doesn't exist
6. **`'Done'`** - Used in 3+ places, but actual value is `'done'` (lowercase)
7. **`'Cancelled'`** - Used in 1 place, but doesn't exist
8. **`'Blocked'`** - Used in 1 place, but doesn't exist

### Case Sensitivity Issues

- **Case-sensitive checks**: `nightly_task_automation.py`, `task_assignee.py`, `task_clarification_resolution.py`
- **Case-insensitive checks**: `project_scorecard.py`, `resources/tasks.py`
- **Mixed**: `sprint_automation.py`, `project_overview.py`

---

## Standardization Recommendations

### 1. Define Canonical Status Values

**Recommended canonical statuses** (based on actual usage):

```python
# Canonical status values (lowercase)
CANONICAL_STATUSES = {
    'todo': 'Todo',           # Pending/not started
    'in_progress': 'In Progress',  # Currently being worked on
    'review': 'Review',       # Awaiting review/approval
    'completed': 'Completed', # Finished
    'done': 'Done',          # Finished (alias for completed)
    'blocked': 'Blocked',    # Cannot proceed
    'cancelled': 'Cancelled', # Cancelled/abandoned
}
```

**Note**: Current data uses lowercase (`'todo'`, `'completed'`, `'done'`), but some code expects Title Case.

### 2. Create Status Normalization Utility

**Recommended location**: `project_management_automation/utils/todo2_utils.py`

```python
def normalize_status(status: str) -> str:
    """
    Normalize task status to canonical lowercase form.
    
    Args:
        status: Raw status value (case-insensitive, handles variants)
    
    Returns:
        Canonical lowercase status value
    """
    if not status:
        return 'todo'
    
    status_lower = status.lower().strip()
    
    # Map variants to canonical forms
    status_map = {
        # Pending/Todo variants
        'pending': 'todo',
        'not started': 'todo',
        'new': 'todo',
        
        # In Progress variants
        'in progress': 'in_progress',
        'in-progress': 'in_progress',
        'in_progress': 'in_progress',
        'working': 'in_progress',
        'active': 'in_progress',
        
        # Review variants
        'review': 'review',
        'needs review': 'review',
        'awaiting review': 'review',
        
        # Completed variants
        'completed': 'completed',
        'done': 'completed',  # Normalize 'done' to 'completed'
        'finished': 'completed',
        'closed': 'completed',
        
        # Blocked variants
        'blocked': 'blocked',
        'waiting': 'blocked',
        
        # Cancelled variants
        'cancelled': 'cancelled',
        'canceled': 'cancelled',  # US spelling
        'abandoned': 'cancelled',
    }
    
    return status_map.get(status_lower, status_lower)

def is_pending_status(status: str) -> bool:
    """Check if status represents a pending task."""
    normalized = normalize_status(status)
    return normalized in ['todo']

def is_completed_status(status: str) -> bool:
    """Check if status represents a completed task."""
    normalized = normalize_status(status)
    return normalized in ['completed', 'cancelled']

def is_active_status(status: str) -> bool:
    """Check if status represents an active (non-completed) task."""
    normalized = normalize_status(status)
    return normalized in ['todo', 'in_progress', 'review', 'blocked']
```

### 3. Update All Status Checks

**Pattern to use everywhere**:

```python
from project_management_automation.utils.todo2_utils import normalize_status, is_pending_status, is_completed_status

# Instead of:
if task.get('status') == 'Todo':
    # ...

# Use:
if normalize_status(task.get('status', '')) == 'todo':
    # ...

# Or use helper:
if is_pending_status(task.get('status', '')):
    # ...
```

### 4. Files Requiring Updates

**High Priority** (affects core functionality):
1. `project_management_automation/tools/project_scorecard.py` - Lines 194-195, 375
2. `project_management_automation/tools/nightly_task_automation.py` - Lines 228-233, 459, 547, 572
3. `project_management_automation/scripts/automate_sprint.py` - Lines 553-554
4. `project_management_automation/tools/task_assignee.py` - Lines 461-464, 489-496, 635
5. `project_management_automation/tools/task_clarification_resolution.py` - Line 258

**Medium Priority** (affects specific features):
6. `project_management_automation/tools/task_hierarchy_analyzer.py` - Lines 151-152
7. `project_management_automation/tools/project_overview.py` - Lines 210, 283
8. `project_management_automation/scripts/automate_todo2_alignment_v2.py` - Line 220

**Low Priority** (mapping/sync utilities):
9. `project_management_automation/scripts/automate_todo_sync.py` - Lines 47-56 (update mapping)

---

## Migration Plan

### Phase 1: Create Utility Functions
1. Add `normalize_status()` and helper functions to `utils/todo2_utils.py`
2. Add unit tests for normalization
3. Document canonical status values

### Phase 2: Update Core Tools (High Priority)
1. Update `project_scorecard.py`
2. Update `nightly_task_automation.py`
3. Update `automate_sprint.py`
4. Update `task_assignee.py`
5. Update `task_clarification_resolution.py`

### Phase 3: Update Supporting Tools (Medium Priority)
1. Update `task_hierarchy_analyzer.py`
2. Update `project_overview.py`
3. Update `automate_todo2_alignment_v2.py`

### Phase 4: Update Sync/Mapping (Low Priority)
1. Update `automate_todo_sync.py` status mapping
2. Verify cross-system compatibility

### Phase 5: Data Migration (Optional)
1. Normalize all existing task statuses in `.todo2/state.todo2.json`
2. Update any external systems that read Todo2 statuses

---

## Testing Checklist

After implementing standardization:

- [ ] All status checks use `normalize_status()` or helper functions
- [ ] Case-insensitive matching works correctly
- [ ] Variant statuses (`'done'` vs `'completed'`) are normalized
- [ ] Pending tasks are correctly identified
- [ ] Completed tasks are correctly identified
- [ ] Review tasks are correctly identified (if implemented)
- [ ] Project scorecard shows correct pending/completed counts
- [ ] Nightly automation processes correct tasks
- [ ] Sprint automation processes correct tasks
- [ ] Task assignment works correctly
- [ ] Clarification resolution works correctly

---

## References

- **Todo2 Format**: `.todo2/state.todo2.json`
- **Status Values**: See "Current Status Values in Todo2" section above
- **Related Documentation**: 
  - `docs/PARALLELIZATION_SETUP.md`
  - `docs/INTERACTIVE_MCP_INTEGRATION.md`

---

## Implementation Status

### ✅ Phase 1: Utility Functions (COMPLETED)

**Location**: `project_management_automation/utils/todo2_utils.py`

**Functions Added**:
- `normalize_status(status: str) -> str` - Normalizes status to canonical lowercase form
- `is_pending_status(status: str) -> bool` - Checks if status is pending
- `is_completed_status(status: str) -> bool` - Checks if status is completed
- `is_active_status(status: str) -> bool` - Checks if status is active (non-completed)
- `is_review_status(status: str) -> bool` - Checks if status is review

**Testing**: ✅ All test cases pass (17/17)

**Usage Example**:
```python
from project_management_automation.utils.todo2_utils import normalize_status, is_pending_status

# Normalize status
normalized = normalize_status(task.get('status', ''))  # 'Todo' -> 'todo', 'done' -> 'completed'

# Use helper functions
if is_pending_status(task.get('status', '')):
    # Handle pending task
    pass
```

### ✅ Phase 2: Update Core Tools (COMPLETED)

**Files Updated**:
1. ✅ `project_management_automation/tools/project_scorecard.py`
   - Lines 194-195: Updated pending/completed detection
   - Line 376: Updated security task filtering
   - Uses: `is_pending_status()`, `is_completed_status()`

2. ✅ `project_management_automation/tools/nightly_task_automation.py`
   - Lines 228-233: Updated `_is_background_capable()` status checks
   - Line 460: Updated interactive task detection
   - Lines 548, 573: Updated review task counting
   - Uses: `is_pending_status()`, `is_review_status()`

3. ✅ `project_management_automation/scripts/automate_sprint.py`
   - Lines 560-561: Updated actionable status check
   - Uses: `is_pending_status()`

4. ✅ `project_management_automation/tools/task_assignee.py`
   - Lines 463-467: Updated unassigned task status detection
   - Lines 492-500: Updated bucket status counting
   - Line 639: Updated Todo status filter
   - Uses: `normalize_status()`, `is_pending_status()`, `is_review_status()`

5. ✅ `project_management_automation/tools/task_clarification_resolution.py`
   - Line 259: Updated review task detection
   - Uses: `is_review_status()`

**Testing**: ✅ All imports verified, functional tests pass

### ✅ Phase 3: Update Supporting Tools (COMPLETED)

**Files Updated**:
1. ✅ `project_management_automation/tools/task_hierarchy_analyzer.py`
   - Lines 151-152: Updated pending/completed categorization
   - Uses: `is_pending_status()`, `is_completed_status()`

2. ✅ `project_management_automation/tools/project_overview.py`
   - Lines 204-215: Updated status counting and hour calculation
   - Line 287: Updated high-priority task filtering
   - Uses: `normalize_status()`, `is_active_status()`

**Testing**: ✅ All imports verified

### ⏳ Phase 4-5: Remaining Updates (OPTIONAL)

**Low Priority** (sync/mapping utilities):
- `project_management_automation/scripts/automate_todo_sync.py` - Status mapping (may need adjustment)
- `project_management_automation/scripts/automate_todo2_alignment_v2.py` - Default status handling

**Data Migration** (optional):
- Normalize all existing task statuses in `.todo2/state.todo2.json`
- Update any external systems that read Todo2 statuses

---

## Conclusion

**Current State**: 
- ✅ Status normalization utility implemented and tested
- ❌ Status checks still inconsistent across 10+ files  
**Impact**: Tasks may not be recognized correctly, leading to incorrect counts and automation failures  
**Recommendation**: Update all status checks to use `normalize_status()` or helper functions  
**Priority**: High (affects core functionality)

**Next Steps**:
1. ✅ ~~Implement `normalize_status()` utility~~ **COMPLETED**
2. Update high-priority files to use normalization functions
3. Test thoroughly
4. Update remaining files
5. Consider data migration (optional)
