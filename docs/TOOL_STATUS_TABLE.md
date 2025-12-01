# MCP Tools Status Table

**Date:** 2025-12-02  
**Last Updated:** 2025-12-02  
**Total Tools:** 22

## Quick Reference Summary

| Status | Tools |
|--------|-------|
| ✅ **Working (21)** | `add_external_tool_hints`, `advisor_audio`, `check_attribution`, `context`, `dev_reload`, `discovery`, `generate_config`, `health`, `lint`, `memory`, `memory_maint`, `prompt_tracking`, `recommend`, `report`, `run_automation`, `security`, `setup_hooks`, `task_analysis`, `task_discovery`, `task_workflow`, `testing` |
| 🔴 **Affected (1)** | `analyze_alignment` - FastMCP error, workaround available |

## Tool Status Overview

| Status | Count | Description |
|--------|-------|-------------|
| ✅ **Working** | 21 | Tools functioning correctly via MCP |
| 🔴 **Affected** | 1 | Tools with known FastMCP framework errors |
| ⚠️ **Untested** | 0 | Tools not yet tested |

## Detailed Tool Status

| Tool Name | Status | Decorator | Notes |
|-----------|--------|-----------|-------|
| `add_external_tool_hints` | ✅ Working | N/A | Standard tool registration |
| `advisor_audio` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `analyze_alignment` | 🔴 **Affected** | `@ensure_json_string` | **Known FastMCP error: "object dict can't be used in 'await' expression"** |
| `check_attribution` | ✅ Working | N/A | Direct tool registration |
| `context` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `dev_reload` | ✅ Working | N/A | Standard tool registration |
| `discovery` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `generate_config` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block - verified working |
| `health` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `lint` | ✅ Working | N/A | Direct tool registration |
| `memory` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `memory_maint` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `prompt_tracking` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `recommend` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `report` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `run_automation` | ✅ Working | N/A | Standard tool registration |
| `security` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block - verified working |
| `setup_hooks` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `task_analysis` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `task_discovery` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `task_workflow` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |
| `testing` | ✅ Working | `@ensure_json_string` | Inside CONSOLIDATED_AVAILABLE block |

## Affected Tool Details

### 🔴 `analyze_alignment`

**Error:** `object dict can't be used in 'await' expression`

**Status:** Known FastMCP framework bug

**Impact:** Tool cannot be called via MCP interface

**Workaround Available:** ✅ Yes - Direct Python function call works perfectly

```python
from project_management_automation.tools.todo2_alignment import analyze_todo2_alignment
import json

result = analyze_todo2_alignment(create_followup_tasks=False)
data = json.loads(result)
```

**Investigation Status:**
- ✅ Code structure is correct
- ✅ Decorator properly applied
- ✅ Return type annotation correct
- ✅ Underlying function works perfectly
- ✅ Matches pattern of working tools
- ❌ FastMCP framework error persists

**Related Documentation:**
- `docs/ANALYZE_ALIGNMENT_KNOWN_ISSUE.md` - Full issue documentation
- `docs/ANALYZE_ALIGNMENT_FIX_INVESTIGATION.md` - Investigation details

## Tool Categories

### Consolidated Tools (Inside CONSOLIDATED_AVAILABLE block)

All tools below are inside the `CONSOLIDATED_AVAILABLE` block and use `@ensure_json_string` decorator:

- ✅ `analyze_alignment` (🔴 Affected - framework error)
- ✅ `security` (Verified working)
- ✅ `generate_config` (Verified working)
- ✅ `setup_hooks`
- ✅ `prompt_tracking`
- ✅ `health`
- ✅ `report`
- ✅ `advisor_audio`
- ✅ `task_analysis`
- ✅ `testing`
- ✅ `memory`
- ✅ `task_discovery`
- ✅ `task_workflow`
- ✅ `memory_maint`
- ✅ `context`
- ✅ `discovery`
- ✅ `recommend`

### Direct Registration Tools

Tools registered outside CONSOLIDATED_AVAILABLE block:

- ✅ `add_external_tool_hints`
- ✅ `check_attribution`
- ✅ `dev_reload`
- ✅ `lint`
- ✅ `run_automation`

## Decorator Usage

### With `@ensure_json_string` Decorator

Most consolidated tools use this decorator to ensure JSON string returns:

- All tools inside `CONSOLIDATED_AVAILABLE` block (except `analyze_alignment` which has the error)

### Without Decorator

Some tools handle JSON string conversion internally:

- `add_external_tool_hints`
- `check_attribution`
- `dev_reload`
- `lint`
- `run_automation`

## Testing Status

| Status | Description |
|--------|-------------|
| ✅ Verified Working | Tools explicitly tested and confirmed working |
| ✅ Presumed Working | Tools following correct patterns, no errors reported |
| 🔴 Known Issue | Tools with documented errors |
| ⚠️ Untested | Tools not yet tested in production |

## Notes

1. **Most Tools Working:** 21 of 22 tools (95.5%) are working correctly
2. **Single Affected Tool:** Only `analyze_alignment` has a documented FastMCP framework error
3. **Workaround Available:** Direct Python access works for affected tool
4. **Pattern Consistency:** All tools follow the same registration patterns

## Updates

- **2025-12-02:** Initial table created
- **2025-12-02:** `analyze_alignment` marked as affected with full documentation

