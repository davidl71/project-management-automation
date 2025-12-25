# MCP Prompts - Project Management Automation

**Status:** ✅ 34 Prompts Available

This server provides reusable prompt templates that guide users through common project management workflows.

---

## 📋 Available Prompts

### Documentation Management

#### `doc_check`
**Description:** Analyze documentation health and create tasks for issues

**Use Case:** Before releases, after major changes, or during regular maintenance

**Related Tool:** `health(action=docs, create_tasks=True)`

---

#### `doc_quick`
**Description:** Quick documentation health check without creating tasks

**Use Case:** Quick assessment before committing changes

**Related Tool:** `health(action=docs, create_tasks=False)`

---

### Task Management

#### `align`
**Description:** Analyze Todo2 task alignment with project goals

**Use Case:** Before starting new work, during sprint planning

**Related Tool:** `analyze_alignment(action=todo2, create_followup_tasks=True)`

---

#### `dups`
**Description:** Find and consolidate duplicate Todo2 tasks

**Use Case:** Regular cleanup, before starting new work

**Related Tool:** `task_analysis(action=duplicates, similarity_threshold=0.85, auto_fix=False)`

---

#### `sync`
**Description:** Synchronize tasks between shared TODO table and Todo2

**Use Case:** Keep task systems in sync, after bulk updates

**Related Tool:** `task_workflow(action=sync, dry_run=True)` (preview) or `task_workflow(action=sync, dry_run=False)` (apply)

---

#### `discover`
**Description:** Discover tasks from TODO comments, markdown, and orphaned tasks

**Use Case:** Find hidden work items, capture todos from code comments

**Related Tool:** `task_discovery(action=all, create_tasks=False)`

---

### Security & Dependencies

#### `scan`
**Description:** Scan project dependencies for security vulnerabilities (supports all languages via tool parameter)

**Use Case:** Before releases, after dependency updates, regular security audits

**Related Tool:** 
- `security(action=report)` - Combined report for all languages
- `security(action=scan, languages=['python'])` - Python only
- `security(action=scan, languages=['rust'])` - Rust only
- `security(action=alerts)` - GitHub Dependabot alerts

---

### Automation Discovery

#### `auto`
**Description:** Discover new automation opportunities in the codebase

**Use Case:** During refactoring, after completing features, regular optimization

**Related Tool:** `automation(action=discover, min_value_score=0.7)`

---

#### `auto_high`
**Description:** Find only high-value automation opportunities (score >= 0.8)

**Use Case:** Focus on highest-impact automations

**Related Tool:** `automation(action=discover, min_value_score=0.8)`

---

#### `automation_setup`
**Description:** One-time automation setup: git hooks, triggers, cron

**Use Case:** Initial project setup, configuring automation infrastructure

**Related Tool:** `setup_hooks(action=git)`, `setup_hooks(action=patterns)`

---

### Workflow Prompts

#### `pre_sprint`
**Description:** Pre-sprint cleanup workflow: duplicates, alignment, documentation

**Workflow:**
1. `task_analysis(action=duplicates)` - Find and consolidate duplicates
2. `analyze_alignment(action=todo2)` - Check task alignment
3. `health(action=docs)` - Ensure docs are up to date

**Use Case:** Before starting a new sprint or iteration

---

#### `post_impl`
**Description:** Post-implementation review workflow: docs, security, automation

**Workflow:**
1. `health(action=docs)` - Update documentation
2. `security(action=scan)` - Check for new vulnerabilities
3. `automation(action=discover)` - Discover new automation needs

**Use Case:** After completing a feature or major change

---

#### `weekly`
**Description:** Weekly maintenance workflow: docs, duplicates, security, sync

**Workflow:**
1. `health(action=docs)` - Keep docs healthy
2. `task_analysis(action=duplicates)` - Clean up duplicates
3. `security(action=scan)` - Check security
4. `task_workflow(action=sync)` - Sync across systems

**Use Case:** Regular weekly maintenance routine

---

#### `daily_checkin`
**Description:** Daily check-in workflow: server status, blockers, git health

**Use Case:** Start of day routine, quick health check

**Related Tool:** `health(action=server)`, `health(action=git)`, `health(action=dod)`

---

#### `sprint_start`
**Description:** Sprint start workflow: clean backlog, align tasks, queue work

**Use Case:** Beginning of sprint, preparing for new work

**Related Tool:** `task_analysis(action=duplicates)`, `analyze_alignment(action=todo2)`, `task_workflow(action=cleanup)`

---

#### `sprint_end`
**Description:** Sprint end workflow: test coverage, docs, security check

**Use Case:** End of sprint, preparing for release

**Related Tool:** `testing(action=coverage)`, `health(action=docs)`, `security(action=scan)`

---

### Project Health & Reporting

#### `project_health`
**Description:** Full project health assessment: code, docs, security, CI/CD

**Use Case:** Comprehensive project review, before major decisions

**Related Tool:** `health(action=server)`, `health(action=git)`, `health(action=docs)`, `health(action=dod)`, `health(action=cicd)`

---

#### `scorecard`
**Description:** Generate comprehensive project health scorecard with all metrics

**Use Case:** Executive reporting, project status updates

**Related Tool:** `report(action=scorecard)`

---

#### `overview`
**Description:** Generate one-page project overview for stakeholders

**Use Case:** Quick status updates, onboarding new team members

**Related Tool:** `report(action=overview)`

---

### Configuration & Setup

#### `config`
**Description:** Generate IDE configuration files

**Use Case:** Initial project setup, IDE standardization

**Related Tool:** `generate_config(action=rules)`, `generate_config(action=ignore)`, `generate_config(action=simplify)`

---

### Context & Mode Management

#### `mode`
**Description:** Suggest optimal Cursor IDE mode (Agent vs Ask) for a task

**Use Case:** Before starting work, optimizing AI interaction mode

**Related Tool:** `recommend(action=workflow, task_id=...)`

---

#### `context`
**Description:** Manage LLM context with summarization and budget tools

**Use Case:** Optimizing context usage, managing token budgets

**Related Tool:** `context(action=summarize)`, `context(action=budget)`, `context(action=batch)`

---

#### `remember`
**Description:** Use AI session memory to persist insights

**Use Case:** Saving important discoveries, building knowledge base

**Related Tool:** `memory(action=save)`, `memory(action=recall)`, `memory(action=search)`

---

### Session Handoff

#### `end_of_day`
**Description:** End your work session and create a handoff for other developers

**Use Case:** End of workday, transferring context to teammates

**Related Tool:** `session(action=handoff)`

---

#### `resume_session`
**Description:** Resume work by reviewing the latest handoff from another developer

**Use Case:** Start of workday, picking up where someone left off

**Related Tool:** `session(action=handoff, direction=both)`

---

#### `view_handoffs`
**Description:** View recent handoff notes from all developers

**Use Case:** Team coordination, understanding recent changes

**Related Tool:** `session(action=handoff)`

---

### Persona Workflows

#### `dev`
**Description:** Developer daily workflow for writing quality code

**Use Case:** Daily development routine, code quality focus

**Persona:** Developer

---

#### `pm`
**Description:** Project Manager workflow for delivery tracking

**Use Case:** Project management, delivery tracking, stakeholder communication

**Persona:** Project Manager

---

#### `reviewer`
**Description:** Code Reviewer workflow for quality gates

**Use Case:** Code review, quality assurance

**Persona:** Code Reviewer

---

#### `exec`
**Description:** Executive/Stakeholder workflow for strategic view

**Use Case:** Executive reporting, strategic decision making

**Persona:** Executive

---

#### `seceng`
**Description:** Security Engineer workflow for risk management

**Use Case:** Security audits, vulnerability management

**Persona:** Security Engineer

---

#### `arch`
**Description:** Architect workflow for system design

**Use Case:** System design, architecture decisions

**Persona:** Architect

---

#### `qa`
**Description:** QA Engineer workflow for quality assurance

**Use Case:** Testing, quality assurance

**Persona:** QA Engineer

---

#### `writer`
**Description:** Technical Writer workflow for documentation

**Use Case:** Documentation, technical writing

**Persona:** Technical Writer

---

## 🚀 Usage

### In Cursor

Prompts are available in Cursor's MCP prompt menu. Select a prompt to:
1. Get structured guidance for the workflow
2. See which tools to use
3. Understand the recommended parameters

### Example

1. Open Cursor's prompt menu
2. Select "Pre-Sprint Cleanup" (`pre_sprint`)
3. Follow the workflow steps
4. Use the recommended tools with suggested parameters

---

## 📊 Prompt Categories

| Category | Count | Prompts |
|----------|-------|---------|
| Documentation | 2 | `doc_check`, `doc_quick` |
| Task Management | 4 | `align`, `dups`, `sync`, `discover` |
| Security | 1 | `scan` |
| Automation | 3 | `auto`, `auto_high`, `automation_setup` |
| Workflows | 6 | `pre_sprint`, `post_impl`, `weekly`, `daily_checkin`, `sprint_start`, `sprint_end` |
| Project Health | 3 | `project_health`, `scorecard`, `overview` |
| Configuration | 1 | `config` |
| Context & Mode | 3 | `mode`, `context`, `remember` |
| Session Handoff | 3 | `end_of_day`, `resume_session`, `view_handoffs` |
| Personas | 8 | `dev`, `pm`, `reviewer`, `exec`, `seceng`, `arch`, `qa`, `writer` |

**Total: 34 prompts**

**Note:** Removed redundant prompts:
- `scan_py`, `scan_rs` - Consolidated into `scan` (users can specify language via tool parameter)
- `task_review` - Redundant (combines `align`, `dups`, and `cleanup` - use individual prompts or workflows like `pre_sprint`)

---

## 🔄 Integration with Tools

All prompts are designed to work seamlessly with the project management automation tools:

- ✅ **Tool-specific prompts** guide users to the right tool with correct parameters
- ✅ **Workflow prompts** sequence multiple tools for complete workflows
- ✅ **Context-aware** prompts provide use case guidance
- ✅ **Persona prompts** provide role-specific workflows

---

**Last Updated:** 2025-12-25
