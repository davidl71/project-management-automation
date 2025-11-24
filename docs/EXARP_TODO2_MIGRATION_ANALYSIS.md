# Exarp Todo2 Migration Analysis

**Date**: 2025-01-27
**Status**: Analysis Complete
**Purpose**: Identify Todo2 tasks that should be moved to Exarp repository

---

## Overview

After splitting `project-management-automation` into a separate **Exarp** repository, we need to identify any Todo2 tasks in the main repository that are related to Exarp development and should be moved to the Exarp repository's Todo2 system.

---

## Analysis Results

### Tasks Found

**Total Exarp-Related Tasks**: 5 tasks (all part of tool reuse refactoring)

#### Task T-1: Refactor sync_todo_tasks_tool
- **ID**: `T-1`
- **Status**: Todo
- **Priority**: high
- **Content**: "Refactor sync_todo_tasks_tool to sync_tasks_tool with adapter pattern support"
- **Tags**: `refactor`, `adapter-pattern`, `tool-reuse`, `high-priority`
- **Category**: Exarp tool refactoring

**Analysis**: This task is about refactoring an Exarp tool (`sync_todo_tasks_tool`) to support an adapter pattern. Since Exarp is now a separate repository, this refactoring work should be tracked in the Exarp repository.

**Recommendation**: ✅ **Move to Exarp repository**

---

#### Task T-2: Create TaskSourceAdapter and TaskTargetAdapter
- **ID**: `T-2`
- **Status**: Todo
- **Priority**: high
- **Content**: "Create TaskSourceAdapter and TaskTargetAdapter base classes"
- **Tags**: `adapter-pattern`, `architecture`, `tool-reuse`
- **Category**: Exarp architecture refactoring

**Analysis**: This task is about creating adapter base classes for Exarp's tool architecture. This is core Exarp development work.

**Recommendation**: ✅ **Move to Exarp repository**

---

#### Task T-3: Extend detect_duplicate_tasks_tool
- **ID**: `T-3`
- **Status**: Todo
- **Priority**: high
- **Content**: "Extend detect_duplicate_tasks_tool to support multiple sources"
- **Tags**: `refactor`, `adapter-pattern`, `tool-reuse`
- **Category**: Exarp tool enhancement

**Analysis**: This task is about extending an Exarp tool to support multiple sources. This is Exarp development work.

**Recommendation**: ✅ **Move to Exarp repository**

---

#### Task T-4: Refactor analyze_todo2_alignment_tool
- **ID**: `T-4`
- **Status**: Todo
- **Priority**: high
- **Content**: "Refactor analyze_todo2_alignment_tool to analyze_task_alignment_tool with source parameter"
- **Tags**: `refactor`, `adapter-pattern`, `tool-reuse`
- **Category**: Exarp tool refactoring

**Analysis**: This task is about refactoring an Exarp tool (`analyze_todo2_alignment_tool`). Since Exarp is now a separate repository, this refactoring work should be tracked in the Exarp repository.

**Recommendation**: ✅ **Move to Exarp repository**

---

#### Task T-5: Extend simplify_rules_tool
- **ID**: `T-5`
- **Status**: Todo
- **Priority**: medium
- **Content**: "Extend simplify_rules_tool to support Cursor rules (.cursorrules)"
- **Tags**: `refactor`, `cursor-integration`, `tool-reuse`
- **Category**: Exarp tool enhancement

**Analysis**: This task is about extending an Exarp tool (`simplify_rules_tool`) to support Cursor rules. This is Exarp development work.

**Recommendation**: ✅ **Move to Exarp repository**

---

**Note**: Task T-11 was initially identified but appears to be part of a different set. All 5 tasks (T-1 through T-5) are part of the tool reuse refactoring effort documented in `EXARP_TOOL_REUSE_ANALYSIS.md`.

---

### Tasks NOT to Move

#### Automation Execution Tasks (AUTO-*)
- **IDs**: `AUTO-20251124195801`, `AUTO-20251124200259`
- **Status**: done
- **Content**: "Automated Shared TODO Table Synchronization execution"
- **Tags**: `automation`, `shared-todo-table-synchronization`

**Analysis**: These are execution logs from Exarp tools running in this repository. They document automation runs, not Exarp development work.

**Recommendation**: ❌ **Keep in main repository** (they're about using Exarp, not developing it)

---

## Migration Strategy

### Option 1: Manual Migration (Recommended)

**Steps**:
1. Export tasks T-4 and T-11 from main repository
2. Import into Exarp repository's `.todo2/state.todo2.json`
3. Update task IDs to match Exarp's ID scheme (if different)
4. Remove from main repository

**Pros**:
- Clean separation
- Tasks tracked where they belong
- Clear ownership

**Cons**:
- Manual work required
- Need to coordinate between repositories

---

### Option 2: Keep in Main Repository (Not Recommended)

**Rationale**: These tasks are about refactoring tools that are used in this repository, so they could stay here.

**Pros**:
- No migration needed
- Tasks stay in context where they're used

**Cons**:
- Exarp development tracked in wrong repository
- Confusion about where Exarp work happens
- Harder to manage Exarp as independent project

---

## Recommended Actions

### Immediate Actions

1. ✅ **Export Tasks T-4 and T-11**
   - Save task details (content, tags, priority, status)
   - Note any dependencies

2. ✅ **Create Tasks in Exarp Repository**
   - Add T-4 and T-11 to Exarp's `.todo2/state.todo2.json`
   - Update task IDs if needed (e.g., `EXARP-1`, `EXARP-2`)
   - Preserve all metadata (tags, priority, status)

3. ✅ **Remove from Main Repository**
   - Delete T-4 and T-11 from main repository's `.todo2/state.todo2.json`
   - Update any dependencies that reference these tasks

---

## Task Details for Migration

### All Tasks (T-1 through T-5)

All 5 tasks are part of the **Tool Reuse Refactoring** effort documented in:
- `docs/EXARP_TOOL_REUSE_ANALYSIS.md` - Complete analysis
- Related to adapter pattern implementation for Exarp tools

**Common Characteristics**:
- All have `tool-reuse` or `adapter-pattern` tags
- All are about refactoring/extending Exarp tools
- All should be tracked in Exarp repository

**Task List**:
1. **T-1**: Refactor sync_todo_tasks_tool → sync_tasks_tool (adapter pattern)
2. **T-2**: Create TaskSourceAdapter and TaskTargetAdapter base classes
3. **T-3**: Extend detect_duplicate_tasks_tool (multi-source support)
4. **T-4**: Refactor analyze_todo2_alignment_tool → analyze_task_alignment_tool
5. **T-5**: Extend simplify_rules_tool (Cursor rules support)

---

## Related Tasks

### Tool Reuse Refactoring Tasks

These tasks (T-4, T-11, and others) are part of a larger refactoring effort documented in:
- `docs/EXARP_TOOL_REUSE_ANALYSIS.md` - Analysis of tool reuse opportunities
- `docs/EXARP_CLEANUP_COMPLETE.md` - Cleanup summary

**All tool reuse refactoring tasks should be moved to Exarp repository** since they're about Exarp's internal architecture.

---

## Verification

### After Migration

1. ✅ Verify tasks exist in Exarp repository
2. ✅ Verify tasks removed from main repository
3. ✅ Verify no broken dependencies
4. ✅ Verify task IDs are unique in Exarp repository

---

## Summary

### Tasks to Move (5)

| Task ID | Description | Reason |
|---------|-------------|--------|
| **T-1** | Refactor sync_todo_tasks_tool to sync_tasks_tool | Exarp tool refactoring (adapter pattern) |
| **T-2** | Create TaskSourceAdapter and TaskTargetAdapter | Exarp architecture (adapter pattern) |
| **T-3** | Extend detect_duplicate_tasks_tool | Exarp tool enhancement (multi-source) |
| **T-4** | Refactor analyze_todo2_alignment_tool | Exarp tool refactoring (adapter pattern) |
| **T-5** | Extend simplify_rules_tool | Exarp tool enhancement (Cursor rules) |

### Tasks to Keep (2)

| Task ID | Description | Reason |
|---------|-------------|--------|
| **AUTO-20251124195801** | Automation execution log | Using Exarp, not developing it |
| **AUTO-20251124200259** | Automation execution log | Using Exarp, not developing it |

---

## Next Steps

1. **Export tasks** T-1 through T-5 from main repository
2. **Create tasks** in Exarp repository with same content
3. **Update task IDs** in Exarp repository (e.g., `EXARP-1` through `EXARP-5`)
4. **Remove tasks** from main repository
5. **Update dependencies** if any tasks reference T-1 through T-5
6. **Document migration** in Exarp repository

---

## Migration Script

A migration script could be created to:
1. Read tasks T-1 through T-5 from main repository
2. Export to JSON format
3. Import into Exarp repository
4. Update IDs and dependencies
5. Remove from main repository

**See**: `scripts/migrate_exarp_todos.py` (to be created)

---

**Status**: Analysis Complete
**Recommendation**: Move T-1 through T-5 to Exarp repository
**Action Required**: Manual migration of 5 tasks
**Related**: All tasks are part of tool reuse refactoring (see `EXARP_TOOL_REUSE_ANALYSIS.md`)
