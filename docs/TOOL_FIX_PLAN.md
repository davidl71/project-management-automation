# MCP Tool Fix Plan

**Date:** 2025-12-02  
**Purpose:** Fix invalid tools identified by validation to prevent FastMCP issues

---

## Summary

**Current Status:**
- ✅ 20 valid tools (87%)
- ❌ 3 invalid tools (13%)
- ⚠️  16 warnings

**Priority:**
1. **High:** Fix `run_automation` - Same pattern as `analyze_alignment` (already fixed)
2. **Medium:** Improve `recommend` - Add decorator and simplify
3. **Low:** Improve `dev_reload` - Add decorator (logic is acceptable)

---

## Fix 1: Split `run_automation` Tool (HIGH PRIORITY)

### Issue
- Has conditional logic based on `action` parameter
- Complex if/elif/else branches (2 if, 4 elif, 2 else)
- Missing `@ensure_json_string` decorator
- 70 lines long

### Solution
Split into 4 separate tools (following `analyze_alignment` pattern):

1. `run_daily_automation()` - Daily checks
2. `run_nightly_automation()` - Nightly task processing
3. `run_sprint_automation()` - Sprint automation
4. `run_discover_automation()` - Automation discovery

### Implementation Steps

#### Step 1: Create individual tool functions in server.py

Replace the unified `run_automation` tool (lines 1660-1718) with:

```python
@ensure_json_string
@mcp.tool()
def run_daily_automation(
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
    dry_run: bool = False,
    output_path: Optional[str] = None,
) -> str:
    """
    [HINT: Daily automation. Run daily checks (docs_health, alignment, duplicates, security).]
    
    Run daily automation checks including documentation health, task alignment,
    duplicate detection, and security scanning.
    
    📊 Output: Daily automation results
    🔧 Side Effects: Creates tasks and reports
    """
    return _run_daily_automation(tasks, include_slow, dry_run, output_path)

@ensure_json_string
@mcp.tool()
def run_nightly_automation(
    max_tasks_per_host: int = 5,
    max_parallel_tasks: int = 10,
    priority_filter: Optional[str] = None,
    tag_filter: Optional[list[str]] = None,
    dry_run: bool = False,
    notify: bool = False,
) -> str:
    """
    [HINT: Nightly automation. Process tasks automatically with host limits.]
    
    Process background-capable tasks automatically with host and parallel limits.
    
    📊 Output: Nightly automation results
    🔧 Side Effects: Processes tasks, sends notifications
    """
    result = _run_nightly_task_automation(
        max_tasks_per_host=max_tasks_per_host,
        max_parallel_tasks=max_parallel_tasks,
        priority_filter=priority_filter,
        tag_filter=tag_filter,
        dry_run=dry_run,
        notify=notify,
    )
    # Ensure JSON string return
    if isinstance(result, str):
        return result
    elif isinstance(result, dict):
        return json.dumps(result, indent=2)
    else:
        return json.dumps({"result": str(result)}, indent=2)

@ensure_json_string
@mcp.tool()
def run_sprint_automation(
    max_iterations: int = 10,
    auto_approve: bool = True,
    extract_subtasks: bool = True,
    run_analysis_tools: bool = True,
    run_testing_tools: bool = True,
    priority_filter: Optional[str] = None,
    tag_filter: Optional[list[str]] = None,
    dry_run: bool = False,
    output_path: Optional[str] = None,
    notify: bool = False,
) -> str:
    """
    [HINT: Sprint automation. Full sprint automation with subtask extraction.]
    
    Systematically process all background-capable tasks with minimal prompts.
    Extracts subtasks, auto-approves safe tasks, runs analysis/testing tools.
    
    📊 Output: Sprint automation results
    🔧 Side Effects: Creates tasks, extracts subtasks, runs tools
    """
    return _sprint_automation_impl(
        max_iterations, auto_approve, extract_subtasks,
        run_analysis_tools, run_testing_tools,
        priority_filter, tag_filter, dry_run, output_path, notify,
    )

@ensure_json_string
@mcp.tool()
def run_discover_automation(
    min_value_score: float = 0.7,
    output_path: Optional[str] = None,
) -> str:
    """
    [HINT: Discover automation. Find automation opportunities in codebase.]
    
    Discover automation opportunities in the codebase based on value score.
    
    📊 Output: Automation opportunities
    🔧 Side Effects: Creates discovery report
    """
    return _find_automation_opportunities(min_value_score, output_path)
```

#### Step 2: Update stdio server registration

Update the stdio server's `call_tool` function (around line 1551) to handle the new tool names:

```python
elif name == "run_daily_automation":
    result = _run_daily_automation(
        arguments.get("tasks"),
        arguments.get("include_slow", False),
        arguments.get("dry_run", False),
        arguments.get("output_path"),
    )
elif name == "run_nightly_automation":
    result = _run_nightly_task_automation(
        max_tasks_per_host=arguments.get("max_tasks_per_host", 5),
        max_parallel_tasks=arguments.get("max_parallel_tasks", 10),
        priority_filter=arguments.get("priority_filter"),
        tag_filter=arguments.get("tag_filter"),
        dry_run=arguments.get("dry_run", False),
        notify=arguments.get("notify", False),
    )
elif name == "run_sprint_automation":
    result = sprint_automation(
        max_iterations=arguments.get("max_iterations", 10),
        auto_approve=arguments.get("auto_approve", True),
        extract_subtasks=arguments.get("extract_subtasks", True),
        run_analysis_tools=arguments.get("run_analysis_tools", True),
        run_testing_tools=arguments.get("run_testing_tools", True),
        priority_filter=arguments.get("priority_filter"),
        tag_filter=arguments.get("tag_filter"),
        dry_run=arguments.get("dry_run", False),
        output_path=arguments.get("output_path"),
        notify=arguments.get("notify", False),
    )
elif name == "run_discover_automation":
    result = _find_automation_opportunities(
        arguments.get("min_value_score", 0.7),
        arguments.get("output_path"),
    )
```

#### Step 3: Update stdio server tool list

Update `list_tools()` function (around line 1177) to replace the single `run_automation` tool with 4 separate tools.

#### Step 4: Remove old unified tool

Delete the old `run_automation` function and `_sprint_automation_impl` helper.

#### Step 5: Update documentation

- Update `docs/TOOL_STATUS_TABLE.md`
- Document the split in a new file: `docs/RUN_AUTOMATION_SPLIT.md`

### Testing

1. Run validation: `python3 -m project_management_automation.utils.tool_validator`
2. Test each new tool individually
3. Verify old `run_automation` calls are updated

### Migration Notes

**Breaking Change:** The unified `run_automation(action="sprint")` will no longer exist.

**Update calls:**
- `run_automation(action="daily")` → `run_daily_automation()`
- `run_automation(action="nightly")` → `run_nightly_automation()`
- `run_automation(action="sprint")` → `run_sprint_automation()`
- `run_automation(action="discover")` → `run_discover_automation()`

---

## Fix 2: Improve `recommend` Tool (MEDIUM PRIORITY)

### Issue
- Complex conditional logic (3 if, 1 elif, 1 else)
- Missing `@ensure_json_string` decorator
- 106 lines long
- Logic is in underlying function (acceptable)

### Solution
Add decorator and simplify wrapper (logic in underlying function is fine).

### Implementation Steps

1. Add `@ensure_json_string` decorator before `@mcp.tool()`
2. Simplify wrapper to just pass through to underlying function
3. Move any remaining conditional logic to helper function

```python
@ensure_json_string
@mcp.tool()
def recommend(
    action: str = "model",
    # ... parameters ...
) -> str:
    """[HINT: Recommendations. action=model|workflow|advisor. Unified recommendation system.]"""
    return _recommend(
        action=action,
        # ... pass all parameters ...
    )
```

---

## Fix 3: Improve `dev_reload` Tool (LOW PRIORITY)

### Issue
- Complex conditional logic (3 if, 2 elif, 2 else)
- Missing `@ensure_json_string` decorator
- Logic is acceptable (environment checks are necessary)

### Solution
Add decorator (logic can stay as-is for environment checks).

### Implementation Steps

1. Add `@ensure_json_string` decorator before `@mcp.tool()`
2. Keep conditional logic (needed for dev mode check)

```python
@ensure_json_string
@mcp.tool()
def dev_reload(modules: Optional[list[str]] = None) -> str:
    """[HINT: Dev reload. Hot-reload modules without restart. Requires EXARP_DEV_MODE=1.]"""
    # Keep existing logic - environment checks are necessary
    ...
```

---

## Fix 4: Address Warnings (MEDIUM PRIORITY)

### Missing `@ensure_json_string` Decorators

Add to these tools:
- `dev_reload`
- `add_external_tool_hints`
- `run_automation` (will be split, so add to new tools)
- `discovery`
- `context`
- `recommend`
- `check_attribution`
- `lint`

### Simple Return Pattern

Tools to simplify:
- `dev_reload` - Keep logic (environment check needed)
- `check_attribution` - Simplify if possible

### Function Length

Tools to refactor:
- `memory_maint` (169 lines) - Move logic to helper functions
- `recommend` (106 lines) - Already addressed in Fix 2
- `context` (53 lines) - Consider splitting

---

## Implementation Order

1. **Fix 1: Split `run_automation`** (Critical - same issue as `analyze_alignment`)
2. **Fix 4: Add missing decorators** (Quick wins - prevents future issues)
3. **Fix 2: Improve `recommend`** (Medium - reduces complexity)
4. **Fix 3: Improve `dev_reload`** (Low - acceptable as-is)

---

## Validation Checklist

After each fix:

- [ ] Run validation: `python3 -m project_management_automation.utils.tool_validator`
- [ ] All invalid tools show as valid
- [ ] Warnings reduced
- [ ] Tests pass
- [ ] Manual tool testing works
- [ ] Documentation updated

---

## Expected Results

**After Fix 1 (run_automation split):**
- 20 valid tools → 23 valid tools
- 3 invalid tools → 2 invalid tools

**After Fix 2-4:**
- 23 valid tools → 23 valid tools
- 2 invalid tools → 0 invalid tools (or 1 if dev_reload stays as warning)
- Warnings reduced significantly

---

## Reference

- **Similar Fix:** See `docs/ANALYZE_ALIGNMENT_SPLIT.md` for pattern
- **Constraints:** See `docs/FASTMCP_TOOL_CONSTRAINTS.md`
- **Current Status:** See `docs/TOOL_VALIDATION_REPORT.md`

---

**Status:** 📋 Ready to implement  
**Estimated Time:** 2-3 hours  
**Risk Level:** Low (following proven pattern)

