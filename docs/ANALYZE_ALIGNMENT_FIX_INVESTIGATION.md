# Analyze Alignment Tool Fix Investigation


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date:** 2025-12-02  
**Issue:** FastMCP error: "object dict can't be used in 'await' expression"  
**Status:** 🔄 Investigation in progress

## Problem

The `analyze_alignment` MCP tool fails with FastMCP error:
```
object dict can't be used in 'await' expression
```

## Investigation Summary

### Code Analysis

1. **Tool Registration** (✅ Correct)
   - Location: `project_management_automation/server.py:2086-2140`
   - Has `@ensure_json_string` decorator (before `@mcp.tool()`)
   - Returns `-> str` type annotation
   - Calls underlying functions that return JSON strings

2. **Underlying Functions** (✅ Working)
   - `_analyze_todo2_alignment()` - Returns JSON string ✅
   - Direct Python testing confirms it works correctly
   - All tests pass: returns valid JSON string

3. **Comparison with Working Tools**
   - Same pattern as `security`, `generate_config` tools
   - Same decorator usage
   - Same return type annotation

### Fixes Applied

1. **Initial Fix** (Applied)
   - Added `@ensure_json_string` decorator
   - Simplified function body (removed redundant JSON conversion)

2. **Enhanced Fix** (Applied - Current)
   - Added explicit `wrap_tool_result()` call inside function
   - Defense in depth: both decorator + explicit wrapping
   - Fallback handling if wrapper not available

### Current Status

- ✅ Code structure is correct
- ✅ Underlying functions work perfectly
- ✅ Decorators properly applied
- ❌ FastMCP error persists after multiple restarts

### Possible Root Causes

1. **FastMCP Framework Issue**
   - Framework bug in async/await handling
   - Caching issue with tool registration
   - Middleware interference

2. **Tool Registration Timing**
   - Tool registered outside `CONSOLIDATED_AVAILABLE` block
   - May conflict with consolidated tools registration

3. **Async Version Conflict**
   - Async version exists in `consolidated.py` (returns dict)
   - FastMCP might be detecting/using wrong version

### Next Steps

1. ✅ Explicit result wrapping added (current state)
2. ⏳ Test after server restart
3. ⏳ Check if moving tool inside `CONSOLIDATED_AVAILABLE` block helps
4. ⏳ Investigate FastMCP middleware for interference
5. ⏳ Check server logs for registration errors

## Current Implementation

```python
@ensure_json_string  # Decorator ensures JSON string
@mcp.tool()
def analyze_alignment(...) -> str:
    try:
        result = _analyze_todo2_alignment(...)  # Returns JSON string
        # Explicit wrapping for defense in depth
        return wrap_tool_result(result)
    except Exception as e:
        return wrap_tool_result({"success": False, "error": str(e)})
```

## Workaround

If MCP tool continues to fail, use direct Python access:

```python
from project_management_automation.tools.todo2_alignment import analyze_todo2_alignment
import json

result = analyze_todo2_alignment(create_followup_tasks=False)
data = json.loads(result)
```

## Files Modified

- `project_management_automation/server.py` (lines 2084-2140)

