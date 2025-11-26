# IDE Integration Guide

> **How to integrate Exarp workflows into Cursor and VSCode for seamless project management**

---

## 📋 Table of Contents

1. [Cursor Integration](#cursor-integration)
2. [VSCode Integration](#vscode-integration)
3. [Workflow Discovery](#workflow-discovery)
4. [TODO Comment Sync](#todo-comment-sync)
5. [Project Goals Integration](#project-goals-integration)
6. [Clarification & Persona Detection](#clarification--persona-detection)

---

## 🎯 Cursor Integration

### MCP Server (Already Configured)

Exarp tools are available via MCP:
```bash
/exarp/project_scorecard
/exarp/project_overview
/exarp/prompt persona_developer
```

### .cursorrules for Workflow Guidance

Add to `.cursorrules` to help Cursor suggest appropriate workflows:

```markdown
# Exarp Workflow Integration

## Persona Detection
When the user mentions their role, suggest appropriate Exarp workflows:
- "developer" or "coding" → Use /exarp/prompt persona_developer
- "PM" or "project manager" or "planning" → Use /exarp/prompt persona_project_manager
- "review" or "PR" → Use /exarp/prompt persona_code_reviewer
- "security" or "vulnerabilities" → Use /exarp/prompt persona_security
- "architecture" or "design" → Use /exarp/prompt persona_architect
- "testing" or "QA" → Use /exarp/prompt persona_qa
- "documentation" or "docs" → Use /exarp/prompt persona_tech_writer
- "executive" or "status" or "stakeholder" → Use /exarp/prompt persona_executive

## Automatic Workflow Triggers
- Before committing: Suggest running /exarp/project_scorecard
- When asking about project health: Run /exarp/project_scorecard
- When asking about tasks: Run /exarp/list_tasks_awaiting_clarification
- When starting work: Suggest /exarp/prompt daily_checkin
- End of sprint: Suggest /exarp/prompt sprint_end

## Clarification Questions
When user intent is unclear, ask:
1. "What's your role? (developer/PM/reviewer/architect/security/QA)"
2. "What do you want to achieve? (health check/planning/review/deep analysis)"
3. "How much time do you have? (2 min quick/15 min detailed/1 hour deep)"

## Project Goals Awareness
Read PROJECT_GOALS.md to understand project priorities.
When suggesting tasks, align with current phase and keywords.
```

### Cursor Prompts (Accessible via @)

Create `.cursor/prompts/` directory with workflow prompts:

```bash
mkdir -p .cursor/prompts
```

#### `.cursor/prompts/quick-health.md`
```markdown
# Quick Health Check

Run a quick project health check and summarize key findings.

Steps:
1. Run /exarp/project_scorecard
2. Highlight any scores below 70%
3. List top 3 recommended actions
4. Note any blockers
```

#### `.cursor/prompts/start-day.md`
```markdown
# Start of Day Workflow

Help me start my day with a project overview.

Steps:
1. Run /exarp/project_scorecard for health
2. Run /exarp/list_tasks_awaiting_clarification for blockers
3. Suggest top 3 tasks to work on based on priority
4. Note any security alerts
```

#### `.cursor/prompts/pre-commit.md`
```markdown
# Pre-Commit Check

Before I commit, verify my changes are ready.

Steps:
1. Check what files changed
2. Run /exarp/check_documentation_health if docs changed
3. Run /exarp/project_scorecard --quick for metrics
4. Flag any complexity or security concerns
```

---

## 🔧 VSCode Integration

### Tasks Configuration (`.vscode/tasks.json`)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Exarp: Quick Health Check",
      "type": "shell",
      "command": "python -m project_management_automation.tools.project_scorecard",
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "problemMatcher": []
    },
    {
      "label": "Exarp: Deep Analysis",
      "type": "shell",
      "command": "python -m project_management_automation.tools.project_scorecard tier=deep",
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Exarp: Project Overview (HTML)",
      "type": "shell",
      "command": "python -m project_management_automation.tools.project_overview output_format=html output_path=docs/PROJECT_OVERVIEW.html && open docs/PROJECT_OVERVIEW.html",
      "group": "test"
    },
    {
      "label": "Exarp: Security Scan",
      "type": "shell",
      "command": "python -m project_management_automation.tools.dependency_security",
      "group": "test"
    },
    {
      "label": "Exarp: Documentation Health",
      "type": "shell",
      "command": "python -m project_management_automation.tools.docs_health",
      "group": "test"
    },
    {
      "label": "Exarp: Run Tests with Coverage",
      "type": "shell",
      "command": "python -m pytest --cov=project_management_automation --cov-report=html",
      "group": "test"
    }
  ]
}
```

**Usage:** `Cmd+Shift+P` → "Tasks: Run Task" → Select Exarp task

### Keyboard Shortcuts (`.vscode/keybindings.json`)

Add to user keybindings:
```json
[
  {
    "key": "cmd+shift+h",
    "command": "workbench.action.tasks.runTask",
    "args": "Exarp: Quick Health Check"
  },
  {
    "key": "cmd+shift+d",
    "command": "workbench.action.tasks.runTask",
    "args": "Exarp: Deep Analysis"
  },
  {
    "key": "cmd+shift+o",
    "command": "workbench.action.tasks.runTask",
    "args": "Exarp: Project Overview (HTML)"
  }
]
```

### Snippets (`.vscode/exarp.code-snippets`)

```json
{
  "Exarp Scorecard": {
    "prefix": "exarp-score",
    "body": [
      "# Run: /exarp/project_scorecard",
      "# Tier options: default (10s), quick (15s), deep (4min)"
    ],
    "description": "Insert Exarp scorecard command"
  },
  "Exarp TODO Task": {
    "prefix": "exarp-todo",
    "body": [
      "# TODO(exarp): $1",
      "# Priority: ${2|high,medium,low|}",
      "# Tags: ${3:enhancement}"
    ],
    "description": "Create Exarp-compatible TODO comment"
  },
  "Exarp FIXME": {
    "prefix": "exarp-fixme",
    "body": [
      "# FIXME(exarp): $1",
      "# Priority: high",
      "# Tags: bug"
    ],
    "description": "Create Exarp-compatible FIXME comment"
  }
}
```

### Settings Recommendations (`.vscode/settings.json`)

```json
{
  "todo-tree.general.tags": [
    "TODO",
    "FIXME",
    "TODO(exarp)",
    "FIXME(exarp)",
    "HACK",
    "XXX"
  ],
  "todo-tree.highlights.customHighlight": {
    "TODO(exarp)": {
      "icon": "checklist",
      "foreground": "#FF8C00",
      "iconColour": "#FF8C00"
    },
    "FIXME(exarp)": {
      "icon": "alert",
      "foreground": "#FF0000",
      "iconColour": "#FF0000"
    }
  },
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  }
}
```

### Extensions Recommendations (`.vscode/extensions.json`)

```json
{
  "recommendations": [
    "gruntfuggly.todo-tree",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "ms-python.black-formatter"
  ]
}
```

---

## 🔍 Workflow Discovery

### Method 1: Ask Cursor Directly

```
User: "What workflows are available?"
Cursor: [Reads prompts.py, lists available workflows]

User: "I'm a developer, what should I run?"
Cursor: [Detects persona, suggests /exarp/prompt persona_developer]
```

### Method 2: MCP Resource (Proposed)

Add an `exarp://workflows` resource:

```python
@mcp.resource("exarp://workflows")
def list_workflows():
    """List all available Exarp workflows by persona and scenario."""
    return {
        "personas": {
            "developer": "Daily code quality workflow",
            "project_manager": "Delivery tracking workflow",
            # ...
        },
        "scenarios": {
            "daily_checkin": "Morning health check",
            "sprint_start": "Sprint preparation",
            # ...
        }
    }
```

### Method 3: Interactive Workflow Selector (Proposed Tool)

```python
@mcp.tool()
def suggest_workflow(
    role: Optional[str] = None,
    goal: Optional[str] = None,
    time_available: Optional[int] = None  # minutes
) -> str:
    """
    [HINT: Suggest workflow. Returns recommended tools based on role/goal/time.]
    
    Interactively suggest the best Exarp workflow.
    
    If parameters not provided, will ask clarifying questions.
    """
    if not role:
        return "What's your role? (developer/pm/reviewer/architect/security/qa/executive)"
    
    if not goal:
        return "What do you want to achieve? (health-check/planning/review/deep-analysis/security-audit)"
    
    if not time_available:
        return "How much time do you have? (2/5/15/30/60 minutes)"
    
    # Return personalized workflow recommendation
    # ...
```

---

## 📝 TODO Comment Sync

### Exarp-Compatible TODO Format

```python
# TODO(exarp): Implement user authentication
# Priority: high
# Tags: security, feature
# Estimate: 4h

# FIXME(exarp): Race condition in async handler
# Priority: critical
# Tags: bug, async
```

### Proposed Tool: Sync TODO Comments to Todo2

```python
@mcp.tool()
def sync_code_todos(
    scan_paths: list[str] = ["project_management_automation/"],
    create_tasks: bool = False,
    dry_run: bool = True
) -> str:
    """
    [HINT: Sync TODOs. Finds TODO/FIXME comments, optionally creates Todo2 tasks.]
    
    Scan codebase for TODO/FIXME comments and sync with Todo2.
    
    Features:
    - Finds TODO(exarp) formatted comments
    - Extracts priority, tags, estimates
    - Creates/updates Todo2 tasks
    - Tracks location (file:line)
    - Marks resolved when comment removed
    """
```

### VSCode Todo Tree Integration

With Todo Tree extension, TODOs are aggregated in sidebar:
- Click to jump to location
- Filter by tag (exarp, bug, enhancement)
- Export to Todo2 via Exarp tool

---

## 🎯 Project Goals Integration

### Current: PROJECT_GOALS.md

```markdown
# Project Goals

## Current Phase: Phase 2 - Core Tools

## Priority Keywords
- mcp, server, tool, prompt, resource
- automation, workflow, integration
```

### Proposed: Goals-Aware Assistance

#### 1. MCP Resource for Goals

```python
@mcp.resource("exarp://goals")
def get_project_goals():
    """Return current project goals and phase."""
    # Parse PROJECT_GOALS.md
    return {
        "current_phase": "Phase 2 - Core Tools",
        "priority_keywords": ["mcp", "server", "tool"],
        "success_criteria": [...],
        "risks": [...]
    }
```

#### 2. Goal-Aware Task Suggestions

```python
@mcp.tool()
def suggest_aligned_task() -> str:
    """
    [HINT: Suggest task. Returns highest-priority task aligned with current phase.]
    
    Suggest the next task to work on based on:
    1. Current project phase (from PROJECT_GOALS.md)
    2. Task priority and dependencies
    3. Your role (if specified)
    """
```

#### 3. Cursor Rules for Goal Awareness

```markdown
# .cursorrules addition

## Project Goals Awareness
Before suggesting tasks or features:
1. Read PROJECT_GOALS.md
2. Check current phase
3. Prioritize work aligned with phase keywords
4. Flag work that doesn't align with current phase

When reviewing code:
- Check if changes align with project goals
- Flag scope creep (features outside current phase)
```

---

## ❓ Clarification & Persona Detection

### Automatic Persona Detection

Cursor can detect persona from context:

| User Says | Detected Persona | Suggested Workflow |
|-----------|------------------|-------------------|
| "I'm reviewing this PR" | Code Reviewer | `persona_code_reviewer` |
| "Sprint planning tomorrow" | Project Manager | `persona_project_manager` |
| "Is this secure?" | Security Engineer | `persona_security` |
| "Architecture looks complex" | Architect | `persona_architect` |
| "Tests are failing" | QA Engineer | `persona_qa` |
| "Need a status update" | Executive | `persona_executive` |
| "Docs are outdated" | Technical Writer | `persona_tech_writer` |

### Clarification Questions

When intent is unclear, Cursor should ask:

```
Cursor: I'd like to help you with Exarp workflows. A few quick questions:

1. What's your role today?
   [ ] Developer (writing code)
   [ ] Project Manager (tracking delivery)
   [ ] Code Reviewer (reviewing PRs)
   [ ] Architect (system design)
   [ ] Security Engineer (risk assessment)
   [ ] QA Engineer (testing)
   [ ] Executive (status overview)
   [ ] Technical Writer (documentation)

2. What do you want to accomplish?
   [ ] Quick health check (2 min)
   [ ] Detailed analysis (15 min)
   [ ] Deep investigation (1 hour)
   [ ] Find what to work on
   [ ] Prepare for a meeting

3. Any specific concerns?
   [ ] Security
   [ ] Performance
   [ ] Code quality
   [ ] Documentation
   [ ] Task management
```

### Proposed: Interactive Onboarding

```python
@mcp.tool()
def onboard_user() -> str:
    """
    [HINT: Onboard user. Interactive workflow to set up personalized Exarp experience.]
    
    Guide new users through Exarp setup:
    1. Detect/ask role
    2. Configure preferred workflows
    3. Set up automation (hooks, cron)
    4. Import project goals
    5. Sync existing TODOs
    """
```

---

## 🛠️ Implementation Tasks

| Feature | Effort | Priority | Task |
|---------|--------|----------|------|
| `.cursorrules` workflow hints | 1h | 🔴 High | Create now |
| VSCode tasks.json | 1h | 🔴 High | Create now |
| suggest_workflow tool | 2h | 🟡 Medium | T-NEW |
| sync_code_todos tool | 3h | 🟡 Medium | T-NEW |
| exarp://goals resource | 1h | 🟡 Medium | T-NEW |
| exarp://workflows resource | 1h | 🟡 Medium | T-NEW |
| Interactive onboarding | 2h | 🟢 Low | T-NEW |

---

*Last updated: $(date +%Y-%m-%d)*
