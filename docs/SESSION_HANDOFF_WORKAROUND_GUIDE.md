# Session Handoff - Workaround Guide

**Date:** 2025-11-30  
**Issue:** MCP framework error preventing tool access  
**Solution:** Direct Python access wrapper

## Quick Start

### Option 1: Use Convenience Functions (Easiest)

```python
from project_management_automation.tools.session_handoff_wrapper import (
    resume,
    latest,
    list_handoffs,
    end_session,
    sync_state
)

# Resume session (returns dict)
context = resume()
print(f"Host: {context['current_host']}")
print(f"Previous handoff from: {context.get('previous_handoff', {}).get('from_host')}")

# Get latest handoff
handoff = latest()
print(f"Summary: {handoff.get('summary')}")

# List recent handoffs
handoffs = list_handoffs(limit=5)
print(f"Total handoffs: {handoffs.get('total_handoffs', 0)}")

# End session
result = end_session(
    summary="Completed feature X",
    blockers=["Need to test"],
    next_steps=["Add tests"]
)

# Sync state
sync_result = sync_state(direction="pull")
```

### Option 2: Use Wrapper Class

```python
from project_management_automation.tools.session_handoff_wrapper import SessionHandoffWrapper

wrapper = SessionHandoffWrapper()

# Resume
context = wrapper.resume()

# Unified handoff method
result = wrapper.handoff("resume")
result = wrapper.handoff("latest")
result = wrapper.handoff("list", limit=10)
result = wrapper.handoff("end", summary="Done", next_steps=["Test"])
result = wrapper.handoff("sync", direction="pull")
```

### Option 3: Direct Function Access (Original)

```python
from project_management_automation.tools.session_handoff import (
    session_handoff,
    resume_session,
    get_latest_handoff,
    list_handoffs
)
import json

# Returns JSON string
result_str = session_handoff('resume')
result_dict = json.loads(result_str)
```

## API Reference

### Convenience Functions

All convenience functions return Python dictionaries for easy use.

#### `resume() -> dict`
Resume session and get context.
```python
context = resume()
# Returns: {
#     "success": True,
#     "current_host": "...",
#     "previous_handoff": {...},
#     "available_work": {...},
#     "recommendations": [...]
# }
```

#### `latest() -> dict`
Get latest handoff note.
```python
handoff = latest()
# Returns: {
#     "success": True,
#     "handoff": {...}
# }
```

#### `list_handoffs(limit: int = 5) -> dict`
List recent handoff notes.
```python
handoffs = list_handoffs(limit=10)
# Returns: {
#     "success": True,
#     "handoffs": [...],
#     "total_handoffs": 10
# }
```

#### `end_session(summary, blockers, next_steps, ...) -> dict`
End current session and create handoff.
```python
result = end_session(
    summary="Completed authentication module",
    blockers=["Need to test on Ubuntu"],
    next_steps=["Add integration tests"],
    unassign_my_tasks=True,
    include_git_status=True
)
```

#### `sync_state(direction, prefer_agentic_tools, auto_commit, dry_run) -> dict`
Sync Todo2 state across machines.
```python
result = sync_state(
    direction="both",  # "pull", "push", or "both"
    prefer_agentic_tools=True,
    auto_commit=True,
    dry_run=False
)
```

### Wrapper Class

#### `SessionHandoffWrapper`

**Methods:**
- `resume() -> dict` - Resume session
- `latest() -> dict` - Get latest handoff
- `list(limit: int) -> dict` - List handoffs
- `end(...) -> dict` - End session
- `sync(...) -> dict` - Sync state
- `handoff(action: str, **kwargs) -> dict` - Unified entry point

**Usage:**
```python
wrapper = SessionHandoffWrapper()
result = wrapper.handoff("resume")
```

## Examples

### Example 1: Resume and Pick Up Work

```python
from project_management_automation.tools.session_handoff_wrapper import resume

context = resume()

# Check for blockers
if context.get('previous_handoff', {}).get('blockers'):
    print("⚠️ Blockers from previous session:")
    for blocker in context['previous_handoff']['blockers']:
        print(f"  - {blocker}")

# Check available work
work = context.get('available_work', {})
print(f"\n📋 Available tasks: {work.get('total_unassigned', 0)}")
print(f"   Orphaned in-progress: {len(work.get('orphaned_in_progress', []))}")

# Show recommendations
for rec in context.get('recommendations', []):
    print(f"\n💡 {rec}")
```

### Example 2: End Session and Create Handoff

```python
from project_management_automation.tools.session_handoff_wrapper import end_session

result = end_session(
    summary="Implemented authentication module with OAuth2 support",
    blockers=[
        "Need to test on Ubuntu server",
        "Waiting for OAuth app credentials from team"
    ],
    next_steps=[
        "Add integration tests",
        "Set up OAuth app in staging",
        "Update documentation"
    ],
    include_git_status=True
)

if result.get('success'):
    print(f"✅ Session ended successfully")
    print(f"   Handoff ID: {result.get('handoff_id')}")
    if result.get('warnings'):
        for warning in result['warnings']:
            print(f"   ⚠️ {warning}")
```

### Example 3: Sync State Before Starting

```python
from project_management_automation.tools.session_handoff_wrapper import sync_state, resume

# Sync latest state from remote
sync_result = sync_state(direction="pull")
if sync_result.get('success'):
    print(f"✅ Synced: {sync_result.get('message')}")
    
    # Now resume to get latest context
    context = resume()
    print(f"📋 Resumed session from {context.get('current_host')}")
else:
    print(f"❌ Sync failed: {sync_result.get('error')}")
```

## Comparison: MCP vs Wrapper

| Feature | MCP Interface | Wrapper (Workaround) |
|---------|---------------|----------------------|
| **Status** | ❌ Broken (framework error) | ✅ Working perfectly |
| **Return Type** | JSON string | Python dict |
| **Error Handling** | Framework error | Works correctly |
| **Access** | Via MCP tool call | Direct Python import |
| **Performance** | N/A (broken) | Fast (direct call) |
| **Usability** | N/A | Easy (returns dicts) |

## Migration Guide

### From MCP Interface

**Before (Broken):**
```python
# This doesn't work due to framework error
session_handoff(action="resume")
```

**After (Works):**
```python
from project_management_automation.tools.session_handoff_wrapper import resume

# Returns dict directly
context = resume()
```

### From Direct Function Calls

**Before:**
```python
from project_management_automation.tools.session_handoff import resume_session
import json

result_str = resume_session()
result = json.loads(result_str)
```

**After (Easier):**
```python
from project_management_automation.tools.session_handoff_wrapper import resume

# Returns dict directly, no JSON parsing needed
result = resume()
```

## Benefits

### ✅ Immediate Access
- Works right now, no framework fix needed
- Direct Python access, fast and reliable

### ✅ Better Developer Experience
- Returns Python dicts instead of JSON strings
- No need to parse JSON manually
- Type hints and IDE autocomplete

### ✅ Same Functionality
- All features available
- Same error handling
- Same validation

## When to Use

**Use Wrapper When:**
- ✅ MCP framework has issues
- ✅ Want direct Python access
- ✅ Prefer dicts over JSON strings
- ✅ Need reliability

**Use MCP Interface When:**
- ✅ Framework is fixed
- ✅ Want MCP protocol benefits
- ✅ Integrating with MCP clients

## Files

- `project_management_automation/tools/session_handoff_wrapper.py` - Wrapper implementation
- `project_management_automation/tools/session_handoff.py` - Core functions (working)

## Status

**Current:** ✅ Wrapper works perfectly  
**Future:** Will work via MCP once framework is fixed

The wrapper provides a reliable workaround while the FastMCP framework issue is resolved.
