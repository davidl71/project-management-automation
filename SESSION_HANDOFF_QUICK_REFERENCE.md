# Session Handoff Quick Reference

## Available Actions

### 1. `latest` - Get Latest Handoff
Get information about the most recent session handoff.

```python
session_handoff(action="latest")
```

### 2. `list` - List Recent Handoffs
List recent handoffs (default: 5 most recent).

```python
session_handoff(action="list", limit=5)
```

### 3. `resume` - Resume Latest Handoff
Resume the most recent handoff session.

```python
session_handoff(action="resume")
```

### 4. `end` - End Current Session
End the current session and create a handoff.

```python
session_handoff(
    action="end",
    summary="Finished feature X",
    blockers=["Need API key"],
    next_steps=["Add tests", "Update docs"],
    unassign_my_tasks=True,
    include_git_status=True
)
```

### 5. `sync` - Sync Todo2 State
Synchronize Todo2 state across devices/agents.

```python
# Sync both directions (pull then push)
session_handoff(action="sync")

# Pull only
session_handoff(action="sync", direction="pull")

# Push only
session_handoff(action="sync", direction="push")

# Dry run
session_handoff(action="sync", dry_run=True)
```

## Common Workflows

### Starting a Session
```python
# Check for handoffs from other agents
session_handoff(action="resume")

# Or just check latest
session_handoff(action="latest")
```

### Ending a Session
```python
session_handoff(
    action="end",
    summary="Completed authentication module",
    next_steps=["Add integration tests", "Update documentation"]
)
```

### Syncing State
```python
# Before starting work
session_handoff(action="sync", direction="pull")

# After making changes
session_handoff(action="sync", direction="push")

# Or both at once
session_handoff(action="sync", direction="both")
```

## Direct Python Access

If MCP tool has issues, use direct Python:

```python
from project_management_automation.tools.session_handoff import session_handoff

result = session_handoff(action="latest")
print(result)
```

---

**What would you like to do?**
- Check latest handoff
- Resume a session
- End current session
- Sync state

