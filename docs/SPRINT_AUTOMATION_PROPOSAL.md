# Sprint Automation Tool Proposal

**Date**: 2025-11-25  
**Status**: 📋 Proposal  
**Priority**: High

---

## Overview

Exarp currently has **partial** sprint automation capabilities but lacks a comprehensive tool to systematically process all background-capable tasks with minimal prompts. This proposal outlines a new `sprint_automation` tool that orchestrates existing tools to maximize autonomous task processing.

---

## Current State

### ✅ What Exarp Can Do (Partially)

1. **`batch_approve_tasks`** - Approves tasks in Review that don't need clarification
   - ✅ Filters by `clarification_none=True`
   - ✅ Moves from Review → Todo
   - ❌ Doesn't extract subtasks
   - ❌ Doesn't run tools systematically

2. **`nightly_task_automation`** - Filters background vs interactive tasks
   - ✅ Identifies background-capable tasks
   - ✅ Moves interactive tasks to Review
   - ✅ Batch approves research tasks
   - ❌ Doesn't extract subtasks
   - ❌ Doesn't run analysis tools

3. **`list_tasks_awaiting_clarification`** - Lists tasks needing input
   - ✅ Identifies tasks in Review
   - ✅ Shows clarification questions
   - ❌ Doesn't auto-resolve simple clarifications

4. **Task Analysis Tools** (can be orchestrated):
   - ✅ `check_documentation_health` - Docs analysis
   - ✅ `analyze_todo2_alignment` - Task alignment
   - ✅ `detect_duplicate_tasks` - Duplicate detection
   - ✅ `run_tests` - Test execution
   - ✅ `analyze_test_coverage` - Coverage analysis
   - ✅ `find_automation_opportunities` - Automation discovery

### ❌ What's Missing

1. **Subtask Extraction** - No tool to extract subtasks from parent tasks
2. **Systematic Processing** - No orchestration of all tools in sequence
3. **Auto-Resolution** - No intelligent resolution of simple clarifications
4. **Sprint Workflow** - No end-to-end sprint automation

---

## Proposed Solution: `sprint_automation` Tool

### Purpose

Systematically sprint through a project by:
1. Extracting all background-capable subtasks
2. Running all applicable analysis tools
3. Auto-approving tasks that don't need input
4. Processing tasks in priority order
5. Minimizing prompts and user interaction

### Parameters

- `max_iterations`: Maximum sprint iterations (default: `10`)
- `auto_approve`: Auto-approve tasks without clarification (default: `true`)
- `extract_subtasks`: Extract subtasks from parent tasks (default: `true`)
- `run_analysis_tools`: Run docs health, alignment, duplicates (default: `true`)
- `run_testing_tools`: Run tests and coverage (default: `true`)
- `priority_filter`: Only process high/medium/low priority (optional)
- `tag_filter`: Only process tasks with specific tags (optional)
- `dry_run`: Preview mode without making changes (default: `false`)

### Workflow

```
1. EXTRACT SUBTASKS
   ├─ Use agentic-tools MCP to list all tasks
   ├─ For each parent task, extract subtasks
   ├─ Filter subtasks: background-capable only
   └─ Add extracted subtasks to processing queue

2. AUTO-APPROVE SAFE TASKS
   ├─ List tasks in Review status
   ├─ Filter: no clarification needed
   ├─ Filter: research/implementation/testing tasks
   ├─ Auto-approve: Review → Todo
   └─ Add to processing queue

3. RUN ANALYSIS TOOLS (if enabled)
   ├─ check_documentation_health (create_tasks=false)
   ├─ analyze_todo2_alignment (create_followup_tasks=true)
   ├─ detect_duplicate_tasks (auto_fix=true)
   └─ find_automation_opportunities (min_value_score=0.8)

4. RUN TESTING TOOLS (if enabled)
   ├─ run_tests (coverage=true)
   ├─ analyze_test_coverage (min_coverage=80)
   └─ Create tasks for low-coverage files

5. PROCESS BACKGROUND TASKS
   ├─ Filter: background-capable tasks
   ├─ Sort by priority (high → medium → low)
   ├─ Process in batches (max 10 parallel)
   └─ Update status: Todo → In Progress → Done

6. IDENTIFY BLOCKERS
   ├─ List tasks still in Review
   ├─ Identify why blocked (clarification, design decision)
   ├─ Generate summary report
   └─ Suggest next actions
```

### Features

1. **Subtask Extraction**
   - Use agentic-tools MCP `list_subtasks()` to extract subtasks
   - Filter subtasks: background-capable only
   - Auto-create subtasks if parent task has "subtasks" in description

2. **Intelligent Auto-Approval**
   - Research tasks → Auto-approve (no clarification needed)
   - Implementation tasks → Auto-approve (if no design decisions)
   - Testing tasks → Auto-approve (if no configuration needed)
   - Design/Strategy tasks → Keep in Review (needs input)

3. **Systematic Tool Execution**
   - Run all applicable tools in optimal order
   - Use results from one tool to inform next tool
   - Create follow-up tasks automatically
   - Generate comprehensive sprint report

4. **Minimal Prompts**
   - Only prompt for critical decisions
   - Auto-resolve simple clarifications
   - Batch process similar tasks
   - Generate summary instead of individual prompts

---

## Implementation Plan

### Phase 1: Core Sprint Automation (Week 1)
- ✅ Create `sprint_automation` tool
- ✅ Integrate with agentic-tools MCP for subtask extraction
- ✅ Implement auto-approval logic
- ✅ Basic workflow orchestration

### Phase 2: Tool Integration (Week 2)
- ✅ Integrate all analysis tools
- ✅ Integrate testing tools
- ✅ Tool result aggregation
- ✅ Follow-up task creation

### Phase 3: Intelligence (Week 3)
- ✅ Smart clarification resolution
- ✅ Priority-based processing
- ✅ Blocker identification
- ✅ Sprint report generation

---

## Example Usage

```python
# Full sprint with all tools
sprint_automation(
    max_iterations=10,
    auto_approve=True,
    extract_subtasks=True,
    run_analysis_tools=True,
    run_testing_tools=True
)

# Quick sprint (analysis only)
sprint_automation(
    max_iterations=5,
    run_testing_tools=False
)

# Testing sprint
sprint_automation(
    max_iterations=3,
    run_analysis_tools=False,
    run_testing_tools=True,
    priority_filter="high"
)
```

---

## Integration with Existing Tools

### Uses Existing Tools
- `batch_approve_tasks` - For auto-approval
- `list_tasks_awaiting_clarification` - To identify blockers
- `resolve_task_clarification` - For simple clarifications
- `check_documentation_health` - Docs analysis
- `analyze_todo2_alignment` - Task alignment
- `detect_duplicate_tasks` - Duplicate detection
- `run_tests` - Test execution
- `analyze_test_coverage` - Coverage analysis
- `find_automation_opportunities` - Automation discovery

### Uses Agentic-Tools MCP
- `list_tasks` - Get all tasks
- `list_subtasks` - Extract subtasks
- `create_task` - Create follow-up tasks
- `update_task` - Update task status
- `get_task` - Get task details

---

## Benefits

1. **Maximizes Autonomous Processing** - Processes all background-capable tasks
2. **Minimizes Prompts** - Only asks for critical decisions
3. **Systematic Coverage** - Runs all applicable tools
4. **Subtask Extraction** - Breaks down complex tasks automatically
5. **Intelligent Filtering** - Only processes tasks that can proceed
6. **Comprehensive Reporting** - Full sprint summary with blockers

---

## Sprint Report Format

```markdown
# Sprint Automation Report

## Summary
- Subtasks Extracted: 15
- Tasks Auto-Approved: 8
- Tasks Processed: 23
- Tasks Completed: 18
- Blockers Identified: 5

## Analysis Results
- Documentation Health: 85/100
- Task Alignment: 12 misaligned tasks
- Duplicates Found: 3 (auto-fixed)
- Test Coverage: 78% (below 80% threshold)

## Blockers
1. T-123: Design decision needed (multi-service architecture)
2. T-124: User preference required (UI framework choice)
3. T-125: Clarification needed (API rate limits)

## Next Actions
- Review 5 blockers
- Address 12 misaligned tasks
- Improve test coverage (22% gap)
```

---

## Next Steps

1. **Create Todo2 task** for sprint automation implementation
2. **Implement Phase 1** (core automation)
3. **Test with existing project**
4. **Iterate based on feedback**

---

**Status**: Ready for implementation  
**Priority**: High (complements existing automation tools)

