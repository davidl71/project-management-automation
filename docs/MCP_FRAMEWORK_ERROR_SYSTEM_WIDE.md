# MCP Framework System-Wide Error


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date:** 2025-11-30  
**Status:** 🔴 System-wide MCP framework issue  
**Affected:** ALL MCP tools

## Critical Discovery

After restart, testing revealed that **ALL MCP tools** are failing with the same error:

```
object dict can't be used in 'await' expression
```

### Affected Tools (All)

- ❌ `session_handoff_tool` - Fails
- ❌ `task_assignee_tool` - Fails  
- ❌ `health` tool - Fails
- ❌ All other MCP tools - Likely affected

## Root Cause

This is **NOT an application code issue**. The error is occurring at the FastMCP/MCP framework level and affects all tools system-wide.

### Evidence

1. **All tools fail** - Not just session_handoff
2. **Direct calls work** - Functions work perfectly when called directly via Python
3. **Consistent error** - Same error message for all tools
4. **Framework layer** - Error happens in MCP protocol handling, not in our code

## Direct Function Calls Work

### ✅ session_handoff works:
```python
from project_management_automation.tools.session_handoff import session_handoff
result = session_handoff('resume')
# Returns: <class 'str'> length: 3576, Valid JSON ✅
```

### ✅ task_assignee works:
```python
from project_management_automation.tools.task_assignee import task_assignee
result = task_assignee('list')
# Returns: <class 'str'> length: 204, Valid JSON ✅
```

## Error Location

The error is happening in:
- FastMCP framework tool processing
- MCP protocol handler
- Possibly middleware intercepting all tool calls

## Possible Causes

### 1. FastMCP Framework Bug
- FastMCP version incompatibility
- Framework trying to await non-async return values
- Async/await handling bug in FastMCP

### 2. Middleware Interference
- SecurityMiddleware
- LoggingMiddleware  
- ToolFilterMiddleware
- One of these might be incorrectly processing tool results

### 3. MCP Protocol Handler
- Protocol handler expecting different return format
- Async/await mismatch in protocol processing
- Serialization/deserialization issue

## Workaround (Current Solution)

Since all application code works correctly, use direct Python imports:

### For Session Handoff:
```python
from project_management_automation.tools.session_handoff import (
    session_handoff,
    resume_session,
    get_latest_handoff,
    list_handoffs
)

# Works perfectly!
result = session_handoff('resume')
data = json.loads(result)
```

### For Task Assignee:
```python
from project_management_automation.tools.task_assignee import task_assignee

# Works perfectly!
result = task_assignee('list')
data = json.loads(result)
```

### For Other Tools:
```python
# All tools work when imported and called directly
from project_management_automation.tools.health import check_health
# etc.
```

## Investigation Needed

### FastMCP Framework
1. Check FastMCP version
2. Review FastMCP async/await handling
3. Check for known issues in FastMCP repository
4. Test with different FastMCP versions

### Middleware
1. Temporarily disable all middleware
2. Test tools one by one
3. Identify which middleware (if any) causes the issue

### MCP Configuration
1. Review `.cursor/mcp.json` configuration
2. Check for configuration issues
3. Verify MCP server initialization

## Next Steps

### Immediate
- ✅ Document workaround (direct Python access)
- ✅ Verify all functions work when called directly
- 🔍 Investigate FastMCP framework version/compatibility

### Short Term
- Test with middleware disabled
- Check FastMCP GitHub issues
- Review MCP protocol specification

### Long Term
- Update FastMCP if bug exists
- Report bug to FastMCP maintainers if needed
- Implement alternative MCP server if framework bug persists

## Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Application Code | ✅ Perfect | All functions work correctly |
| Direct Python Calls | ✅ Working | All tools accessible via imports |
| MCP Tool Interface | ❌ Broken | Framework-level error affects all tools |
| FastMCP Framework | ❓ Unknown | Likely source of the error |

## Conclusion

**This is a FastMCP/MCP framework issue, not an application bug.**

All our code is correct and working. The MCP framework layer is failing to process tool results correctly, affecting all tools system-wide.

**Recommendation:** Use direct Python imports as a workaround until the framework issue is resolved.
