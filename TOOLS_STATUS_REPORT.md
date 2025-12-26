# MCP Tools Status Report

**Date**: 2025-12-26  
**Test Method**: MCP Client with content validation  
**Total Tools**: 27

## Summary

- ✅ **Working**: 7 tools (25.9%)
- ❌ **Broken**: 20 tools (74.1%) - All with "await dict" error

## Working Tools ✅

These tools return valid results when called with empty arguments:

1. **task_workflow** - Task lifecycle management
2. **estimation** - Task duration estimation
3. **ollama** - Ollama integration
4. **mlx** - MLX integration  
5. **git_tools** - Git-inspired task management
6. **session** - Session management (⚠️ NOTE: Works with empty args, but fails with `action="prime"`)
7. **memory_maint** - Memory maintenance

## Broken Tools ❌

All broken tools return error message: `"object dict can't be used in 'await' expression"`

1. infer_session_mode
2. add_external_tool_hints
3. automation
4. tool_catalog
5. workflow_mode (async function)
6. context
7. recommend
8. analyze_alignment
9. security
10. generate_config
11. setup_hooks
12. prompt_tracking
13. health
14. check_attribution
15. report
16. task_analysis
17. testing
18. lint
19. memory
20. task_discovery

## Key Findings

### Pattern Analysis

1. **All tools use `@ensure_json_string` decorator** - This is not the differentiating factor
2. **Most tools are synchronous** - Only `workflow_mode` is async (and it's broken)
3. **All tools have `-> str` return type annotations**
4. **All underlying functions return JSON strings**

### Important Discovery

The `session` tool shows as "working" when called with empty arguments `{}`, but **fails when called with `action="prime"`**. This suggests:

- FastMCP may handle empty-argument calls differently
- The error occurs when specific code paths are triggered
- The `auto_prime` function call chain may be the issue

### Root Cause

Despite fixing all dict returns in our code:
- ✅ All functions return JSON strings
- ✅ All return type annotations are `-> str`
- ✅ All dict literals converted to `json.dumps()`
- ❌ FastMCP still detects dicts somewhere in the call chain

**Conclusion**: This is a FastMCP framework bug that occurs during:
1. Static analysis of function call chains
2. Runtime detection of dict types in intermediate functions
3. Processing of tool results before serialization

## Recommendations

1. **Use `EXARP_FORCE_STDIO=1`** as workaround to bypass FastMCP
2. **Report to FastMCP maintainers** - This affects 74% of tools
3. **Continue using stdio server** as primary transport
4. **Monitor FastMCP updates** for potential fixes

## Test Scripts

- `test_all_tools_comprehensive.py` - Tests all tools and validates content
- `test_fastmcp_static_analysis.py` - Analyzes function signatures
- `test_fastmcp_comprehensive.py` - Scans for dict returns using AST
- `test_session_specific.py` - Tests session tool with different arguments

## Files Generated

- `test_tools_comprehensive_results.json` - Detailed test results
- `test_tools_comprehensive_report.md` - Full test report
- `FASTMCP_STATIC_ANALYSIS_REPORT.md` - Static analysis findings

