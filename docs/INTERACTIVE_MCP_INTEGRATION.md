# Interactive MCP Integration

**Date**: 2025-11-29  
**Status**: Implemented  
**Task**: RESEARCH-c162d40f

---

## Overview

Exarp integrates with `interactive-mcp` to provide human-in-the-loop workflows for confirmations, notifications, and interactive sessions. This integration is **optional** - Exarp gracefully falls back when interactive-mcp is not available.

## Features

### 1. User Confirmations (`confirm` parameter)

**Location**: `project_management_automation/tools/batch_task_approval.py`

Batch operations can request user confirmation before executing:

```python
from project_management_automation.tools.batch_task_approval import batch_approve_tasks

result = batch_approve_tasks(
    status="Review",
    new_status="Todo",
    confirm=True  # Request user confirmation
)
```

**Behavior**:
- If `confirm=True` and interactive-mcp is available, shows a prompt with options: `["yes", "no", "review"]`
- If user selects "no", operation is cancelled
- If user selects "review", returns preview without executing
- If user selects "yes", operation proceeds
- If interactive-mcp is unavailable, confirmation is skipped (backward compatible)

**MCP Tool Usage**:
```json
{
  "action": "approve",
  "status": "Review",
  "new_status": "Todo",
  "confirm": true
}
```

### 2. Completion Notifications (`notify` parameter)

**Locations**:
- `project_management_automation/tools/nightly_task_automation.py`
- `project_management_automation/tools/sprint_automation.py`

Automation tools can send OS notifications when complete:

```python
from project_management_automation.tools.nightly_task_automation import run_nightly_task_automation

result = run_nightly_task_automation(
    max_tasks_per_host=5,
    notify=True  # Send notification on completion
)
```

**Notification Messages**:
- **Nightly**: `"Nightly automation complete: X tasks assigned, Y moved to Review, Z batch approved"`
- **Sprint**: `"Sprint automation complete: X subtasks extracted, Y tasks processed, Z blockers identified"`

**MCP Tool Usage**:
```json
{
  "action": "nightly",
  "notify": true
}
```

### 3. Critical Security Alerts (`alert_critical` parameter)

**Location**: `project_management_automation/tools/dependency_security.py`

Security scans can send alerts when critical vulnerabilities are found:

```python
from project_management_automation.tools.dependency_security import scan_dependency_security

result = scan_dependency_security(
    languages=["python"],
    alert_critical=True  # Alert on critical vulnerabilities
)
```

**Alert Message**: `"🚨 X CRITICAL vulnerabilities found! Total: Y vulnerabilities"`

**MCP Tool Usage**:
```json
{
  "action": "scan",
  "languages": ["python"],
  "alert_critical": true
}
```

## Implementation Details

### Module: `project_management_automation/interactive.py`

Provides wrapper functions for interactive-mcp tools:

```python
from project_management_automation.interactive import (
    is_available,
    request_user_input,
    message_complete_notification,
    start_intensive_chat,
    ask_intensive_chat,
    stop_intensive_chat,
)
```

**Features**:
- **Graceful Fallback**: All functions check `is_available()` before calling interactive-mcp
- **Error Handling**: Catches ImportError and other exceptions, logs warnings but doesn't fail
- **Type Safety**: Returns `None` when unavailable, allowing optional chaining

### Integration Pattern

All integrations follow this pattern:

```python
if notify and not dry_run:
    try:
        from ..interactive import message_complete_notification, is_available
        
        if is_available():
            message_complete_notification("Exarp", message)
    except ImportError:
        pass  # interactive-mcp not available
    except Exception as e:
        logger.debug(f"Notification failed: {e}")
```

## Configuration

### MCP Server Setup

Add `interactive-mcp` to your MCP configuration (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "interactive-mcp": {
      "command": "npx",
      "args": ["-y", "@ttommyth/interactive-mcp"]
    },
    "exarp": {
      "command": "python3",
      "args": ["-m", "project_management_automation.server"]
    }
  }
}
```

### Availability Check

Check if interactive-mcp is available:

```python
from project_management_automation.interactive import is_available

if is_available():
    # Use interactive features
    pass
else:
    # Fallback behavior
    pass
```

## Usage Examples

### Example 1: Batch Approval with Confirmation

```python
# Request confirmation before approving tasks
result = batch_approve_tasks(
    status="Review",
    new_status="Todo",
    clarification_none=True,
    confirm=True
)

if result.get("cancelled"):
    print("User cancelled approval")
elif result.get("requires_review"):
    print("User requested review:", result.get("preview"))
else:
    print(f"Approved {result['approved_count']} tasks")
```

### Example 2: Nightly Automation with Notification

```python
# Run nightly automation and notify on completion
result = run_nightly_task_automation(
    max_tasks_per_host=5,
    max_parallel_tasks=10,
    notify=True
)

# Notification sent automatically if interactive-mcp available
print(f"Assigned {result['summary']['tasks_assigned']} tasks")
```

### Example 3: Security Scan with Critical Alerts

```python
# Scan dependencies and alert on critical vulnerabilities
result = scan_dependency_security(
    languages=["python", "rust"],
    alert_critical=True
)

# Alert sent automatically if critical vulnerabilities found
vulns = json.loads(result)
print(f"Found {vulns['total_vulnerabilities']} vulnerabilities")
```

## Fallback Behavior

When interactive-mcp is **not available**:

1. **Confirmations**: Skipped silently, operations proceed as if `confirm=False`
2. **Notifications**: Skipped silently, no errors logged
3. **Alerts**: Skipped silently, scan results still returned

This ensures **backward compatibility** - existing code continues to work without interactive-mcp.

## Testing

Test interactive-mcp integration:

```python
from project_management_automation.interactive import is_available

# Check availability
assert is_available() == False  # When interactive-mcp not configured

# Test with mock (if needed)
# Mock interactive-mcp tools for testing
```

## Future Enhancements

Potential future integrations:

1. **Clarification Workflow**: Use `request_user_input` for task clarification resolution
2. **Intensive Chat Sessions**: Use `start_intensive_chat` for multi-step configuration
3. **Progress Updates**: Use notifications for long-running operations
4. **Error Escalation**: Use alerts for critical errors or failures

## References

- **interactive-mcp**: https://github.com/ttommyth/interactive-mcp
- **MCP SDK**: @modelcontextprotocol/sdk
- **Exarp Module**: `project_management_automation/interactive.py`

---

## Summary

✅ **RESEARCH-A1**: Created `exarp.interactive` module  
✅ **RESEARCH-A2**: Added `confirm` parameter to `batch_approve_tasks`  
✅ **RESEARCH-A3**: Added `notify` parameter to automation tools  
✅ **RESEARCH-A4**: Added `alert_critical` parameter to security scan  
✅ **RESEARCH-A5**: Documented integration (this file)

All features are **optional** and **backward compatible** - Exarp works perfectly without interactive-mcp, but provides enhanced UX when available.
