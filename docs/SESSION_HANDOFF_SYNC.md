# Session Handoff State Sync

> **Sync Todo2 state across agents without manual git commits**

## Overview

The `session_handoff` tool now includes a `sync` action that enables automatic synchronization of Todo2 state across multiple agents/machines without requiring manual git commits.

## Problem Solved

Previously, syncing Todo2 state (`.todo2/state.todo2.json`) across agents required:
1. Manual `git add .todo2/state.todo2.json`
2. Manual `git commit -m "Update state"`
3. Manual `git push`

This was cumbersome and error-prone when multiple agents were working simultaneously.

## Solution

The `sync` action provides **two sync methods**:

### 1. Agentic-Tools MCP (Preferred)

When available, uses the agentic-tools MCP server which:
- Manages its own state file (`.agentic-tools-mcp/tasks/tasks.json`)
- Automatically syncs when operations are performed
- Provides better conflict resolution
- Works across different Todo2 implementations

**Benefits:**
- ✅ No manual commits needed
- ✅ Automatic state management
- ✅ Better error handling
- ✅ Format-agnostic

### 2. Git Auto-Sync (Fallback)

When agentic-tools MCP is unavailable, falls back to git-based sync:
- Automatically commits state changes with descriptive messages
- Automatically pushes to remote
- Handles merge conflicts gracefully
- Pulls remote changes before pushing

**Benefits:**
- ✅ Works with existing git workflow
- ✅ Automatic commit/push
- ✅ Conflict detection
- ✅ No manual intervention needed

## Usage

### Basic Sync (Pull then Push)

```python
session_handoff(action="sync")
# or explicitly:
session_handoff(action="sync", direction="both")
```

### Pull Only

```python
session_handoff(action="sync", direction="pull")
```

### Push Only

```python
session_handoff(action="sync", direction="push")
```

### Force Git Method

```python
session_handoff(action="sync", prefer_agentic_tools=False)
```

### Dry Run

```python
session_handoff(action="sync", dry_run=True)
```

## Sync Directions

| Direction | Description |
|-----------|-------------|
| `pull` | Fetch and merge remote state changes |
| `push` | Auto-commit and push local state changes |
| `both` | Pull remote changes, then push local changes (default) |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `direction` | `str` | `"both"` | Sync direction: "pull", "push", or "both" |
| `prefer_agentic_tools` | `bool` | `True` | Try agentic-tools MCP first |
| `auto_commit` | `bool` | `True` | Auto-commit state changes for git sync |
| `dry_run` | `bool` | `False` | Preview sync operations without changes |

## How It Works

### Agentic-Tools MCP Flow

1. **Pull**: Calls `list_todos()` to ensure latest state is loaded
2. **Push**: Operations automatically update `.agentic-tools-mcp/tasks/tasks.json`
3. The MCP server handles its own git commits (if configured)

### Git Auto-Sync Flow

1. **Pull**:
   - `git fetch origin`
   - Check if behind remote
   - `git merge origin/<branch>` if needed
   - Handle conflicts gracefully

2. **Push**:
   - Check for uncommitted changes in `.todo2/`
   - `git add .todo2/state.todo2.json .todo2/handoffs.json`
   - `git commit -m "Auto-sync Todo2 state from <host> [timestamp]"`
   - `git push origin HEAD`

## Example Output

### Successful Sync (Agentic-Tools)

```json
{
  "success": true,
  "host": "dlowes-dell",
  "timestamp": "2025-11-29T12:00:00Z",
  "direction": "both",
  "methods_tried": [
    {
      "success": true,
      "method": "agentic-tools",
      "direction": "both",
      "tasks_synced": 55,
      "message": "Agentic-tools MCP state synced (uses .agentic-tools-mcp/tasks/tasks.json)"
    }
  ],
  "final_method": "agentic-tools",
  "message": "Synced via agentic-tools MCP",
  "duration_ms": 234.5
}
```

### Successful Sync (Git Auto)

```json
{
  "success": true,
  "host": "dlowes-dell",
  "timestamp": "2025-11-29T12:00:00Z",
  "direction": "both",
  "methods_tried": [
    {
      "success": false,
      "method": "agentic-tools",
      "error": "MCP client not available"
    },
    {
      "success": true,
      "method": "git-auto",
      "direction": "both",
      "operations": ["fetched", "already_up_to_date", "staged", "committed", "pushed"]
    }
  ],
  "final_method": "git-auto",
  "message": "Synced via git auto-commit/push: fetched, already_up_to_date, staged, committed, pushed",
  "duration_ms": 1234.5
}
```

## Integration with Other Actions

The `sync` action can be combined with other session handoff actions:

```python
# Sync before ending session
session_handoff(action="sync", direction="push")
session_handoff(action="end", summary="Completed feature X")

# Sync when resuming
session_handoff(action="sync", direction="pull")
session_handoff(action="resume")
```

## Best Practices

1. **Before Starting Work**: Pull latest state
   ```python
   session_handoff(action="sync", direction="pull")
   ```

2. **After Making Changes**: Push state changes
   ```python
   session_handoff(action="sync", direction="push")
   ```

3. **End of Session**: Sync both directions
   ```python
   session_handoff(action="sync", direction="both")
   session_handoff(action="end", summary="...")
   ```

4. **Use Agentic-Tools When Available**: It provides better conflict resolution and state management

## Troubleshooting

### Merge Conflicts

If git auto-sync detects merge conflicts:
- The sync will fail gracefully
- You'll need to manually resolve conflicts
- Then run sync again

### Agentic-Tools Not Available

If agentic-tools MCP is not configured:
- The system automatically falls back to git auto-sync
- No action needed

### Network Issues

If git push/pull fails:
- Check network connectivity
- Verify git remote is configured
- Check git credentials

## Future Enhancements

Potential improvements:
- [ ] Real-time sync via WebSocket/SSE
- [ ] Conflict resolution UI
- [ ] Sync status monitoring
- [ ] Batch sync operations
- [ ] Custom sync strategies

## Related Documentation

- [Session Handoff Guide](./SESSION_HANDOFF.md) - General session handoff usage
- [Agentic-Tools Integration](./AGENTIC_TOOLS_INTEGRATION_PLAN.md) - MCP integration details
- [Task Assignee Guide](./TASK_ASSIGNEE_GUIDE.md) - Cross-host task coordination
