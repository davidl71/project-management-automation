# AI Session Memory System

> 💡 **AI Assistant Hint:** This document describes EXARP's AI session memory system for persistent context across conversations.

**Date**: 2025-11-26  
**Status**: Implemented  
**Trusted Advisor**: 🎓 Confucius - *"Choose a job you love, and you will never have to work a day."*

---

## Overview

The AI Session Memory System enables persistent storage and retrieval of insights, discoveries, and context across AI sessions. This provides:

- **Session Continuity** - Remember what was learned yesterday
- **Task Context** - Link discoveries to specific tasks
- **Debug History** - Searchable solutions to past problems
- **Pattern Recognition** - Accumulated sprint insights

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Session Memory System                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Storage: .exarp/memories/*.json                                │
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   MCP        │     │   MCP        │     │  Advisor     │    │
│  │  Resources   │     │   Tools      │     │   Logs       │    │
│  │  (passive)   │     │  (active)    │     │  (wisdom)    │    │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘    │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │  automation://    │                        │
│                    │     wisdom        │                        │
│                    └───────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Memory Categories

| Category | Icon | Description | Example |
|----------|------|-------------|---------|
| `debug` | 🔧 | Error solutions, workarounds, root causes | "Fixed ImportError by adding __init__.py" |
| `research` | 📚 | Pre-implementation findings, approach comparisons | "Compared MCP vs REST, chose MCP for type safety" |
| `architecture` | 🏗️ | Component relationships, hidden dependencies | "Module X depends on Y through event system" |
| `preference` | ⚙️ | User coding style, workflow preferences | "User prefers verbose logging in debug mode" |
| `insight` | 💡 | Sprint patterns, blockers, optimizations | "Tasks without estimates tend to stall in review" |

---

## MCP Resources

Resources provide **passive context** - the AI can browse them without explicit action.

### Available Resources

| Resource URI | Description |
|--------------|-------------|
| `automation://memories` | All memories (browsable) |
| `automation://memories/category/{cat}` | Filter by category |
| `automation://memories/task/{task_id}` | Linked to specific task |
| `automation://memories/recent` | Last 24 hours |
| `automation://memories/session/{date}` | Daily session (YYYY-MM-DD) |
| `automation://wisdom` | Combined memories + advisor consultations |

### Usage Example

```
AI reads: automation://memories/task/T-123
→ Gets: All research, debug history, decisions for this task
→ Knows what was already tried before starting work
```

---

## MCP Tools

Tools provide **active operations** for creating and searching memories.

### `save_memory`

Save a session insight/discovery to persistent memory.

```python
save_memory(
    title="Debug: Import error fix",
    content="Fixed by adding __init__.py to package directory",
    category="debug",
    task_id="0054adcf-e06a-41b9-81be-79a31a521166"  # optional
)
```

**Parameters:**
- `title` (str): Short descriptive title (max 100 chars)
- `content` (str): Full insight content
- `category` (str): One of: debug, research, architecture, preference, insight
- `task_id` (str, optional): Task ID to link this memory to

### `recall_context`

Get memories related to a task before starting work.

```python
recall_context(
    task_id="0054adcf-e06a-41b9-81be-79a31a521166",
    include_related=True
)
```

**Returns:** Summary of related memories grouped by category.

### `search_memories`

Search past insights by text.

```python
search_memories(
    query="import error",
    category="debug",  # optional filter
    limit=10
)
```

### `session_summary`

Generate end-of-session summary with learnings.

```python
session_summary(
    date="2025-11-26",  # optional, defaults to today
    include_consultations=True  # include advisor wisdom
)
```

### `sprint_memories`

Get memories useful for sprint planning/review.

```python
sprint_memories()
# Returns: blockers, debug solutions, patterns from last 7 days
```

---

## Wisdom Integration

The `automation://wisdom` resource combines:

1. **AI Memories** - What was learned
2. **Advisor Consultations** - What wisdom was given (from `.exarp/advisor_logs/`)
3. **Timeline View** - Chronological narrative

This enables the podcast export feature to pull from a unified knowledge base.

---

## Storage Format

Memories are stored as JSON files in `.exarp/memories/`:

```json
{
  "id": "850a3f80-1b13-4797-9211-c4ff9543175b",
  "title": "Sprint: AI Memory System implementation started",
  "content": "Created resources/memories.py and tools/session_memory.py...",
  "category": "architecture",
  "linked_tasks": ["0054adcf-e06a-41b9-81be-79a31a521166"],
  "metadata": {},
  "created_at": "2025-11-26T12:33:16.312649",
  "session_date": "2025-11-26"
}
```

---

## Best Practices

### When to Save Memories

| Situation | Category | Example |
|-----------|----------|---------|
| Fixed a tricky bug | `debug` | Root cause + solution |
| Researched approaches | `research` | Comparison + decision |
| Discovered hidden dependency | `architecture` | Component relationship |
| Learned user preference | `preference` | Coding style, workflow |
| Noticed pattern | `insight` | Sprint/blocker pattern |

### Session Workflow

1. **Start of Session**: Check `automation://memories/recent` for context
2. **Before Task**: Use `recall_context(task_id)` to see past work
3. **During Work**: Save discoveries with `save_memory()`
4. **End of Session**: Run `session_summary()` to review learnings

### Linking to Tasks

Always link memories to tasks when relevant:
- Enables `recall_context()` to work
- Builds task-specific knowledge base
- Supports future sprint planning

---

## Related Documentation

- [EXARP MCP Integration](./EXARP_MCP_INTEGRATION_ANALYSIS.md) - MCP architecture
- [Project Overview](./PROJECT_OVERVIEW.md) - Project overview and health metrics

---

## Files

| File | Description |
|------|-------------|
| `resources/memories.py` | Resource handlers |
| `tools/session_memory.py` | MCP tool implementations |
| `.exarp/memories/` | Memory storage directory |
| `.exarp/advisor_logs/` | Advisor consultation logs |

