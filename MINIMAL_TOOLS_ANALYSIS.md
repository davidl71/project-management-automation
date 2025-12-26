# Minimal Tools Analysis - Simplified Execution Paths

**Date**: 2025-12-26  
**Goal**: Test tools with the simplest possible execution paths to isolate the issue

## Test Tools Created

7 minimal test tools with progressively simpler execution paths:

1. **`test_minimal_simple`** - Absolute simplest: `@mcp.tool()`, direct return
2. **`test_minimal_with_decorator`** - With `@ensure_json_string` decorator
3. **`test_minimal_json_string`** - Returns JSON string directly
4. **`test_minimal_decorator_json`** - Decorator + JSON string
5. **`test_minimal_underlying_call`** - Calls underlying function (like our tools)
6. **`test_minimal_dict_conversion`** - Converts dict to JSON string
7. **`test_batch_process`** - FastMCP example pattern (for comparison)

## Results

**ALL 7 minimal tools are BROKEN** - 100% failure rate

| Tool | Pattern | Status | Error |
|------|---------|--------|-------|
| `test_minimal_simple` | Simplest possible | ❌ BROKEN | `object dict can't be used in 'await' expression` |
| `test_minimal_with_decorator` | With decorator | ❌ BROKEN | `object dict can't be used in 'await' expression` |
| `test_minimal_json_string` | JSON string return | ❌ BROKEN | `object dict can't be used in 'await' expression` |
| `test_minimal_decorator_json` | Decorator + JSON | ❌ BROKEN | `object dict can't be used in 'await' expression` |
| `test_minimal_underlying_call` | Underlying function | ❌ BROKEN | `object dict can't be used in 'await' expression` |
| `test_minimal_dict_conversion` | Dict conversion | ❌ BROKEN | `object dict can't be used in 'await' expression` |
| `test_batch_process` | FastMCP example | ❌ BROKEN | `object dict can't be used in 'await' expression` |

## Key Findings

1. **Even the simplest possible tool fails** - No decorators, no function calls, just `return "string"`
2. **Decorators don't matter** - Tools with and without `@ensure_json_string` both fail
3. **Return type doesn't matter** - Plain strings and JSON strings both fail
4. **Function calls don't matter** - Direct returns and function calls both fail
5. **FastMCP example pattern fails** - Even the exact pattern from FastMCP examples fails

## Conclusion

**The issue is NOT in our code execution path.** Even the absolute simplest possible tool fails. This confirms:

- ✅ The bug is in FastMCP's framework itself
- ✅ It's not related to our decorators, function calls, or return types
- ✅ It's a fundamental issue with how FastMCP processes tool results
- ✅ No amount of code simplification will fix it

## Impact

This proves the bug is **completely in FastMCP's framework**, not in our application code. The workaround (`EXARP_FORCE_STDIO=1`) is the only solution until FastMCP fixes the framework bug.

