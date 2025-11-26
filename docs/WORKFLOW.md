# Exarp Workflow Guide

> **Comprehensive project management workflows for different roles and scenarios**

---

## 📋 Table of Contents

1. [Persona-Based Workflows](#persona-based-workflows)
2. [Scenario-Based Workflows](#scenario-based-workflows)
3. [Metric Tiers](#metric-tiers)
4. [Automation Schedule](#automation-schedule)
5. [Quick Reference](#quick-reference)

---

## 👥 Persona-Based Workflows

### 🧑‍💻 Developer (Daily Contributor)

**Goal:** Write quality code, stay unblocked, contribute effectively

#### Morning Checkin (~2 min)
\`\`\`
/exarp/project_scorecard              # Quick health check
/exarp/list_tasks_awaiting_clarification  # Any blockers?
\`\`\`

**What to look for:**
- Overall health score (target: >75%)
- Any tasks blocked or awaiting input
- Security alerts (critical vulns = stop and fix)

#### Before Committing
\`\`\`
/exarp/check_documentation_health     # If you touched docs
# Git pre-commit hook runs automatically:
#   - Complexity check on changed files
#   - Security scan (bandit)
\`\`\`

#### Before PR/Push
\`\`\`
/exarp/analyze_todo2_alignment        # Is my work aligned with goals?
# Git pre-push hook runs automatically:
#   - Full security scan
#   - Test suite
\`\`\`

#### Weekly Self-Review (~10 min)
\`\`\`
/exarp/project_scorecard --quick      # With complexity metrics
/exarp/consolidate_tags dry_run=true  # Tag hygiene
\`\`\`

**Key Metrics for Developers:**
| Metric | Why It Matters | Target |
|--------|----------------|--------|
| Cyclomatic Complexity | Your code maintainability | <10 per function |
| Test Coverage | Your code is tested | >80% |
| Bandit Findings | Security issues you introduced | 0 high/critical |
| Cycle Time | How fast you complete tasks | <3 days avg |

---

### 📊 Project Manager (Delivery Focus)

**Goal:** Track progress, remove blockers, ensure delivery

#### Daily Standup Prep (~3 min)
\`\`\`
/exarp/project_scorecard              # Overall health
/exarp/list_tasks_awaiting_clarification  # What needs decisions?
\`\`\`

**Dashboard view:**
- Task completion rate (target: on track for sprint)
- Blocked tasks count (target: 0)
- In-progress count (should match team capacity)

#### Sprint Planning (~15 min)
\`\`\`
/exarp/project_overview output_format=markdown  # Current state
/exarp/detect_duplicate_tasks         # Clean up backlog
/exarp/analyze_todo2_alignment        # Prioritize aligned work
\`\`\`

#### Sprint Retrospective (~20 min)
\`\`\`
/exarp/project_scorecard --deep       # Full analysis
# Review:
#   - Cycle time distribution (T-56)
#   - First pass yield (T-57)
#   - Estimation accuracy (T-32)
\`\`\`

**Questions to answer:**
1. Did we complete what we planned? (completion rate)
2. Did we have rework? (first pass yield)
3. Were estimates accurate? (estimation vs actual)
4. What blocked us? (blocked tasks, dependencies)

#### Weekly Status Report (~5 min)
\`\`\`
/exarp/project_overview output_format=html output_path=docs/WEEKLY_STATUS.html
\`\`\`

**Key Metrics for PMs:**
| Metric | Why It Matters | Target |
|--------|----------------|--------|
| Task Completion % | Sprint progress | Per sprint goal |
| Blocked Tasks | Delivery risk | 0 |
| Cycle Time | Predictability | Consistent |
| First Pass Yield | Quality of planning | >85% |
| Dependency Health | Bottleneck risk | No cycles |

---

### 🔍 Code Reviewer (Quality Gate)

**Goal:** Ensure code quality, catch issues early, mentor

#### Pre-Review Check (~1 min)
\`\`\`
# Run on the PR branch:
/exarp/project_scorecard --quick      # Changed since main?
\`\`\`

#### During Review
\`\`\`
# If complexity concerns:
radon cc <changed_files> -s           # Cyclomatic complexity
radon mi <changed_files> -s           # Maintainability index

# If security concerns:
bandit -r <changed_files>             # Security scan

# If architecture concerns:
/exarp/project_scorecard --deep       # Full coupling/cohesion
\`\`\`

#### Review Checklist (automated where possible)
- [ ] Complexity acceptable? (CC < 10)
- [ ] Tests added/updated?
- [ ] No security issues? (Bandit clean)
- [ ] Documentation updated?
- [ ] No dead code introduced? (Vulture)

**Key Metrics for Reviewers:**
| Metric | Why It Matters | Target |
|--------|----------------|--------|
| Cyclomatic Complexity | Maintainability | <10 new, <15 existing |
| Comment Density | Readability | 10-30% |
| Bandit Findings | Security | 0 in new code |
| Coupling | Architecture impact | Low increase |

---

### 👔 Executive / Stakeholder (Strategic View)

**Goal:** Understand project health, risks, and progress at a glance

#### Weekly Check (~2 min)
\`\`\`
/exarp/project_overview output_format=html
\`\`\`

**One-page summary includes:**
- Overall health score with trend
- Key risks and blockers
- Progress toward goals
- Resource utilization

#### Monthly Review (~10 min)
\`\`\`
/exarp/project_scorecard --deep output_format=markdown
# Review GQM goal achievement (T-66)
\`\`\`

**Executive Dashboard Metrics:**
| Metric | What It Tells You |
|--------|-------------------|
| Health Score (0-100) | Overall project health |
| Goal Alignment % | Are we building the right things? |
| Security Score | Risk exposure |
| Velocity Trend | Are we speeding up or slowing down? |
| Tech Debt Score | Long-term sustainability |

#### Quarterly Strategy (~30 min)
\`\`\`
/exarp/project_scorecard --deep
# Review:
#   - Uniqueness score (are we reinventing wheels?)
#   - Architecture health (sustainable?)
#   - Security posture (acceptable risk?)
\`\`\`

---

### 🔒 Security Engineer (Risk Focus)

**Goal:** Identify and mitigate security risks

#### Daily Scan (~5 min)
\`\`\`
/exarp/scan_dependency_security       # Dependency vulnerabilities
\`\`\`

#### Weekly Deep Scan (~15 min)
\`\`\`
/exarp/scan_dependency_security       # Dependencies
bandit -r project_management_automation/ -f json  # Code security
/exarp/project_scorecard              # Security score trend
\`\`\`

#### Security Audit (~1 hour)
\`\`\`
/exarp/project_scorecard --deep       # Full security section
# Review:
#   - All Bandit findings with context
#   - Dependency tree vulnerabilities
#   - Security hotspots (files with most issues)
#   - CVE details and remediation
\`\`\`

**Key Metrics for Security:**
| Metric | Why It Matters | Target |
|--------|----------------|--------|
| Critical Vulns | Immediate risk | 0 |
| High Vulns | Short-term risk | 0 |
| Bandit High/Critical | Code security | 0 |
| Security Score | Overall posture | >90% |

---

### 🏗️ Architect (System Design)

**Goal:** Ensure sustainable architecture, manage technical debt

#### Weekly Architecture Review (~15 min)
\`\`\`
/exarp/project_scorecard --deep       # Architecture metrics
# Focus on:
#   - Coupling matrix
#   - Cohesion scores
#   - Distance from Main Sequence
#   - Dependency graph
\`\`\`

#### Before Major Changes
\`\`\`
# Current state baseline:
/exarp/project_scorecard --deep output_path=before_change.json

# After implementation:
/exarp/project_scorecard --deep output_path=after_change.json

# Compare architecture impact
\`\`\`

#### Tech Debt Prioritization (~30 min)
\`\`\`
/exarp/project_scorecard --deep
# Review:
#   - High complexity functions (refactor candidates)
#   - Dead code (remove candidates)
#   - Coupling hotspots (decoupling candidates)
#   - Halstead effort (complexity burden)
\`\`\`

**Key Metrics for Architects:**
| Metric | Why It Matters | Target |
|--------|----------------|--------|
| Avg Cyclomatic Complexity | Maintainability | <5 |
| Max Complexity | Worst offenders | <15 |
| Distance from Main Sequence | Architecture balance | <0.3 |
| Coupling (Ce, Ca) | Module independence | Low |
| Dead Code % | Cruft accumulation | <5% |

---

### 🧪 QA Engineer (Quality Assurance)

**Goal:** Ensure comprehensive testing, track defects

#### Daily Testing Status (~3 min)
\`\`\`
/exarp/run_tests                      # Run test suite
/exarp/analyze_test_coverage          # Coverage report
\`\`\`

#### Sprint Testing Review (~20 min)
\`\`\`
/exarp/project_scorecard --quick      # Test metrics
# Review:
#   - Test coverage % (target: >80%)
#   - Test ratio (tests/code)
#   - Failing tests
\`\`\`

#### Defect Analysis (~30 min)
\`\`\`
# When ODC is implemented (T-63):
# Review defect patterns:
#   - Defect type distribution
#   - Trigger analysis (where are bugs found?)
#   - Impact distribution
\`\`\`

**Key Metrics for QA:**
| Metric | Why It Matters | Target |
|--------|----------------|--------|
| Test Coverage | Code tested | >80% |
| Tests Passing | Current quality | 100% |
| Defect Density | Bugs per KLOC | <5 |
| First Pass Yield | Rework indicator | >85% |

---

### 📝 Technical Writer (Documentation)

**Goal:** Maintain accurate, complete documentation

#### Weekly Doc Health (~5 min)
\`\`\`
/exarp/check_documentation_health     # Full docs analysis
\`\`\`

**What to look for:**
- Broken links (fix immediately)
- Stale documents (review and update)
- Missing documentation (add to backlog)

#### Documentation Metrics
| Metric | Why It Matters | Target |
|--------|----------------|--------|
| Broken Links | User experience | 0 |
| Stale Docs | Accuracy | 0 >30 days |
| Comment Density | Code docs | 10-30% |
| Docstring Coverage | API docs | >90% |

---

## 🎯 Scenario-Based Workflows

### New Team Member Onboarding
\`\`\`bash
# 1. Understand project health
/exarp/project_overview output_format=html

# 2. Understand architecture
/exarp/project_scorecard --deep
# Review: coupling matrix, dependency graph

# 3. Understand goals
cat PROJECT_GOALS.md
# When GQM implemented (T-66): metrics-to-goals report

# 4. Find tasks to start with
/exarp/analyze_task_complexity        # Find simple tasks
\`\`\`

### Release Preparation
\`\`\`bash
# 1. Full health check
/exarp/project_scorecard --deep

# 2. Security gate
/exarp/scan_dependency_security
bandit -r project_management_automation/ -f json

# 3. Documentation check
/exarp/check_documentation_health

# 4. Test verification
/exarp/run_tests coverage=true

# 5. Generate release notes
/exarp/project_overview output_format=markdown
\`\`\`

### Debugging Production Issue
\`\`\`bash
# 1. Quick health check
/exarp/project_scorecard

# 2. Find related code
# Use complexity + coupling to identify fragile areas

# 3. After fix - verify no regression
/exarp/run_tests
/exarp/project_scorecard              # Health didn't drop
\`\`\`

### Technical Debt Sprint
\`\`\`bash
# 1. Identify debt
/exarp/project_scorecard --deep
# High complexity functions
# Dead code
# Coupling hotspots

# 2. Prioritize
# Impact × Effort matrix

# 3. Track progress
/exarp/project_scorecard --deep output_path=before.json
# ... do work ...
/exarp/project_scorecard --deep output_path=after.json
# Compare metrics
\`\`\`

---

## �� Metric Tiers

### Tier 1: Default (~10 sec)
*Always runs, suitable for CI*

| Metric | Category |
|--------|----------|
| SLOC, Files, Tools | Codebase |
| Test Ratio, Pass % | Testing |
| Completion %, Blocked | Tasks |
| Critical Vulns | Security |
| Hooks, CI, Cron | Dogfooding |
| Health Score | Overall |

### Tier 2: Quick (~15 sec)
*Adds complexity and git metrics*

| Metric | Category |
|--------|----------|
| Avg Complexity (CC) | Code Quality |
| Maintainability Index | Code Quality |
| Comment Density | Documentation |
| Commits This Week | Velocity |

### Tier 3: Deep (~3-5 min)
*Full investigation mode*

| Metric | Category |
|--------|----------|
| Halstead Metrics | Complexity |
| Coupling Matrix | Architecture |
| Cohesion (LCOM) | Architecture |
| Distance from Main Sequence | Architecture |
| Dead Code Report | Code Quality |
| Git Hotspots & Churn | Velocity |
| Cycle Time Distribution | Tasks |
| ODC Defect Analysis | Quality |
| Full Bandit Report | Security |

---

## ⏰ Automation Schedule

### Continuous (Every Commit)
- Pre-commit: Quick complexity check, basic security
- Pre-push: Full test suite, security scan

### Daily (Cron: 6 AM)
\`\`\`bash
/exarp/run_daily_automation
# - Documentation health
# - Tag consolidation (dry-run)
# - Task alignment check
\`\`\`

### Weekly (Cron: Monday 7 AM)
\`\`\`bash
/exarp/sprint_automation
# - Full scorecard
# - Duplicate detection
# - Security scan
# - Project overview generation
\`\`\`

### Monthly (Manual or Cron: 1st of month)
\`\`\`bash
/exarp/project_scorecard --deep output_path=monthly_report.md
# - Full architecture review
# - Tech debt assessment
# - Goal alignment review
\`\`\`

---

## 🗂️ Quick Reference Card

| I want to... | Run this |
|--------------|----------|
| Check overall health | \`/exarp/project_scorecard\` |
| Get one-page summary | \`/exarp/project_overview\` |
| Find what to work on | \`/exarp/list_tasks_awaiting_clarification\` |
| Check my alignment | \`/exarp/analyze_todo2_alignment\` |
| Verify docs are OK | \`/exarp/check_documentation_health\` |
| Run tests | \`/exarp/run_tests\` |
| Check security | \`/exarp/scan_dependency_security\` |
| Find duplicates | \`/exarp/detect_duplicate_tasks\` |
| Clean up tags | \`/exarp/consolidate_tags\` |
| Deep dive | \`/exarp/project_scorecard --deep\` |

---

## 🔄 Workflow Decision Tree

\`\`\`
Start
  │
  ├─ "How's the project?" ──────────► /exarp/project_scorecard
  │
  ├─ "What should I work on?" ──────► /exarp/list_tasks_awaiting_clarification
  │                                   /exarp/analyze_task_complexity
  │
  ├─ "Is my PR ready?" ─────────────► /exarp/project_scorecard --quick
  │                                   /exarp/run_tests
  │
  ├─ "Why is quality dropping?" ────► /exarp/project_scorecard --deep
  │                                   (review complexity, coupling)
  │
  ├─ "Are we secure?" ──────────────► /exarp/scan_dependency_security
  │                                   bandit -r . -f json
  │
  ├─ "What's blocking us?" ─────────► /exarp/detect_duplicate_tasks
  │                                   /exarp/analyze_todo2_alignment
  │
  └─ "Executive summary?" ──────────► /exarp/project_overview output_format=html
\`\`\`

---

*Last updated: $(date +%Y-%m-%d)*
*Exarp v0.2.0*
