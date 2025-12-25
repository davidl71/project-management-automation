# Tool Consolidation Analysis

**Date**: 2025-12-25  
**Current Count**: 36 tools (6 over limit)  
**Target**: ≤30 tools  
**Need to Save**: 6+ tools

---

## Current Tool Breakdown

### Already Consolidated (16 tools)
✅ These use `action=` parameter pattern:
- `task_analysis` (5 actions: duplicates|tags|hierarchy|dependencies|parallelization)
- `testing` (4 actions: run|coverage|suggest|validate)
- `security` (3 actions: scan|alerts|report)
- `health` (5 actions: server|git|docs|dod|cicd)
- `lint` (2 actions: run|analyze)
- `memory` (3 actions: save|recall|search)
- `memory_maint` (5 actions: health|gc|prune|consolidate|dream)
- `task_discovery` (4 actions: comments|markdown|orphans|all)
- `task_workflow` (3 actions: sync|approve|clarify)
- `context` (3 actions: summarize|budget|batch)
- `tool_catalog` (2 actions: list|help)
- `workflow_mode` (3 actions: focus|suggest|stats)
- `recommend` (3 actions: model|workflow|advisor)
- `prompt_tracking` (2 actions: log|analyze)
- `generate_config` (3 actions: rules|ignore|simplify)
- `setup_hooks` (2 actions: git|patterns)

**Total**: 16 consolidated tools

### Individual Tools That Need Consolidation (20 tools)

#### Priority 1: High-Impact Consolidations

##### 1. Automation Tools (4→1) - **SAVE 3 TOOLS**
**Current**: 
- `run_daily_automation`
- `run_nightly_automation`
- `run_sprint_automation`
- `run_discover_automation`

**Proposed**: `automation(action=daily|nightly|sprint|discover)`
```python
@mcp.tool()
def automation(
    action: str = "daily",
    tasks: Optional[list[str]] = None,
    include_slow: bool = False,
    dry_run: bool = False,
    output_path: Optional[str] = None,
    # ... other params
) -> str:
    """
    Unified automation tool.
    
    Actions:
    - daily: Run daily maintenance tasks
    - nightly: Process tasks automatically
    - sprint: Full sprint automation
    - discover: Find automation opportunities
    """
```

**Savings**: 3 tools

---

##### 2. Estimation Tools (3→1) - **SAVE 2 TOOLS**
**Current**:
- `estimate_task_duration`
- `analyze_estimation_accuracy`
- `get_estimation_statistics`

**Proposed**: `estimation(action=estimate|analyze|stats)`
```python
@mcp.tool()
def estimation(
    action: str = "estimate",
    name: Optional[str] = None,
    details: Optional[str] = None,
    # ... params for each action
) -> str:
    """
    Unified task duration estimation tool.
    
    Actions:
    - estimate: Generate MLX-enhanced time estimate
    - analyze: Analyze estimation accuracy from historical data
    - stats: Get estimation statistics and patterns
    """
```

**Savings**: 2 tools

---

##### 3. Git-Inspired Task Tools (8→1) - **SAVE 7 TOOLS**
**Current**:
- `get_task_commits_tool`
- `get_branch_commits_tool`
- `list_branches_tool`
- `get_branch_tasks_tool`
- `set_task_branch`
- `merge_branch_tools_tool`
- `compare_task_diff_tool`
- `generate_graph_tool`

**Proposed**: `git_tasks(action=commits|branches|set_branch|merge|diff|graph)`
```python
@mcp.tool()
def git_tasks(
    action: str = "commits",
    task_id: Optional[str] = None,
    branch: Optional[str] = None,
    # ... params for each action
) -> str:
    """
    Unified git-inspired task management tool.
    
    Actions:
    - commits: Get commit history for task/branch
    - branches: List or get tasks for branches
    - set_branch: Set task branch association
    - merge: Merge branch tasks
    - diff: Compare task changes
    - graph: Generate task dependency graph
    """
```

**Savings**: 7 tools

---

##### 4. Alignment Tools (2→1) - **SAVE 1 TOOL**
**Current**:
- `analyze_todo2_alignment`
- `analyze_prd_alignment`

**Note**: There's an `analyze_alignment` function in consolidated.py, but these are registered separately!

**Proposed**: Consolidate into single `alignment` tool
- Already exists in consolidated.py but not used in server.py

**Savings**: 1 tool

---

##### 5. Task Management Extras (2→1) - **SAVE 1 TOOL**
**Current**:
- `improve_task_clarity`
- `cleanup_stale_tasks`

**Proposed**: Add to `task_workflow` or `task_analysis`
- Option A: Add to `task_workflow(action=clarity|cleanup|...)`
- Option B: Add to `task_analysis(action=clarity|cleanup|...)`

**Recommendation**: Add to `task_workflow` since both are workflow operations

**Savings**: 1 tool

---

##### 6. Remaining Individual Tools (6 tools)

**Low Priority** (infrequently used or specific-purpose):
- `add_external_tool_hints` - One-time setup tool
- `check_attribution` - Specific compliance check
- Could remain as-is (used infrequently)

**Could Consolidate**:
- Consider if any fit into existing consolidated tools

---

## Recommended Consolidation Plan

### Phase 1: Quick Wins (Immediate - 7 tools saved)

1. ✅ **Automation Tools** (4→1): Save 3 tools
2. ✅ **Estimation Tools** (3→1): Save 2 tools  
3. ✅ **Alignment Tools** (2→1): Save 1 tool (fix registration)
4. ✅ **Task Extras** (2→1): Save 1 tool (add to task_workflow)

**Result**: 36 → 29 tools (1 under limit) ✅

---

### Phase 2: Major Consolidation (Optional - 7 more tools saved)

5. ✅ **Git-Inspired Tools** (8→1): Save 7 tools

**Result**: 29 → 22 tools (8 under limit) ✅✅

---

## Implementation Priority

### Immediate Action (Phase 1)
**Priority**: HIGH - Gets us under limit immediately

**Effort**: Low-Medium
- Follow existing consolidated.py pattern
- Add actions to existing tools or create new consolidated tool
- Update server.py registrations

**Estimated Time**: 2-4 hours

### Optional Enhancement (Phase 2)
**Priority**: MEDIUM - Nice to have, but not critical

**Effort**: Medium
- More complex consolidation (8 tools → 1)
- Requires careful parameter handling

**Estimated Time**: 3-5 hours

---

## Summary

| Category | Current | After Phase 1 | After Phase 2 |
|----------|---------|---------------|---------------|
| Total Tools | 36 | 29 | 22 |
| Over/Under Limit | +6 | -1 ✅ | -8 ✅✅ |
| Savings | - | 7 tools | 14 tools |

**Recommendation**: Implement Phase 1 immediately to get under limit. Phase 2 can be done later if needed.

---

## Next Steps

1. Create `automation()` consolidated tool (4→1)
2. Create `estimation()` consolidated tool (3→1)
3. Fix `analyze_alignment` registration (2→1)
4. Add clarity/cleanup actions to `task_workflow` (2→1)
5. Test all consolidated tools
6. Update PROJECT_GOALS.md with new count

