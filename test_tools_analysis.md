# MCP Tools Test Results Analysis

**Date**: 2025-12-26  
**Total Tools**: 27  
**Test Method**: MCP Client via stdio

## Summary

- ❌ **All tools are broken** (100% failure rate)
- 🔴 **20 tools**: FastMCP "await dict" error
- 🟡 **7 tools**: FastMCP "to_mcp_result" error

## Error Types

### Error Type 1: "object dict can't be used in 'await' expression" (20 tools)

**Affected Tools:**
1. `infer_session_mode`
2. `add_external_tool_hints`
3. `automation`
4. `tool_catalog`
5. `workflow_mode`
6. `context`
7. `recommend`
8. `analyze_alignment`
9. `security`
10. `generate_config`
11. `setup_hooks`
12. `prompt_tracking`
13. `health`
14. `check_attribution`
15. `report`
16. `task_analysis`
17. `testing`
18. `lint`
19. `memory`
20. `task_discovery`

**Error Message:**
```
object dict can't be used in 'await' expression
```

**Root Cause:**
FastMCP framework is trying to await a dict value instead of a coroutine. This happens during FastMCP's internal processing of tool return values.

### Error Type 2: "'dict' object has no attribute 'to_mcp_result'" (7 tools)

**Affected Tools:**
1. `task_workflow`
2. `estimation`
3. `ollama`
4. `mlx`
5. `git_tools`
6. `session`
7. `memory_maint`

**Error Message:**
```
'dict' object has no attribute 'to_mcp_result'
```

**Root Cause:**
FastMCP is trying to call `.to_mcp_result()` on a dict, expecting a different return type format. This suggests FastMCP expects a specific result object type, not a plain dict or string.

## Pattern Analysis

### Common Characteristics of Broken Tools

1. **All use `@ensure_json_string` decorator** - The decorator should convert dicts to JSON strings, but FastMCP is still seeing dicts
2. **All return `-> str` type annotation** - Type annotations are correct
3. **All work when called directly** - Functions return correct JSON strings when bypassing MCP

### Why Some Tools Show Different Errors

The "to_mcp_result" error suggests FastMCP is getting further in the processing pipeline before failing. This might indicate:
- These tools' return values are being processed differently
- FastMCP's serialization layer is encountering the dict at a different stage
- There might be a difference in how these tools are registered

## Root Cause Hypothesis

**FastMCP Framework Bug:**
FastMCP is doing static analysis or runtime type checking that incorrectly detects dict return types, even though:
1. All functions return JSON strings at runtime
2. All type annotations are `-> str`
3. The `@ensure_json_string` decorator should handle conversion
4. Direct function calls work perfectly

**Possible FastMCP Issues:**
1. Static analysis incorrectly inferring return types
2. Decorator not being applied correctly in FastMCP's tool registry
3. FastMCP expecting a different return format (like a Result object)
4. Middleware or serialization layer incorrectly processing returns

## Verification

### Direct Function Calls (All Work ✅)

```python
from project_management_automation.tools.consolidated import session
result = session(action='prime')
# Returns: <class 'str'> (valid JSON, length: 2455)
```

### MCP Client Calls (All Fail ❌)

```python
result = await session.call_tool("session", {"action": "prime"})
# Error: 'dict' object has no attribute 'to_mcp_result'
# OR: object dict can't be used in 'await' expression
```

## Recommendations

1. **Investigate FastMCP Version**: Check if there's a newer version that fixes this
2. **Check FastMCP Documentation**: Look for proper return type format requirements
3. **Try Different Return Format**: Maybe FastMCP expects a Result object, not a string
4. **Use Stdio Server**: As a workaround, use `EXARP_FORCE_STDIO=1` to bypass FastMCP
5. **Report to FastMCP**: This appears to be a framework bug affecting all tools

## Next Steps

1. Check FastMCP version and update if available
2. Review FastMCP examples to see expected return format
3. Test with stdio server to confirm it's a FastMCP-specific issue
4. Consider creating a FastMCP issue/PR if this is confirmed as a bug

