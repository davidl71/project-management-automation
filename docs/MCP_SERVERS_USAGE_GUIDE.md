# MCP Servers Usage Guide

> 💡 **AI Assistant Hint:** This guide provides prompting patterns to maximize the exarp_pma and interactive MCP servers.

**Date**: 2025-11-27  
**Status**: ✅ Complete  
**Trusted Advisor**: 📚 Confucius - *"Tell me and I forget. Show me and I remember. Involve me and I understand."*

---

## Quick Reference

### Most Useful Prompts by Situation

| Situation | Prompt | What Happens |
|-----------|--------|--------------|
| Start of day | "Check project health and give me a summary" | Reads scorecard, consults advisor, reports blockers |
| Before coding | "What do I need to know about task X?" | Recalls memories, shows dependencies, context |
| Stuck on bug | "Help me debug this import error" | Uses problem categories, searches memories |
| End of session | "Save what we learned today" | Creates memory entries, summarizes session |
| Sprint planning | "Analyze task alignment and find duplicates" | Runs alignment check, duplicate detection |
| Security review | "Scan for vulnerabilities" | Runs security scan, Dependabot check |
| Need wisdom | "What would the advisor say about testing?" | Consults Stoic advisor for testing guidance |
| Deployment | "Is the project production ready?" | Checks scorecard, CI/CD, security |

---

## Workflow-Based Prompting

### 1. Daily Check-in Workflow

Start your day with these prompts:

```
"Good morning! Check the project health and tell me what needs attention."
```
**What happens:** AI reads `automation://scorecard`, identifies blockers, consults daily_checkin advisor (Pistis Sophia).

```
"What's the testing situation? Are we production ready?"
```
**What happens:** AI checks testing metrics, runs coverage analysis if needed, provides Stoic advisor wisdom.

```
"Show me any security alerts"
```
**What happens:** AI fetches `automation://status`, runs `security(action="alerts")`, summarizes vulnerabilities.

```
"What tasks are waiting for clarification?"
```
**What happens:** AI calls `task_workflow(action="clarify", sub_action="list")`, shows tasks needing input.

---

### 2. Sprint Planning Workflow

Use these prompts for effective sprint planning:

```
"Let's do sprint planning. Start by analyzing our task alignment."
```
**What happens:** AI runs `analyze_alignment(action="todo2")`, scores tasks against goals, creates follow-up tasks.

```
"Find any duplicate tasks in the backlog"
```
**What happens:** AI runs `task_analysis(action="duplicates")`, identifies similar tasks with similarity scores.

```
"Which tasks should I work on next?"
```
**What happens:** AI calls `get_next_task_recommendation()`, considers dependencies, priorities, complexity.

```
"Generate tasks from this PRD: [paste PRD content]"
```
**What happens:** AI runs `parse_prd(prdContent="...")`, creates structured tasks with dependencies.

```
"Switch to sprint planning mode so we can focus"
```
**What happens:** AI calls `focus_mode(mode="sprint_planning")`, reduces visible tools by ~63%.

---

### 3. Development Workflow

During active development:

```
"I'm starting work on task T-123. What context do I need?"
```
**What happens:** AI runs `memory(action="recall", task_id="T-123")`, fetches related memories, shows dependencies.

```
"Before I implement this, are there any similar patterns in the codebase?"
```
**What happens:** AI searches memories for architecture decisions, checks for existing implementations.

```
"Save this decision: we chose approach X because Y"
```
**What happens:** AI runs `memory(action="save", title="...", content="...", category="architecture")`.

```
"Switch to development mode"
```
**What happens:** AI calls `focus_mode(mode="development")`, enables balanced toolset (25 tools, 52% reduction).

```
"I need the advisor tools too"
```
**What happens:** AI calls `focus_mode(enable_group="advisors")`, adds advisor tools to current mode.

---

### 4. Debugging Workflow

When troubleshooting issues:

```
"I'm getting this error: [paste error]. Help me debug it."
```
**What happens:** AI checks `automation://problem-categories`, matches error pattern, suggests fixes.

```
"Have we seen this kind of error before?"
```
**What happens:** AI runs `memory(action="search", query="...", category="debug")`, finds past solutions.

```
"Run the tests and tell me what's failing"
```
**What happens:** AI runs `testing(action="run")`, analyzes failures, suggests fixes.

```
"Switch to debugging mode"
```
**What happens:** AI calls `focus_mode(mode="debugging")`, enables memory + testing tools (67% reduction).

```
"Save the fix we found for future reference"
```
**What happens:** AI runs `memory(action="save", category="debug", title="Fix: ...")`.

---

### 5. Code Review Workflow

For reviewing code quality:

```
"Run the linter and analyze the results"
```
**What happens:** AI runs `lint(action="run", analyze=true)`, provides categorized issues with hints.

```
"Check test coverage for the recent changes"
```
**What happens:** AI runs `testing(action="coverage")`, shows coverage percentages, identifies gaps.

```
"Does this code meet our definition of done?"
```
**What happens:** AI runs `health(action="dod", task_id="...")`, validates completion criteria.

```
"Switch to code review mode"
```
**What happens:** AI calls `focus_mode(mode="code_review")`, enables testing + health tools (81% reduction).

---

### 6. Security Review Workflow

For security assessments:

```
"Do a full security review"
```
**What happens:** AI runs `security(action="report")`, combines pip-audit + Dependabot alerts.

```
"Check for vulnerable dependencies"
```
**What happens:** AI runs `security(action="scan")`, performs local pip-audit scan.

```
"What does the BOFH advisor say about our security?"
```
**What happens:** AI runs `consult_advisor(metric="security")`, returns BOFH wisdom.

```
"Switch to security mode"
```
**What happens:** AI calls `focus_mode(mode="security_review")`, reduces to security-focused tools (77% reduction).

---

## Human-in-the-Loop Patterns

### Single Confirmation

When you want the AI to ask before proceeding:

```
"Before making any changes, ask me to confirm"
```
**What happens:** AI uses `request_user_input()` with predefined options before actions.

**Example interaction:**
```
AI: "I found 3 duplicate tasks. Should I merge them?"
    Options: [Yes, merge them] [No, show me first] [Skip]
User: Clicks "Show me first"
AI: Shows detailed comparison
```

---

### Multi-Question Sessions

For gathering multiple inputs efficiently:

```
"Let's go through the sprint backlog together. I have several questions."
```
**What happens:** AI opens intensive chat session, asks questions sequentially, closes when done.

**Example sequence:**
```
AI: [Opens intensive chat: "Sprint Planning"]
AI: "Priority for task 'Add dark mode' (1-10)?"
User: 7
AI: "Estimated hours for this task?"
User: 4
AI: "Any blockers?"
User: Need design specs
AI: [Closes session, updates tasks]
```

---

### Completion Notifications

Get notified when long operations complete:

```
"Run the full test suite and notify me when done"
```
**What happens:** AI runs tests, sends OS notification via `message_complete_notification()`.

```
"Do the nightly automation and ping me when finished"
```
**What happens:** AI runs `run_automation(action="nightly")`, notifies on completion.

---

## Example Prompts by Category

### Health and Status (10 prompts)

1. `"Check project health"` - Overall scorecard
2. `"Is the project production ready?"` - Checks blockers
3. `"What's our test coverage?"` - Testing metrics
4. `"Show documentation health"` - Docs quality score
5. `"Check git working copy status"` - Uncommitted changes
6. `"Validate CI/CD workflows"` - GitHub Actions health
7. `"What's the current focus mode?"` - Tool visibility status
8. `"How many tools am I using?"` - Usage statistics
9. `"Give me the daily briefing"` - Combined health summary
10. `"What advisors are available?"` - List all 15 advisors

### Task Management (10 prompts)

1. `"List all pending tasks"` - Task overview
2. `"Find duplicate tasks"` - Duplicate detection
3. `"Analyze task alignment"` - Goal alignment
4. `"What tasks need clarification?"` - Awaiting input
5. `"Recommend next task"` - AI suggestion
6. `"Sync TODO.md with Todo2"` - Markdown sync
7. `"Bulk approve review tasks"` - Batch approval
8. `"Find tasks from code comments"` - TODO/FIXME discovery
9. `"Analyze task complexity"` - Breakdown suggestions
10. `"Show task hierarchy"` - Tree view

### Security (6 prompts)

1. `"Scan for vulnerabilities"` - pip-audit scan
2. `"Check Dependabot alerts"` - GitHub security alerts
3. `"Full security report"` - Combined analysis
4. `"What would BOFH say about this?"` - Security advisor
5. `"Are there any critical vulnerabilities?"` - Priority filter
6. `"Security status for deployment"` - Pre-deploy check

### Testing (6 prompts)

1. `"Run the tests"` - Execute test suite
2. `"What's test coverage?"` - Coverage analysis
3. `"Which modules need tests?"` - Coverage gaps
4. `"Fix the failing tests"` - Auto-fix attempt
5. `"What would Stoic say about testing?"` - Testing advisor
6. `"Generate tests for this module"` - Test creation

### Advisor Wisdom (6 prompts)

1. `"Consult the advisor about testing"` - Stoic guidance
2. `"What does Art of War say about completion?"` - Strategy
3. `"Wisdom for sprint planning"` - Planning advice
4. `"What should I consider for documentation?"` - Confucius
5. `"End of day reflection"` - Session wisdom
6. `"Generate an advisor briefing"` - Combined insights

### Interactive Confirmations (6 prompts)

1. `"Ask me before making changes"` - Single confirmation
2. `"Let's discuss the options"` - Multi-question session
3. `"Notify me when tests complete"` - Completion alert
4. `"Walk me through the decisions"` - Step-by-step
5. `"I need to approve each step"` - Granular control
6. `"Ping me when the analysis is done"` - Background task

---

## Anti-Patterns to Avoid

### Don't: Be Vague About What You Want

```
❌ "Check stuff"
✅ "Check project health and security status"
```

### Don't: Ask Multiple Unrelated Things

```
❌ "Check security, run tests, plan sprint, and fix bugs"
✅ "Let's start with security. Check for vulnerabilities."
```

### Don't: Forget Context

```
❌ "What should I do next?"
✅ "What should I do next on task T-123?"
```

### Don't: Skip the Memory System

```
❌ [Fix a bug and move on]
✅ "Save this fix: [description]" after solving problems
```

### Don't: Use Wrong Mode for Task

```
❌ [Use security tools in daily_checkin mode - they're hidden]
✅ "Switch to security mode" first, then scan
```

### Don't: Ignore Advisor Guidance

```
❌ [Jump straight to coding]
✅ "What does the advisor say about this metric?" first
```

---

## Mode Selection Guide

| Your Task | Best Mode | Prompt |
|-----------|-----------|--------|
| Morning standup | daily_checkin | "Switch to daily check-in mode" |
| Security audit | security_review | "Switch to security mode" |
| Backlog grooming | task_management | "Switch to task management mode" |
| PR review | code_review | "Switch to code review mode" |
| Sprint planning | sprint_planning | "Switch to sprint planning mode" |
| Bug fixing | debugging | "Switch to debugging mode" |
| General work | development | "Switch to development mode" |
| Full access | all | "Enable all tools" |

---

## Power User Tips

### 1. Chain Operations

```
"Check health, then if testing is below 50%, consult the Stoic advisor"
```

### 2. Save Context Early

```
"Before we start, recall what we know about [topic]"
```

### 3. Use Focus Modes Aggressively

```
"Switch to [mode] so we can focus" - Reduces token usage significantly
```

### 4. Leverage Resources Passively

The AI automatically reads resources like `automation://scorecard` when relevant. You don't need to explicitly request them.

### 5. Request Notifications for Long Tasks

```
"Run [long operation] and notify me when done so I can do other work"
```

### 6. Use Intensive Chat for Decisions

```
"I have 5 tasks to prioritize. Let's go through them together."
```

---

## Related Documentation

- [MCP_SERVERS_DISCOVERY_REPORT.md](MCP_SERVERS_DISCOVERY_REPORT.md) - Full discovery details
- [DYNAMIC_TOOL_LOADING.md](DYNAMIC_TOOL_LOADING.md) - Focus mode deep dive
- [AI_SESSION_MEMORY.md](AI_SESSION_MEMORY.md) - Memory system reference
- [CURSOR_IDE_BEST_PRACTICES.md](CURSOR_IDE_BEST_PRACTICES.md) - General Cursor tips

---

## Quick Start Checklist

- [ ] **First session**: "Check project health and tell me what needs attention"
- [ ] **Pick a mode**: "Switch to [task_management/development/debugging] mode"
- [ ] **Recall context**: "What do we know about [topic/task]?"
- [ ] **Save discoveries**: "Save this: [insight]"
- [ ] **Get wisdom**: "What does the advisor say about [metric]?"
- [ ] **Confirm actions**: "Ask me before making changes"
- [ ] **Stay notified**: "Notify me when done"

---

*Effective prompting is a skill. Start with these patterns and adapt them to your workflow.*

