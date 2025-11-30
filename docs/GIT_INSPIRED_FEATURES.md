# Git-Inspired Task Management Features

This document describes the Git-inspired task management features implemented in the project management automation system.

**Note**: These features were inspired by concepts from [GitTask](https://github.com/Bengerthelorf/gittask) (GPL-3.0). All implementations are original Python code. See [ATTRIBUTIONS.md](../ATTRIBUTIONS.md) for details.

## Overview

These features bring Git version control concepts to task management:
- **Repositories** = Projects
- **Branches** = Work streams (features, bugfixes, etc.)
- **Tasks** = Work items
- **Commits** = Change history records

## Features Implemented

### 1. Automatic Commit History ✅

Every task change is automatically tracked as a commit:
- Task creation → Create commit
- Task update → Update commit with diff
- Task deletion → Delete commit
- Status change → Status change commit

**Storage**: `.todo2/commits.json`

**Usage**:
```python
from project_management_automation.utils.commit_tracking import (
    track_task_create,
    track_task_update,
    track_task_delete,
    track_task_status_change,
)

# Automatically tracked when tasks are modified
commit = track_task_create(task_id, task_data, author="user", branch="feature-auth")
```

### 2. Branch Tags ✅

Tasks are organized into branches using tags with the `branch:` prefix.

**Convention**: `branch:feature-name`, `branch:bugfix-name`, etc.
- Main branch: Tasks without branch tag (default)
- Feature branches: Tasks with `branch:feature-name` tag

**Usage**:
```python
from project_management_automation.utils.branch_utils import (
    get_task_branch,
    set_task_branch,
    filter_tasks_by_branch,
    get_all_branches,
)

# Get branch for a task
branch = get_task_branch(task)

# Set branch for a task
task = set_task_branch(task, "feature-auth")

# Filter tasks by branch
feature_tasks = filter_tasks_by_branch(all_tasks, "feature-auth")

# Get all branches
branches = get_all_branches(all_tasks)
```

### 3. Task Diff Tool ✅

Compare task versions across commits to see what changed.

**Features**:
- Compare two commits
- Compare by timestamp
- Show field-by-field differences
- Formatted diff output

**Usage**:
```python
from project_management_automation.tools.task_diff import (
    compare_task_versions,
    get_task_history,
    task_diff,
)

# Compare task versions
result = compare_task_versions(
    task_id="task-123",
    version1_commit_id="commit-abc",
    version2_commit_id="commit-xyz",
)

# Get complete history
history = get_task_history("task-123", branch="feature-auth")

# Generate formatted diff
diff_output = task_diff("task-123", commit1="abc", commit2="xyz")
```

### 4. Git Graph Visualization ✅

Generate visual timelines of commits (text or Graphviz DOT format).

**Formats**:
- **Text**: ASCII graph showing commit history
- **DOT**: Graphviz format for rendering as images

**Usage**:
```python
from project_management_automation.tools.git_graph import (
    generate_commit_graph,
    get_branch_timeline,
)

# Generate text graph
graph = generate_commit_graph(branch="feature-auth", format="text")

# Generate Graphviz DOT
dot_graph = generate_commit_graph(
    branch="feature-auth",
    format="dot",
    output_path=Path("graph.dot"),
)

# Get branch timeline
timeline = get_branch_timeline("feature-auth")
```

### 5. Branch Merge Workflow ✅

Merge tasks from one branch into another with conflict detection.

**Features**:
- Conflict detection (same task ID, different fields)
- Conflict resolution strategies:
  - `newer`: Use task with later timestamp
  - `source`: Always use source branch version
  - `target`: Always use target branch version
- Merge commit tracking
- Dry-run preview

**Usage**:
```python
from project_management_automation.tools.branch_merge import (
    merge_branches,
    preview_merge,
)

# Preview merge (dry run)
preview = preview_merge("feature-auth", "main")

# Merge branches
result = merge_branches(
    source_branch="feature-auth",
    target_branch="main",
    conflict_strategy="newer",
    author="user",
)
```

## Architecture

### File Structure

```
project_management_automation/
├── utils/
│   ├── commit_tracking.py    # Commit tracking system
│   └── branch_utils.py       # Branch management utilities
├── tools/
│   ├── task_diff.py          # Task version comparison
│   ├── git_graph.py          # Visualization generation
│   ├── branch_merge.py       # Branch merging workflow
│   └── git_inspired_tools.py # MCP-compatible tool wrappers
└── .todo2/
    ├── state.todo2.json      # Task storage
    └── commits.json          # Commit history
```

### Data Models

#### TaskCommit
- `id`: Unique commit ID
- `task_id`: Associated task ID
- `message`: Commit message (e.g., "Create task: Login bug fix")
- `old_state`: Previous task state
- `new_state`: New task state
- `timestamp`: Commit timestamp
- `author`: Who made the change
- `branch`: Branch name

#### Branch Organization
- Tasks belong to branches via `branch:` tags
- Main branch = default (no tag)
- Feature branches = `branch:feature-name` tag

## Integration Points

### Automatic Commit Tracking

To enable automatic commit tracking, wrap task operations:

```python
from project_management_automation.utils.commit_tracking import (
    track_task_create,
    track_task_update,
    track_task_delete,
)

# When creating a task
def create_task(task_data):
    # ... create task in Todo2 ...
    track_task_create(task_id, task_data, author="system", branch="main")
    
# When updating a task
def update_task(task_id, old_state, new_state):
    # ... update task in Todo2 ...
    track_task_update(task_id, old_state, new_state, author="system", branch="main")
```

### MCP Tool Integration

Git-inspired tools are available as MCP-compatible functions:

```python
from project_management_automation.tools.git_inspired_tools import (
    get_task_commits,
    list_branches,
    merge_branch_tools,
    generate_graph,
)
```

## Examples

### Example 1: Track Task Changes

```python
from project_management_automation.utils.commit_tracking import track_task_update
from project_management_automation.utils.branch_utils import get_task_branch

# Get old state
old_task = load_task("task-123")

# Update task
new_task = old_task.copy()
new_task["status"] = "completed"
save_task(new_task)

# Track commit
branch = get_task_branch(new_task)
track_task_update(
    task_id="task-123",
    old_state=old_task,
    new_state=new_task,
    author="user",
    branch=branch,
)
```

### Example 2: Compare Task Versions

```python
from project_management_automation.tools.task_diff import compare_task_versions

# Compare current vs previous commit
result = compare_task_versions(
    task_id="task-123",
    version1_time=datetime(2025, 1, 1),
    version2_time=datetime.now(),
)

print(result["formatted"])
# Output:
# Task: Login bug fix
# ============================================================
# Changed Fields:
# ------------------------------------------------------------
#   status:
#     - "in_progress"
#     + "completed"
```

### Example 3: Merge Feature Branch

```python
from project_management_automation.tools.branch_merge import merge_branches

# Preview merge
preview = preview_merge("feature-auth", "main")
print(f"Would merge {preview['would_merge']} tasks")
print(f"Conflicts: {len(preview['conflicts'])}")

# Merge if OK
if preview['conflicts'] == 0:
    result = merge_branches(
        source_branch="feature-auth",
        target_branch="main",
        conflict_strategy="newer",
        author="user",
    )
    print(f"Merged {result['merged_tasks']} tasks")
```

### Example 4: Visualize Commit History

```python
from project_management_automation.tools.git_graph import generate_commit_graph
from pathlib import Path

# Generate text graph
graph_text = generate_commit_graph(
    branch="feature-auth",
    format="text",
    max_commits=20,
)
print(graph_text)

# Generate Graphviz DOT (can render with: dot -Tpng graph.dot -o graph.png)
dot_content = generate_commit_graph(
    branch="feature-auth",
    format="dot",
    output_path=Path("feature-auth-graph.dot"),
)
```

## Best Practices

1. **Use Branch Tags Consistently**: Follow naming convention `branch:feature-name`
2. **Track All Changes**: Enable automatic commit tracking for all task operations
3. **Review Before Merging**: Always preview merge before executing
4. **Resolve Conflicts Carefully**: Review conflict resolutions before accepting
5. **Regular Cleanup**: Archive old commits periodically to manage storage

## Future Enhancements

Potential improvements:
- Interactive conflict resolution UI
- Branch protection rules (e.g., require review before merging to main)
- Commit message templates
- Branch statistics dashboard
- Integration with Git repositories (link commits to Git commits)
- Export to external visualization tools

## Related Documentation

- `docs/GITTASK_ANALYSIS.md` - Original GitTask analysis
- `docs/GITTASK_SUMMARY.md` - Quick reference summary
- GitTask Repository: https://github.com/Bengerthelorf/gittask

## Support

For issues or questions:
1. Check commit history: `.todo2/commits.json`
2. Review branch organization: Task tags with `branch:` prefix
3. Examine diff output for change details
4. Use preview before merging branches

