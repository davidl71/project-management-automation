# Persona Alignment Guide

> **How to align tasks and user stories with target personas**

*Generated: 2025-11-26*

---

## 🎯 Quick Reference: Persona → Trusted Advisor → Tools

| Persona | Trusted Advisor | Primary Tools | Key Metrics |
|---------|-----------------|---------------|-------------|
| 💻 **Developer** | Tao of Programming | `project_scorecard`, `list_tasks_awaiting_clarification` | Complexity <10, Coverage >80% |
| ⚔️ **Project Manager** | Art of War (Sun Tzu) | `project_overview`, `detect_duplicate_tasks`, `analyze_todo2_alignment` | Blocked: 0, First Pass Yield >85% |
| 🏛️ **Code Reviewer** | Stoic | `project_scorecard`, complexity tools | CC <10 new, Bandit: 0 |
| 🔮 **Architect** | Enochian | `project_scorecard --deep`, coupling analysis | Complexity <5 avg, Dead Code <5% |
| 😈 **Security Engineer** | BOFH | `scan_dependency_security`, `project_scorecard` | Critical Vulns: 0, Score >90% |
| 🏛️ **QA Engineer** | Stoic | `run_tests`, `analyze_test_coverage` | Coverage >80%, Passing: 100% |
| 📜 **Executive** | Pistis Sophia | `project_overview`, `project_scorecard` | Health >75%, Alignment % |
| 🎓 **Technical Writer** | Confucius | `check_documentation_health` | Broken Links: 0, Docstrings >90% |

---

## 📋 User Story Alignment Matrix

### How to Determine Target Persona for a Task

**Step 1: Identify Keywords**

| Keywords in Task | Primary Persona | Secondary Persona |
|-----------------|-----------------|-------------------|
| `api`, `endpoint`, `mcp`, `tool`, `implement`, `code` | Developer | Architect |
| `sprint`, `planning`, `status`, `delivery`, `blockers` | Project Manager | Executive |
| `pr`, `review`, `approve`, `merge`, `quality` | Code Reviewer | Developer |
| `architecture`, `coupling`, `patterns`, `design` | Architect | Developer |
| `security`, `vulnerability`, `cve`, `audit`, `scan` | Security Engineer | Code Reviewer |
| `test`, `coverage`, `defect`, `validation`, `qa` | QA Engineer | Developer |
| `status`, `summary`, `overview`, `report`, `dashboard` | Executive | Project Manager |
| `doc`, `documentation`, `readme`, `guide`, `tutorial` | Technical Writer | Developer |

**Step 2: Map to Advisor for Wisdom**

```python
# Example: When creating/reviewing PRD user stories
if "security" in task_content:
    consult_advisor(metric="security")  # BOFH will provide paranoid wisdom
elif "test" in task_content:
    consult_advisor(metric="testing")   # Stoics teach discipline
elif "documentation" in task_content:
    consult_advisor(metric="documentation")  # Confucius teaches
```

---

## 🔄 Workflow-Based Alignment

### Developer Tasks

**When to create:**
- New feature implementations
- Bug fixes
- API/tool development
- Code refactoring

**User Story Format:**
```
As a Developer (Daily Contributor),
I want [task_name],
So that I can write quality code and contribute effectively.
```

**Trusted Advisor Wisdom:**
> *"Let code emerge naturally, like water finding its path."* — Tao of Programming

**Alignment Check:**
- [ ] Does this help developers stay unblocked?
- [ ] Will this improve code quality metrics?
- [ ] Is complexity under control (<10)?

---

### Project Manager Tasks

**When to create:**
- Sprint planning items
- Delivery tracking
- Blocker resolution
- Status reporting

**User Story Format:**
```
As a Project Manager (Delivery Focus),
I want [task_name],
So that I can track progress and ensure delivery.
```

**Trusted Advisor Wisdom:**
> *"Know when to attack and when to wait. Sprints are campaigns."* — Sun Tzu

**Alignment Check:**
- [ ] Does this reduce blocked tasks?
- [ ] Will this improve delivery predictability?
- [ ] Does this help prioritize aligned work?

---

### Security Engineer Tasks

**When to create:**
- Vulnerability scanning
- Security audits
- CVE remediation
- Access control

**User Story Format:**
```
As a Security Engineer (Risk Management),
I want [task_name],
So that I can identify and mitigate security risks.
```

**Trusted Advisor Wisdom:**
> *"Assume users will break everything. Plan accordingly."* — BOFH

**Alignment Check:**
- [ ] Does this reduce critical/high vulnerabilities?
- [ ] Will this improve security score?
- [ ] Is paranoid security thinking applied?

---

### QA Engineer Tasks

**When to create:**
- Test coverage improvement
- Quality validation
- Defect analysis
- Test automation

**User Story Format:**
```
As a QA Engineer (Quality Assurance),
I want [task_name],
So that I can ensure product quality through testing.
```

**Trusted Advisor Wisdom:**
> *"Tests reveal truth. Accept harsh feedback with equanimity."* — Stoics

**Alignment Check:**
- [ ] Does this improve test coverage (>80%)?
- [ ] Will tests provide honest feedback?
- [ ] Is first pass yield improving?

---

### Technical Writer Tasks

**When to create:**
- Documentation updates
- README improvements
- API documentation
- User guides

**User Story Format:**
```
As a Technical Writer (Documentation),
I want [task_name],
So that I can create and maintain clear documentation.
```

**Trusted Advisor Wisdom:**
> *"Teaching and transmitting wisdom is a sacred duty."* — Confucius

**Alignment Check:**
- [ ] Are broken links eliminated?
- [ ] Is docstring coverage improving?
- [ ] Will future developers understand this?

---

## 📊 PRD Alignment Validation

### Checking Task ↔ PRD Alignment

**1. Every task should trace to a PRD section:**

| Task Type | PRD Section | Validation |
|-----------|-------------|------------|
| Feature | User Stories | US-X references match |
| Infrastructure | Technical Requirements | Framework/pattern alignment |
| Quality | Success Metrics | Metric targets defined |
| Risk mitigation | Risks & Dependencies | Risk addressed |

**2. Use `analyze_todo2_alignment` tool:**

```bash
/exarp/analyze_todo2_alignment
```

This tool checks:
- Task keywords vs PROJECT_GOALS.md phases
- Task tags vs strategic priorities
- Completion status vs phase milestones

**3. Cross-reference with PRD personas:**

For each user story in PRD:
1. Identify target persona
2. Check persona-specific metrics
3. Validate trusted advisor alignment
4. Ensure workflow coverage

---

## 🔗 Integration with Exarp Tools

### Tool → Persona Mapping

| Tool | Primary Persona(s) | Use Case |
|------|-------------------|----------|
| `generate_prd` | All | Creates persona-aligned PRD |
| `project_scorecard` | All | Health metrics per persona |
| `project_overview` | Executive, PM | High-level status |
| `analyze_todo2_alignment` | PM, Developer | Task ↔ Goal alignment |
| `scan_dependency_security` | Security Engineer | Vulnerability detection |
| `check_documentation_health` | Tech Writer | Doc quality |
| `run_tests` | QA Engineer | Test execution |
| `detect_duplicate_tasks` | PM | Backlog cleanup |

### Advisor Consultations

```python
# Consult advisor for specific metrics
consult_advisor(metric="security", score=75.0)      # BOFH
consult_advisor(metric="testing", score=80.0)       # Stoic
consult_advisor(metric="documentation", score=65.0) # Confucius
consult_advisor(metric="alignment", score=90.0)     # Tao
consult_advisor(metric="completion", score=70.0)    # Art of War

# Consult for workflow stages
consult_advisor(stage="planning")       # Sun Tzu (strategy)
consult_advisor(stage="review")         # Stoic (harsh truths)
consult_advisor(stage="debugging")      # BOFH (paranoid)
consult_advisor(stage="retrospective")  # Confucius (learning)
```

---

## 📝 Creating Aligned Tasks

### Template for New Tasks

```markdown
**Task:** [Clear, actionable title]

**Target Persona:** [Developer/PM/Security/QA/Architect/Executive/TechWriter]

**Trusted Advisor:** [Advisor name] - "[Relevant quote]"

**User Story:**
As a [Persona] ([Role]),
I want [specific action],
So that [measurable benefit].

**Acceptance Criteria:**
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Persona-specific metric target]

**Tags:** [persona-relevant tags]
```

### Example: Security Task

```markdown
**Task:** Scan dependencies for CVE-2024-XXXX

**Target Persona:** Security Engineer (Risk Management)

**Trusted Advisor:** BOFH - "Assume the worst. Verify everything."

**User Story:**
As a Security Engineer (Risk Management),
I want to scan all dependencies for the new CVE,
So that I can identify and mitigate security risks.

**Acceptance Criteria:**
- [ ] All dependencies scanned
- [ ] Critical vulnerabilities: 0
- [ ] Remediation plan for any findings
- [ ] Security score maintained >90%

**Tags:** security, vulnerability, audit, risk
```

---

## 🎯 Summary: Alignment Checklist

Before marking any task as complete:

- [ ] **Persona identified** - Who is this for?
- [ ] **Advisor consulted** - What wisdom applies?
- [ ] **Metrics met** - Are targets achieved?
- [ ] **PRD traced** - Does this link to user stories?
- [ ] **Workflow aligned** - Does this fit the persona's workflow?

---

*This guide ensures all tasks and user stories align with defined personas, their trusted advisors, and project goals.*

