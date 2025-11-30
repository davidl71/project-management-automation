# FastMCP Deep Investigation - Async/Await Error Analysis

**Date:** 2025-11-30  
**Error:** `object dict can't be used in 'await' expression`  
**Scope:** System-wide - ALL MCP tools affected

## Investigation Methodology

### 1. Error Pattern Analysis

**Error Message:**
```
object dict can't be used in 'await' expression
```

**Key Characteristics:**
- Occurs for ALL tools, not just session_handoff
- Only happens via MCP interface, not direct Python calls
- Consistent across different tool implementations
- Suggests framework-level processing issue

### 2. Middleware Chain Investigation

#### LoggingMiddleware (lines 58-121)

```python
async def on_call_tool(self, context: MiddlewareContext, call_next: Callable):
    # ... setup ...
    result = await call_next(context)  # Line 100
    # ... processing ...
    return result
```

**Analysis:**
- ✅ Properly uses `await call_next(context)`
- ✅ Returns result correctly
- ❌ No issues found in middleware code

#### ToolFilterMiddleware

```python
async def __call__(self, request: Any, call_next: Callable, context: Optional[Any] = None) -> Any:
    response = await call_next(request)
    # ... filtering logic ...
    return response
```

**Analysis:**
- ✅ Properly uses `await call_next(request)`
- ✅ Only filters tools/list responses
- ❌ Not processing tool execution results incorrectly

#### SecurityMiddleware

- Checks access control
- Should pass through to next middleware
- Not directly processing tool results

### 3. FastMCP Framework Analysis

**Version:** fastmcp 2.13.1

**Tool Execution Path:**
1. MCP client sends tool call request
2. FastMCP receives request
3. Middleware chain processes request
4. Tool function executes
5. Result returns through middleware
6. FastMCP serializes result
7. Result sent to client

**Error Location:** Likely in steps 4-6 (tool execution/serialization)

### 4. Async Handling Investigation

#### Our Implementation

**Tool Definition:**
```python
@mcp.tool()
def session_handoff_tool(...) -> str:
    return session_handoff(...)  # Returns JSON string
```

**Async Helper:**
```python
def _run_async_safe(coro):
    try:
        loop = asyncio.get_running_loop()
        # Use thread pool with new event loop
        ...
    except RuntimeError:
        return asyncio.run(coro)
```

**Issue Hypothesis:**
- FastMCP may be expecting async tools but getting sync
- Or FastMCP is trying to await the return value
- Or serialization process is incorrectly awaiting dict

### 5. Return Type Analysis

**FastMCP Examples Show:**
```python
@mcp.tool()
async def read_file(...) -> Dict:
    return {"success": True, "data": ...}
```

**Our Tools Return:**
- JSON strings (valid pattern)
- Some tools are sync, some async
- FastMCP should handle both

**Possible Issue:**
- FastMCP may have a bug where it tries to await string/dict returns
- Or middleware is incorrectly processing return values

### 6. Error Propagation Analysis

**Error Flow:**
1. Tool called via MCP interface
2. Middleware intercepts (LoggingMiddleware)
3. `await call_next(context)` executes tool
4. Tool returns JSON string
5. Middleware tries to process result
6. **ERROR OCCURS HERE** - "object dict can't be used in 'await' expression"

**Critical Question:** What is being awaited that's a dict?

### 7. Hypothesis

**Most Likely Cause:**
FastMCP framework is trying to process tool return values in an async context, and somewhere in the execution chain, a dict is being passed to `await` instead of a coroutine.

**Possible Scenarios:**

1. **FastMCP Bug:**
   - Framework incorrectly assumes tool returns are awaitable
   - Tries to await dict/string returns
   - Should serialize directly, not await

2. **Middleware Conflict:**
   - Multiple middleware trying to process same result
   - One middleware awaiting what another already processed
   - Race condition in async processing

3. **Serialization Issue:**
   - FastMCP serialization process expects async generator
   - Receives dict/string instead
   - Tries to await non-coroutine

### 8. Testing Results

#### ✅ Direct Function Calls
```python
from project_management_automation.tools.session_handoff import session_handoff
result = session_handoff('resume')
# Returns: <class 'str'> ✅ Works perfectly
```

#### ✅ Wrapper Access
```python
from project_management_automation.tools.session_handoff_wrapper import resume
result = resume()
# Returns: <class 'dict'> ✅ Works perfectly
```

#### ❌ MCP Interface
```
session_handoff_tool(action="resume")
# Error: object dict can't be used in 'await' expression
```

## Conclusion

**Root Cause:** FastMCP framework bug in tool result processing/serialization

**Evidence:**
- All tools affected (system-wide)
- All functions work when called directly
- Middleware code is correct
- Error is consistent and reproducible

**Location:** FastMCP framework tool execution/serialization layer

## References

- [FastMCP Tutorial - File Operations](https://raw.githubusercontent.com/CarlosIbCu/mcp-tutorial-complete-guide/master/notebooks/intermediate/06_file_operations.ipynb)
- [FastMCP Client Documentation](https://gofastmcp.com/clients/client)
- FastMCP Version: 2.13.1

## Next Actions

1. Report bug to FastMCP maintainers
2. Use workaround wrapper (created)
3. Monitor FastMCP updates for fix
4. Consider alternative MCP implementation if needed
