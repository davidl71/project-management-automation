# Context Priming Guide

> 💡 **AI Assistant Hint:** This guide explains how to set up your project so AI agents automatically have the context they need to use EXARP effectively.

**Date**: 2025-11-27  
**Status**: ✅ Complete  
**Trusted Advisor**: 🎓 Confucius - *"By three methods we may learn wisdom: reflection, imitation, and experience."*

---

## What is Context Priming?

Context priming is the practice of creating specific files in your project that AI agents automatically read to understand:

1. **Project Structure** - What the project does and how it's organized
2. **User Preferences** - Your coding style, conventions, and workflow preferences
3. **Session Memory** - What was learned in previous sessions
4. **Available Tools** - What MCP tools are available and how to use them

When properly primed, an AI agent starts every conversation with relevant context instead of asking "what does this project do?"

---

## Files to Create in Your Project

### Required Files

| File | Purpose | Location |
|------|---------|----------|
| `.cursor/mcp.json` | Configure MCP servers | Project root |
| `openmemory.md` | Project knowledge guide | Project root |

### Recommended Files

| File | Purpose | Location |
|------|---------|----------|
| `.cursor/rules/*.mdc` | AI behavior rules | `.cursor/rules/` |
| `.cursor/prompts/*.md` | Reusable prompt templates | `.cursor/prompts/` |
| `.exarp/` | Auto-created memory storage | Project root |

---

## Step 1: Configure MCP Servers

Create `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "exarp_pma": {
      "command": "uvx",
      "args": ["exarp"],
      "description": "Project management automation"
    },
    "interactive": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-interactive"],
      "description": "Human-in-the-loop confirmations"
    }
  }
}
```

**For development mode** (hot-reload enabled):

```json
{
  "mcpServers": {
    "exarp_pma": {
      "command": "python3",
      "args": ["-m", "project_management_automation.server"],
      "env": {
        "EXARP_DEV_MODE": "1"
      }
    }
  }
}
```

---

## Step 2: Create the OpenMemory Guide

Create `openmemory.md` in your project root. This is the **most important file** for context priming:

```markdown
# Project Memory Guide - [Your Project Name]

## Overview
[Brief description of what your project does - 2-3 sentences]

## User Defined Namespaces
- [namespace1] (e.g., frontend, backend, api)
- [namespace2]
- [namespace3]

## Architecture
[Key architectural decisions and patterns]

## Components
[List major components and their purposes]

## Patterns
[Common patterns used in the codebase]

## Important Decisions
[Key technical decisions and why they were made]
```

**Example from a real project:**

```markdown
# Project Memory Guide - Project Management Automation

## Overview
Automation tools for project management workflows including task management, 
CI/CD validation, documentation health, and developer productivity features.

## User Defined Namespaces
- research
- automation
- integrations

## Architecture
- MCP server built with FastMCP
- Tools organized by category in tools/ directory
- Resources expose passive context via automation:// URIs

## Components
- server.py - Main MCP server entry point
- tools/ - Tool implementations
- resources/ - Resource handlers
- .exarp/memories/ - Persistent memory storage

## Patterns
- Scripts ensure repo root is on sys.path before importing
- Todo2 tasks carry project_id for multi-project filtering
```

---

## Step 3: Add Cursor Rules

Create `.cursor/rules/` directory and add rule files that control AI behavior.

### Essential Rule: `openmemory.mdc`

Create `.cursor/rules/openmemory.mdc`:

```markdown
---
description: "Memory-first development rules"
globs: ["**/*"]
alwaysApply: true
---

# Memory Integration

**project_id:** [your-github-org]/[your-repo]

## Memory-First Development

Before ANY code implementation:
1. Search existing memories for related context
2. Check openmemory.md for patterns and decisions
3. After completing work, store what you learned

## Memory Types
- **component** - What exists and where
- **implementation** - How something was built
- **debug** - How a problem was solved
- **preference** - User coding preferences
- **architecture** - System design decisions

## When to Store Memories
- Solved a non-trivial bug → Store as debug memory
- Made an architecture decision → Store as architecture memory
- Discovered a pattern → Update openmemory.md
- Learned user preference → Store as preference memory
```

### Project Rules: `project-development.mdc`

Create `.cursor/rules/project-development.mdc`:

```markdown
---
description: "Project development guidelines"
globs: ["**/*.py", "**/*.ts", "**/*.js"]
alwaysApply: true
---

# [Project Name] Development Rules

## Code Style
- [Your code style preferences]
- [Testing requirements]
- [Documentation standards]

## Available Tools
When working on this project, use EXARP tools:
- `health(action="server")` - Check project health
- `memory(action="search")` - Find related context
- `memory(action="save")` - Store new discoveries
- `consult_advisor(metric="...")` - Get wisdom

## Workflow
1. Start sessions with health check
2. Search memories before coding
3. Store learnings after completing work
```

---

## Step 4: Create Prompt Templates

Create `.cursor/prompts/` directory with reusable prompts:

### `start-day.md`

```markdown
# Start of Day Workflow

Help me start my day with a project overview.

## Steps
1. Check project health scorecard
2. List tasks awaiting clarification
3. Suggest top 3 tasks based on priority
4. Note any security alerts

## Questions to Answer
- What's the project health?
- What's blocking progress?
- What should I work on first?
```

### `quick-health.md`

```markdown
# Quick Health Check

Run a quick project health check.

## Steps
1. Get project scorecard
2. Highlight scores below 70%
3. List top 3 recommended actions
4. Note any critical blockers

## Expected Output
- Overall health score
- Component breakdown
- Priority actions
```

### `save-session.md`

```markdown
# End of Session

Save what we learned today.

## Steps
1. Summarize key discoveries
2. Store important memories
3. Update openmemory.md if needed
4. Note any unfinished work

## Memory Categories
- debug - Problems solved
- architecture - Design decisions
- implementation - How things were built
- preference - Workflow preferences
```

---

## Step 5: Let EXARP Create Memories

EXARP automatically creates the `.exarp/` directory structure:

```
.exarp/
├── memories/           # AI session memories (JSON files)
│   ├── abc123.json    # Debug memory
│   ├── def456.json    # Architecture memory
│   └── ...
└── advisor_logs/       # Advisor consultation history
    └── consultations_2025-11.jsonl
```

### Memory File Format

Each memory is stored as a JSON file:

```json
{
  "id": "850a3f80-1b13-4797-9211-c4ff9543175b",
  "title": "Fix: Import error in server.py",
  "content": "Fixed by adding __init__.py to package directory...",
  "category": "debug",
  "linked_tasks": ["T-123"],
  "metadata": {},
  "created_at": "2025-11-26T12:33:16.312649",
  "session_date": "2025-11-26"
}
```

---

## EXARP Memory Tool Reference

EXARP provides a unified `memory` tool with multiple actions:

### Save a Memory

```
memory(action="save", title="...", content="...", category="debug|research|architecture|preference|insight", task_id="optional")
```

**Example:**
```
"Save a debug memory: Fixed import error by adding __init__.py"
```

The AI calls:
```python
memory(
    action="save",
    title="Fix: Import error in server.py",
    content="Fixed by adding __init__.py to the package directory. Root cause was missing package marker.",
    category="debug",
    task_id="T-123"  # optional
)
```

### Recall Memories for a Task

```
memory(action="recall", task_id="...")
```

Returns all memories linked to that task, grouped by category.

### Search Memories

```
memory(action="search", query="...", category="optional", limit=10)
```

**Example:**
```
"Search memories for import errors"
```

### Memory Categories

| Category | Use For | Example Title |
|----------|---------|---------------|
| `debug` | Bug fixes, error solutions | "Fix: ModuleNotFoundError" |
| `research` | Pre-implementation findings | "Research: MCP vs REST comparison" |
| `architecture` | Design decisions, patterns | "Architecture: Event-driven messaging" |
| `preference` | User coding style, workflow | "Preference: Use Black formatter" |
| `insight` | Sprint patterns, observations | "Sprint: Testing blockers pattern" |

---

## Auto-Context from MCP Resources

EXARP exposes MCP resources that provide **passive context**—the AI reads them automatically without explicit tool calls.

### How Resources Work

When you ask about project health, the AI automatically reads `automation://scorecard`. You don't need to say "fetch the scorecard resource."

### Key Resources for Context Priming

| Resource URI | When Auto-Read | What It Provides |
|--------------|----------------|------------------|
| `automation://memories/recent` | Session start | Last 24 hours of memories |
| `automation://wisdom` | Wisdom queries | Memories + advisor consultations |
| `automation://scorecard` | Health queries | Project metrics, blockers |
| `automation://tasks` | Task queries | Full task database |
| `automation://advisors` | Advisor queries | 15 philosophical advisors |
| `automation://models` | Model selection | AI model recommendations |
| `automation://problem-categories` | Debug queries | 8 auto-fixable error patterns |

### Leveraging Resources in Prompts

**Implicit (AI reads automatically):**
```
"What's the project health?"
→ AI reads automation://scorecard
```

**Explicit (for specific data):**
```
"Read the recent memories and summarize what we worked on"
→ AI reads automation://memories/recent
```

**Combined wisdom:**
```
"Give me wisdom about testing"
→ AI reads automation://wisdom (memories + consultations)
→ AI consults Stoic advisor
```

---

## Avoiding Memory Duplication

EXARP's automation tools automatically create memories (scorecards, security scans, etc.). To avoid clutter:

### Best Practices

1. **Don't manually save automated results**
   ```
   ❌ "Check health and save the results"
   ✅ "Check health" (auto-saves if significant)
   ```

2. **Be specific with manual saves**
   ```
   ❌ "Save this"
   ✅ "Save as debug memory: [specific insight]"
   ```

3. **Link to tasks when relevant**
   ```
   "Save this fix and link it to task T-123"
   ```

4. **Use search before saving**
   ```
   "Search memories for [topic] before I save a new one"
   ```

### Memory Cleanup

If memories accumulate (especially auto-generated scorecards):

```
"Show me recent memories and identify duplicates"
```

The `task_analysis(action="duplicates")` tool can help identify similar memories.

---

## Interactive Confirmations for Memory

Use the interactive MCP server to confirm before saving important memories:

### Single Confirmation

```
"Before saving this architecture decision, ask me to confirm"
```

The AI uses:
```python
request_user_input(
    "Save architecture decision: 'Use event-driven messaging'?",
    predefinedOptions=["Yes, save it", "No, skip", "Edit first"]
)
```

### Multi-Question Memory Session

```
"Let's categorize and save what we learned today. Walk me through each item."
```

The AI opens an intensive chat:
```python
start_intensive_chat("Session Memory Review")
ask_intensive_chat("Save 'Fixed import error' as debug memory?", ["Yes", "No"])
ask_intensive_chat("Link to which task?", ["T-123", "T-456", "None"])
ask_intensive_chat("Save 'Architecture: Event system' as architecture?", ["Yes", "No"])
stop_intensive_chat()
```

### Notify When Memories Are Saved

```
"Save this and notify me when done"
```

The AI saves and sends:
```python
message_complete_notification("Memory saved: Fix import error (debug)")
```

---

## Cursor Prompts Integration

The `.cursor/prompts/` directory contains reusable prompt templates. These work with EXARP tools.

### How Cursor Prompts Work

1. Create `.md` files in `.cursor/prompts/`
2. Reference them in chat with `@prompt-name`
3. They expand into full prompts with EXARP tool hints

### Example: Enhanced Start-Day Prompt

Create `.cursor/prompts/start-day.md`:

```markdown
# Start of Day Workflow

Help me start my day with project context.

## Steps
1. Read `automation://memories/recent` for yesterday's context
2. Run `health(action="server")` for project health
3. Run `task_workflow(action="clarify", sub_action="list")` for blockers
4. Run `consult_advisor(stage="daily_checkin")` for wisdom
5. Suggest top 3 tasks via `get_next_task_recommendation()`

## Expected Output
- Yesterday's key learnings
- Project health score
- Tasks needing clarification
- Advisor wisdom for the day
- Recommended tasks to work on
```

### Example: Save-Session Prompt

Create `.cursor/prompts/end-session.md`:

```markdown
# End of Session

Save learnings and context for tomorrow.

## Steps
1. Summarize what was accomplished
2. For each significant learning:
   - Use `memory(action="save", category="...")` 
   - Link to task if applicable
3. Update `openmemory.md` if new patterns discovered
4. Use `request_user_input()` to confirm each save
5. Send `message_complete_notification()` when done

## Memory Categories to Consider
- debug: Bugs fixed, error solutions
- architecture: Design decisions made
- implementation: How features were built
- insight: Patterns observed
```

### Example: Debug-With-Context Prompt

Create `.cursor/prompts/debug.md`:

```markdown
# Debug with Memory Context

Help me debug an issue using past learnings.

## Steps
1. Run `memory(action="search", query="[error type]", category="debug")`
2. Check `automation://problem-categories` for auto-fix patterns
3. If pattern found, apply fix
4. If not found, investigate and save solution:
   - Use `memory(action="save", category="debug")`
   - Include root cause and fix
5. Link to task if applicable

## After Fixing
Always save the solution for future reference!
```

### Using Prompts in Chat

```
@start-day
→ Expands to full workflow with EXARP tools

@debug This import error: ModuleNotFoundError
→ Searches memories, checks patterns, saves fix
```

---

## How to Prompt for Best Results

### Starting a New Session

```
"Good morning! Check project health and recall any recent memories about [topic]"
```

This triggers:
1. Reads `automation://scorecard` for health
2. Searches memories for the topic
3. Consults the daily_checkin advisor

### Before Implementing a Feature

```
"Before I start on [feature], what do we know about it? 
Search memories and check if there are any related patterns."
```

This triggers:
1. Searches memories for related context
2. Checks `openmemory.md` patterns
3. Shows any linked tasks

### After Completing Work

```
"Save what we learned: [brief description]"
```

This triggers:
1. Creates a memory with appropriate category
2. Updates `openmemory.md` if relevant
3. Links to task if applicable

### When Debugging

```
"Help me debug [error]. First search memories for similar issues."
```

This triggers:
1. Searches debug memories
2. Checks problem categories for auto-fix
3. Stores the solution when found

---

## Complete Project Setup Checklist

```
your-project/
├── .cursor/
│   ├── mcp.json                    # [Required] MCP server config
│   ├── rules/
│   │   ├── openmemory.mdc          # [Recommended] Memory rules
│   │   └── project-development.mdc # [Recommended] Dev rules
│   └── prompts/
│       ├── start-day.md            # [Optional] Daily prompt
│       ├── quick-health.md         # [Optional] Health check
│       └── save-session.md         # [Optional] End session
├── openmemory.md                   # [Required] Project knowledge guide
├── .exarp/                         # [Auto-created] Memory storage
│   ├── memories/
│   └── advisor_logs/
└── ... (your project files)
```

---

## Priming Prompts for New Projects

When starting with EXARP on a new project, use these prompts:

### First Session: Deep Dive

```
"This is a new project. Please:
1. Analyze the project structure
2. Create an initial openmemory.md
3. Store key findings as memories
4. Set up the context for future sessions"
```

### After Deep Dive: Regular Sessions

```
"Start by reading openmemory.md and checking project health."
```

### Teaching EXARP Your Preferences

```
"Remember: I prefer [your preference]. Store this as a user preference."
```

Examples:
- "Remember: I prefer pytest over unittest"
- "Remember: I use Black for formatting with 88 char lines"
- "Remember: I want verbose logging in debug mode"

---

## MCP Resources for Context

EXARP exposes 15 MCP resources that provide automatic context. The AI reads these passively without you needing to request them explicitly.

### Core Context Resources

| Resource | Auto-Read When | What You Get |
|----------|----------------|--------------|
| `automation://memories/recent` | Session start | Last 24h memories (recent fixes, decisions, insights) |
| `automation://wisdom` | "What do we know about..." | Combined memories + advisor consultation history |
| `automation://scorecard` | Health/status queries | Overall score, blockers, recommendations |
| `automation://tasks` | Task/planning queries | Full Todo2 database with status, priorities |

### Discovery Resources

| Resource | Auto-Read When | What You Get |
|----------|----------------|--------------|
| `automation://tools` | Tool questions | All 23+ tools with parameters and descriptions |
| `automation://advisors` | Wisdom queries | 15 advisors mapped to metrics/tools/stages |
| `automation://models` | Model selection | AI model recommendations by task type |
| `automation://problem-categories` | Debug queries | 8 auto-fixable error patterns |

### System Resources

| Resource | Auto-Read When | What You Get |
|----------|----------------|--------------|
| `automation://status` | Server health | Version, operational status, tool counts |
| `automation://history` | Review past actions | Automation run history |
| `automation://agents` | Multi-agent tracking | Registered AI agents |
| `automation://cache` | Performance queries | Caching statistics |
| `automation://linters` | Code quality setup | Available linter configurations |
| `automation://tts-backends` | Podcast queries | Text-to-speech backends |
| `automation://memories` | Full memory access | Complete memory database (use recent for sessions) |

---

## Troubleshooting Context Issues

### "Agent doesn't remember previous sessions"

**Check:**
1. Is `.exarp/memories/` directory present?
2. Are memory files being created?
3. Did you prompt to save memories?

**Fix:**
```
"Search memories for [topic]" - explicitly recall
"Save this as a memory" - explicitly store
```

### "Agent doesn't follow project conventions"

**Check:**
1. Is `.cursor/rules/` directory present?
2. Are rule files using `.mdc` extension?
3. Is `alwaysApply: true` set in frontmatter?

**Fix:** Create rule file with `globs: ["**/*"]` and `alwaysApply: true`

### "Agent asks basic questions about project"

**Check:**
1. Is `openmemory.md` present and populated?
2. Does it have Overview, Architecture, Components sections?

**Fix:**
```
"Please analyze this project and update openmemory.md"
```

---

## Related Documentation

- [MCP_SERVERS_DISCOVERY_REPORT.md](MCP_SERVERS_DISCOVERY_REPORT.md) - Full MCP capabilities
- [MCP_SERVERS_USAGE_GUIDE.md](MCP_SERVERS_USAGE_GUIDE.md) - Prompting patterns
- [AI_SESSION_MEMORY.md](AI_SESSION_MEMORY.md) - Memory system details
- [DYNAMIC_TOOL_LOADING.md](DYNAMIC_TOOL_LOADING.md) - Focus modes

---

## Quick Setup Script

Create this script to set up a new project for EXARP:

```bash
#!/bin/bash
# setup-exarp.sh - Initialize EXARP context priming

mkdir -p .cursor/rules
mkdir -p .cursor/prompts

# Create minimal mcp.json
cat > .cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "exarp_pma": {
      "command": "uvx",
      "args": ["exarp"]
    }
  }
}
EOF

# Create openmemory.md template
cat > openmemory.md << 'EOF'
# Project Memory Guide

## Overview
[Describe your project here]

## User Defined Namespaces
- [Add your namespaces]

## Architecture
[Key architectural decisions]

## Components
[List major components]

## Patterns
[Common patterns]
EOF

echo "EXARP context priming initialized!"
echo "Next: Populate openmemory.md and restart Cursor"
```

---

*Well-primed context transforms AI from a generic assistant to a knowledgeable colleague who understands your project.*

