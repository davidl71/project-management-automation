# Exarp Improvements: Lessons from Cursor IDE Best Practices


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on FastAPI, Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use FastAPI async endpoints? use context7"
> - "Show me FastAPI examples examples use context7"
> - "FastAPI best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

> **Analysis Date:** 2025-11-26
> **Source:** [10 Best Practices for Cursor IDE](https://medium.com/@roberto.g.infante/mastering-cursor-ide-10-best-practices-building-a-daily-task-manager-app-0b26524411c1)

## Executive Summary

This document maps the 10 Cursor IDE best practices to actionable improvements for the Exarp MCP server. The goal is to make Exarp itself follow these best practices AND help users of Exarp follow them.

---

## Improvement Matrix

| Best Practice | Current State | Gap | Priority |
|--------------|---------------|-----|----------|
| 1. PRD Generation | ❌ Not supported | HIGH | 🔴 |
| 2. Project Rules | ⚠️ Partial (simplify_rules) | MEDIUM | 🟡 |
| 3. Agent Mode Guidance | ❌ No guidance | HIGH | 🔴 |
| 4. Model Selection | ❌ No guidance | MEDIUM | 🟡 |
| 5. @ References | ⚠️ Tool hints exist | LOW | 🟢 |
| 6. Detailed Prompts | ⚠️ HINT system exists | MEDIUM | 🟡 |
| 7. Tests/Logs/Docs | ✅ Have tools (run_tests, docs_health) | LOW | 🟢 |
| 8. Iterative Prompts | ❌ No feedback loop | HIGH | 🔴 |
| 9. File Exclusion | ❌ No cursorignore generation | MEDIUM | 🟡 |
| 10. MCP Integration | ✅ We ARE an MCP server | N/A | 🟢 |

---

## Detailed Improvement Proposals

### 🔴 HIGH PRIORITY

---

### 1. PRD Generation Tool

**Gap:** Exarp doesn't help users create or maintain PRD files.

**Proposal: `generate_prd` Tool**

```python
@mcp.tool()
def generate_prd(
    project_name: str,
    output_path: Optional[str] = None,
    include_existing_tasks: bool = True,
    include_architecture: bool = True
) -> str:
    """
    [HINT: PRD generation. Creates Product Requirements Document from codebase analysis.]
    
    Generate a Product Requirements Document by analyzing:
    - Existing codebase structure
    - Todo2 tasks and their descriptions
    - PROJECT_GOALS.md alignment
    - Current architecture patterns
    
    Output: instructions.md or PRD.md with structured requirements
    """
```

**Value:**
- Creates the "North Star" document the article emphasizes
- Auto-populates from existing tasks, docs, and code
- Keeps PRD in sync with actual project state

---

### 3. Agent Mode Guidance Tool

**Gap:** No guidance on when to use Agent vs Ask mode for different Exarp tools.

**Proposal: Tool metadata + `recommend_workflow_mode` Tool**

```python
# Add to each tool's docstring/metadata:
TOOL_MODE_HINTS = {
    "project_scorecard": "ASK",      # Informational, no changes
    "check_documentation_health": "ASK",  # Analysis only
    "detect_duplicate_tasks": "AGENT if auto_fix=True else ASK",
    "sprint_automation": "AGENT",     # Makes changes
    "batch_approve_tasks": "AGENT",   # Makes changes
    "run_tests": "AGENT",             # Executes commands
}

@mcp.tool()
def recommend_workflow_mode(task_description: str) -> str:
    """
    [HINT: Workflow mode. Recommends AGENT vs ASK mode for a given task.]
    
    Analyzes task description and recommends:
    - ASK mode: For analysis, planning, understanding
    - AGENT mode: For implementation, automation, changes
    
    Also suggests which Exarp tools are relevant.
    """
```

**Value:**
- Helps users choose the right Cursor mode
- Integrates with Exarp's workflow philosophy
- Maps to tractatus_thinking → exarp → sequential_thinking flow

---

### 8. Iterative Feedback Loop

**Gap:** No way to track prompt iterations or learn from corrections.

**Proposal: `session_feedback` Tool Enhancement**

Enhance existing `session_memory` with iteration tracking:

```python
@mcp.tool()
def record_prompt_iteration(
    original_prompt: str,
    issue_identified: str,
    refined_prompt: str,
    task_id: Optional[str] = None
) -> str:
    """
    [HINT: Prompt iteration. Records prompt refinements for learning.]
    
    Track prompt iterations to:
    1. Build prompt improvement patterns
    2. Suggest refinements for similar future prompts
    3. Create project-specific prompt templates
    
    Feeds into `consult_advisor` for prompt coaching.
    """

@mcp.tool()
def suggest_prompt_refinement(
    current_prompt: str,
    issue_type: str  # "ambiguous", "missing_context", "too_broad", "missing_constraints"
) -> str:
    """
    [HINT: Prompt coach. Suggests how to refine prompts based on common issues.]
    
    Returns refined prompt suggestions based on:
    - Best practices from article
    - Project-specific patterns from session_memory
    - Common prompt pitfalls
    """
```

**Value:**
- Embodies the "iterate, iterate, iterate" philosophy
- Builds institutional knowledge of good prompts
- Integrates with existing advisor/wisdom system

---

### 🟡 MEDIUM PRIORITY

---

### 2. Project Rules Enhancement

**Gap:** `simplify_rules` exists but doesn't generate rules from scratch.

**Proposal: `generate_cursor_rules` Tool**

```python
@mcp.tool()
def generate_cursor_rules(
    output_dir: Optional[str] = None,
    tech_stack: Optional[List[str]] = None,  # ["python", "fastapi", "pytest"]
    include_existing_patterns: bool = True
) -> str:
    """
    [HINT: Rules generation. Creates .cursor/rules/*.mdc from codebase analysis.]
    
    Analyzes codebase to generate Cursor rules:
    - Code style patterns (from existing code)
    - Architecture conventions (from structure)
    - Library preferences (from imports/deps)
    - Testing patterns (from test files)
    
    Output: .cursor/rules/ directory with .mdc files
    """
```

**Value:**
- Automates rule creation instead of manual writing
- Learns from existing codebase patterns
- Creates shareable team conventions

---

### 4. Model Selection Guidance

**Gap:** No guidance on which AI model to use for which task.

**Proposal: Add model recommendations to tool output**

```python
# Add to tool responses when relevant:
def _format_model_recommendation(task_complexity: str, context_size: int) -> str:
    """
    Returns model recommendation based on task needs.
    """
    if context_size > 100000:
        return "💡 Tip: Use a model with extended context (Claude-4 Sonnet Max, Gemini 2.5 Pro)"
    elif task_complexity == "high":
        return "💡 Tip: Use Claude-4 Sonnet or o3 for complex code generation"
    else:
        return "💡 Tip: GPT-4o is sufficient for this task"
```

**Value:**
- Helps users choose appropriate models
- Saves costs on simple tasks
- Ensures quality on complex tasks

---

### 6. Enhanced HINT System

**Gap:** Current HINTs are minimal. Need richer, more actionable descriptions.

**Proposal: Expand HINT format**

Current:
```python
"""[HINT: Docs health. Score 0-100, broken links, tasks created.]"""
```

Enhanced:
```python
"""
[HINT: Docs health. Score 0-100, broken links, tasks created.]

📊 Output: Health score, broken links list, recommended fixes
🔧 Side Effects: Creates Todo2 tasks if create_tasks=True
📁 Affected: docs/ directory analysis
⏱️ Typical Runtime: 5-30 seconds depending on docs volume

Example Prompt:
"Check documentation health and create tasks for any issues found"

Related Tools:
- add_external_tool_hints (add Context7 hints after health check)
- sync_todo_tasks (sync created tasks with shared TODO)
"""
```

**Value:**
- Follows "detailed prompts yield accurate results" principle
- Helps AI choose the right tool
- Provides example prompts users can adapt

---

### 9. cursorignore Generation

**Gap:** No tool to help users configure file exclusions.

**Proposal: `generate_cursorignore` Tool**

```python
@mcp.tool()
def generate_cursorignore(
    output_path: Optional[str] = None,
    include_indexignore: bool = True,
    analyze_large_files: bool = True
) -> str:
    """
    [HINT: cursorignore generator. Creates .cursorignore and .cursorindexignore.]
    
    Analyzes project to recommend exclusions:
    - Build artifacts (build/, dist/, __pycache__/)
    - Dependencies (node_modules/, .venv/)
    - Large files (>100KB that aren't source code)
    - Generated files (*.pyc, *.o, *.log)
    - Sensitive patterns (.env, credentials)
    
    Creates:
    - .cursorignore: Complete exclusions
    - .cursorindexignore: Not indexed but referenceable
    """
```

**Value:**
- Speeds up Cursor indexing
- Reduces AI confusion from irrelevant files
- Improves security by excluding sensitive files

---

### 🟢 LOW PRIORITY (Already Good)

---

### 5. @ References (Tool Hints)

**Current State:** `add_external_tool_hints` already adds Context7 hints to docs.

**Enhancement:** Extend to add `@File`, `@Code` hints in code comments:

```python
# In complex functions, add hints like:
# @File: see models.py for Task schema
# @Code: related function update_task_status
```

---

### 7. Tests/Logs/Docs

**Current State:** Already have:
- `run_tests` - pytest/unittest execution
- `analyze_test_coverage` - coverage analysis
- `check_documentation_health` - docs validation

**Enhancement:** Add "Definition of Done" checker:

```python
@mcp.tool()
def check_definition_of_done(task_id: str) -> str:
    """
    [HINT: DoD check. Verifies tests, logs, docs for a completed task.]
    
    Checks if task completion includes:
    ✅ Unit tests written?
    ✅ Logging in place?
    ✅ Documentation updated?
    ✅ Code reviewed?
    """
```

---

## Implementation Roadmap

### Phase 1: High Impact (Week 1-2)

1. **`generate_prd`** - Create PRD generation tool
2. **`recommend_workflow_mode`** - Add mode guidance
3. **`record_prompt_iteration`** - Prompt feedback loop

### Phase 2: Enhanced UX (Week 3-4)

4. **`generate_cursor_rules`** - Rules generation
5. **Enhanced HINT system** - Richer tool descriptions
6. **Model recommendations** - Add to tool outputs

### Phase 3: Polish (Week 5+)

7. **`generate_cursorignore`** - File exclusion tool
8. **`check_definition_of_done`** - Completion verification
9. **@ Reference hints** - Code-level hints

---

## Tool Summary Table

| New Tool | Purpose | Best Practice # |
|----------|---------|-----------------|
| `generate_prd` | Create/maintain PRD from codebase | #1 |
| `generate_cursor_rules` | Create .mdc rules from patterns | #2 |
| `recommend_workflow_mode` | AGENT vs ASK guidance | #3 |
| `record_prompt_iteration` | Track prompt refinements | #8 |
| `suggest_prompt_refinement` | Coach better prompts | #8 |
| `generate_cursorignore` | Create exclusion files | #9 |
| `check_definition_of_done` | Verify completion quality | #7 |

---

## Integration with Existing Philosophy

These improvements align with Exarp's existing workflow:

```
tractatus_thinking → UNDERSTAND structure (Best Practice #1: PRD)
        ↓
    exarp tools → ANALYZE and AUTOMATE (Best Practices #2-9)
        ↓
sequential_thinking → IMPLEMENT steps (Best Practice #8: Iteration)
```

The new tools reinforce the "intentionality" theme from the article: guide the AI with clear requirements, rules, and context.

---

## Metrics for Success

| Metric | Current | Target |
|--------|---------|--------|
| Tools with rich HINT | 5% | 100% |
| PRD coverage | 0% | 80% |
| Rules generation | Manual | Automated |
| Prompt iteration tracking | None | Full |
| cursorignore generation | None | Auto |

---

**Next Steps:**
1. Review and prioritize proposals
2. Create Todo2 tasks for approved items
3. Begin Phase 1 implementation

---

*Generated from analysis of Cursor IDE Best Practices article*

