# Exarp Project Management Workflows

> **Last Updated:** November 2025

This guide provides recommended workflows for using Exarp to manage your project effectively.

## Quick Reference

| Workflow | When to Use | Command/Prompt |
|----------|-------------|----------------|
| Daily Check | Every morning | `/exarp/server_status` → `list_tasks_awaiting_clarification` |
| Sprint Start | Beginning of sprint | `pre_sprint` prompt |
| Sprint End | End of sprint | `post_impl` prompt |
| Task Review | Monthly / After major changes | `task_review` prompt |
| Weekly Maintenance | Fridays | `weekly` prompt |

---

## 🌅 Daily Workflow (5 min)

### Morning Check-in

```
┌────────────────────────────────────────────────────────────────┐
│  /exarp/server_status              → Is everything running?   │
│  /exarp/list_tasks_awaiting_clarification → Any blockers?     │
│  /exarp/check_working_copy_health  → Git status across agents │
└────────────────────────────────────────────────────────────────┘
```

### Automated (via cron)

```
┌────────────────────────────────────────────────────────────────┐
│  /exarp/run_daily_automation       → Docs health, alignment   │
└────────────────────────────────────────────────────────────────┘
```

**Prompt:** `daily_checkin`

---

## 🏃 Sprint Workflow

### Sprint Start

```
┌────────────────────────────────────────────────────────────────┐
│  /exarp/detect_duplicate_tasks     → Clean backlog            │
│  /exarp/analyze_todo2_alignment    → Tasks match goals?       │
│  /exarp/batch_approve_tasks        → Queue ready tasks        │
└────────────────────────────────────────────────────────────────┘
```

**Prompt:** `pre_sprint` or `sprint_start`

### During Sprint

```
┌────────────────────────────────────────────────────────────────┐
│  /exarp/sprint_automation          → Process background tasks │
│  /exarp/run_tests                  → Verify changes           │
│  /exarp/nightly                    → Overnight task execution │
└────────────────────────────────────────────────────────────────┘
```

### Sprint End

```
┌────────────────────────────────────────────────────────────────┐
│  /exarp/analyze_test_coverage      → Coverage gaps?           │
│  /exarp/check_documentation_health → Docs updated?            │
│  /exarp/scan_dependency_security   → Security check           │
└────────────────────────────────────────────────────────────────┘
```

**Prompt:** `post_impl` or `sprint_end`

---

## 📅 Weekly Maintenance (Friday)

```
┌────────────────────────────────────────────────────────────────┐
│  /exarp/scan_dependency_security   → Security vulnerabilities │
│  /exarp/detect_duplicate_tasks     → Hygiene check            │
│  /exarp/find_automation_opportunities → What can we automate? │
│  /exarp/validate_ci_cd_workflow    → CI/CD healthy?           │
└────────────────────────────────────────────────────────────────┘
```

**Prompt:** `weekly`

---

## 🔍 Task Review Workflow

Use this workflow monthly or after major changes to clean up your task backlog.

```
┌────────────────────────────────────────────────────────────────┐
│  Step 1: /exarp/detect_duplicate_tasks    → Find duplicates   │
│  Step 2: /exarp/analyze_todo2_alignment   → Check alignment   │
│  Step 3: /exarp/list_tasks_awaiting_clarification → Blockers  │
│  Step 4: Review obsolete/stale tasks manually                 │
│  Step 5: /exarp/batch_approve_tasks       → Queue ready tasks │
└────────────────────────────────────────────────────────────────┘
```

**Prompt:** `task_review`

### What to Look For

| Category | Action |
|----------|--------|
| Duplicates | Merge or remove |
| Misaligned | Re-scope or cancel |
| Obsolete | Cancel if work already done |
| Stale (>30 days) | Review priority or cancel |
| Blocked | Resolve dependencies |

---

## 🏥 Project Health Check

Comprehensive project health assessment:

```
┌────────────────────────────────────────────────────────────────┐
│  /exarp/server_status              → Server health            │
│  /exarp/check_documentation_health → Docs score               │
│  /exarp/run_tests coverage=true    → Test coverage            │
│  /exarp/scan_dependency_security   → Security vulnerabilities │
│  /exarp/validate_ci_cd_workflow    → CI/CD status             │
│  /exarp/analyze_todo2_alignment    → Task alignment           │
└────────────────────────────────────────────────────────────────┘
```

**Prompt:** `project_health`

---

## 🔧 On-Demand Tools

| Situation | Tool | Purpose |
|-----------|------|---------|
| New feature | `/exarp/analyze_todo2_alignment` | Ensure tasks align with goals |
| Before commit | `/exarp/run_tests` | Verify nothing broken |
| Code review | `/exarp/check_documentation_health` | Docs current? |
| Onboarding | `/exarp/add_external_tool_hints` | Add Context7 hints |
| Setup | `/exarp/setup_git_hooks` | Auto-run checks on commit |
| Refactor | `/exarp/simplify_rules` | Update cursor rules |

---

## 🤖 One-Time Automation Setup

```bash
# 1. Setup git hooks for automatic checks
/exarp/setup_git_hooks

# 2. Setup pattern triggers for file changes  
/exarp/setup_pattern_triggers

# 3. Configure cron for daily/weekly runs
# See: scripts/cron/*.sh
```

---

## 📊 Decision Flowchart

```
                    ┌─────────────────┐
                    │   What to do?   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   ┌─────────┐         ┌──────────┐         ┌─────────┐
   │  Tasks  │         │   Code   │         │ Project │
   └────┬────┘         └────┬─────┘         └────┬────┘
        │                   │                    │
        ▼                   ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Need tasks?   │   │ Write tests?  │   │ Health check? │
│ → align       │   │ → run_tests   │   │ → daily_auto  │
│ → batch_approve   │ → coverage    │   │ → sprint_auto │
│ → nightly     │   │               │   │               │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                    │
        ▼                   ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Blocked?      │   │ Security?     │   │ Docs stale?   │
│ → clarification   │ → security_scan   │ → docs_health │
│ → resolve     │   │ → ci_cd_valid │   │ → hints       │
└───────────────┘   └───────────────┘   └───────────────┘
```

---

## 🎯 Tool Quick Reference

### Task Management
| Tool | Purpose |
|------|---------|
| `/exarp/analyze_todo2_alignment` | Check task alignment with goals |
| `/exarp/run_nightly_task_automation` | Process tasks overnight |
| `/exarp/detect_duplicate_tasks` | Find duplicate tasks |
| `/exarp/batch_approve_tasks` | Approve ready tasks |
| `/exarp/list_tasks_awaiting_clarification` | Find blocked tasks |
| `/exarp/resolve_task_clarification` | Resolve single task |
| `/exarp/resolve_multiple_clarifications` | Bulk resolve tasks |

### Code Quality
| Tool | Purpose |
|------|---------|
| `/exarp/run_tests` | Run test suite |
| `/exarp/analyze_test_coverage` | Check coverage gaps |
| `/exarp/scan_dependency_security` | Security vulnerabilities |

### Automation
| Tool | Purpose |
|------|---------|
| `/exarp/run_daily_automation` | Daily maintenance |
| `/exarp/sprint_automation` | Full sprint cycle |
| `/exarp/setup_git_hooks` | Auto-run on commits |
| `/exarp/setup_pattern_triggers` | File change triggers |

### Documentation
| Tool | Purpose |
|------|---------|
| `/exarp/check_documentation_health` | Broken links, staleness |
| `/exarp/add_external_tool_hints` | Add Context7 hints |

### Infrastructure
| Tool | Purpose |
|------|---------|
| `/exarp/server_status` | Server health |
| `/exarp/check_working_copy_health` | Git status across agents |
| `/exarp/validate_ci_cd_workflow` | CI/CD validation |

---

## 💡 Pro Tips

1. **Start with automation**: Run `/exarp/setup_git_hooks` once to get automatic pre-commit checks
2. **Use sprint_automation for big batches**: It chains multiple tools together
3. **Weekly security scans**: Set up cron for `/exarp/scan_dependency_security`
4. **Task hygiene**: Run `/exarp/detect_duplicate_tasks` before sprint planning
5. **Check blockers first**: Always run `/exarp/list_tasks_awaiting_clarification` at start of day

---

## See Also

- [HOW_TO_USE_PROMPTS.md](HOW_TO_USE_PROMPTS.md) - Detailed prompt usage
- [PROMPTS.md](../PROMPTS.md) - Available prompts reference
- [README.md](../README.md) - Project overview

