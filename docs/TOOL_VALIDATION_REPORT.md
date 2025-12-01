# Tool Validation Report

## Summary

- **Total Tools:** 26
- **Valid Tools:** 25
- **Invalid Tools:** 1
- **Warnings:** 7

## Validation Rules

1. ✅ No conditional logic based on 'action' parameter
2. ✅ Simple return pattern (direct call to underlying function)
3. ✅ @ensure_json_string decorator applied
4. ✅ Minimal conditional logic (< 3 if/elif branches)
5. ✅ Function length < 50 lines

## ❌ Invalid Tools

### dev_reload (line 682)

- ❌ Tool has complex conditional logic (3 if, 2 elif, 2 else). FastMCP may have issues with complex control flow.

## ⚠️  Warnings

- ⚠️  **dev_reload**: Tool does not follow simple return pattern. Consider simplifying to: return _underlying_function(...)
- ⚠️  **run_nightly_automation**: Tool does not follow simple return pattern. Consider simplifying to: return _underlying_function(...)
- ⚠️  **context**: Tool function is long (53 lines). Consider moving logic to helper functions.
- ⚠️  **recommend**: Tool does not follow simple return pattern. Consider simplifying to: return _underlying_function(...)
- ⚠️  **recommend**: Tool function is long (97 lines). Consider moving logic to helper functions.
- ⚠️  **check_attribution**: Tool does not follow simple return pattern. Consider simplifying to: return _underlying_function(...)
- ⚠️  **memory_maint**: Tool function is long (169 lines). Consider moving logic to helper functions.

## ✅ Valid Tools

- ✅ add_external_tool_hints
- ✅ advisor_audio
- ✅ analyze_prd_alignment
- ✅ analyze_todo2_alignment
- ✅ check_attribution
- ✅ context
- ✅ discovery
- ✅ generate_config
- ✅ health
- ✅ lint
- ✅ memory
- ✅ memory_maint
- ✅ prompt_tracking
- ✅ recommend
- ✅ report
- ✅ run_daily_automation
- ✅ run_discover_automation
- ✅ run_nightly_automation
- ✅ run_sprint_automation
- ✅ security
- ✅ setup_hooks
- ✅ task_analysis
- ✅ task_discovery
- ✅ task_workflow
- ✅ testing
