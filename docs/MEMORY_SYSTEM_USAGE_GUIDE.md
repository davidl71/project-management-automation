# Memory System Usage Guide

**Date**: 2025-12-01  
**Status**: Active Guidelines

---

## Overview

This project uses **two memory systems** that serve different purposes. Understanding when to use each is critical for effective context management.

---

## Memory Systems Comparison

### 1. **exarp Memory System** (`memory` tool)

**Purpose**: Project-specific AI session memories and context

**What it stores:**
- Component information (location, purpose, services, I/O)
- Implementation details (purpose, steps, key decisions)
- Debug fixes (issue, diagnosis, solution)
- User preferences (project-specific or global)
- Project information (general knowledge about the project)

**Storage**: Project-specific memory files  
**Access**: `memory` tool (action=save|recall|search)  
**Resources**: `automation://memories`, `automation://memories/recent`, `automation://wisdom`

**Use Cases:**
- ✅ Storing component architecture decisions
- ✅ Remembering implementation patterns for this project
- ✅ Tracking debug solutions specific to this codebase
- ✅ Storing project-specific user preferences
- ✅ Maintaining context about project structure

**Example:**
```python
# Store a component memory
memory(
    action="save",
    title="Auth Service - Token Validation",
    content="Location: src/auth/service.py. Purpose: Validates JWT tokens...",
    category="component"
)
```

---

### 2. **agentic-tools Memory System**

**Purpose**: General-purpose task and context memory

**What it stores:**
- Task-related memories
- General context across projects
- Agent memories (not project-specific)

**Storage**: `.agentic-tools-mcp/` directory  
**Access**: `mcp_agentic-tools_create_memory`, `mcp_agentic-tools_search_memories`, etc.  
**Resources**: None (tool-based only)

**Use Cases:**
- ✅ Storing memories that span multiple projects
- ✅ Task-specific context that's not tied to codebase
- ✅ General agent preferences
- ✅ Cross-project learnings

**Example:**
```python
# Store a general memory
mcp_agentic-tools_create_memory(
    workingDirectory="/path/to/project",
    title="User prefers TypeScript over JavaScript",
    content="User consistently chooses TypeScript for new projects...",
    category="preference"
)
```

---

## Decision Tree: Which Memory System to Use?

### Use **exarp memory** when:
- ✅ Memory is about **this specific project**
- ✅ Memory relates to **code/architecture/implementation**
- ✅ Memory is about **project-specific patterns**
- ✅ Memory should be **tied to project context**
- ✅ Memory is about **components, implementations, or debug fixes**

### Use **agentic-tools memory** when:
- ✅ Memory is **cross-project** or **general**
- ✅ Memory is about **user preferences across all projects**
- ✅ Memory is **task-related but not code-specific**
- ✅ Memory should be **accessible from any project**

---

## Examples

### Example 1: Component Architecture

**Use**: exarp memory

```python
memory(
    action="save",
    title="Database Layer - Connection Pooling",
    content="Location: src/db/pool.py. Uses connection pooling with max 10 connections...",
    category="component"
)
```

**Why**: Project-specific component information

---

### Example 2: User Preference (Project-Specific)

**Use**: exarp memory

```python
memory(
    action="save",
    title="Project Code Style - Type Hints",
    content="This project requires type hints for all functions. Use strict mypy checking.",
    category="user_preference"
)
```

**Why**: Preference specific to this project

---

### Example 3: User Preference (Global)

**Use**: agentic-tools memory

```python
mcp_agentic-tools_create_memory(
    workingDirectory="/path/to/project",
    title="User prefers async/await over callbacks",
    content="User consistently prefers async/await patterns across all projects...",
    category="preference"
)
```

**Why**: Global preference across all projects

---

### Example 4: Debug Fix

**Use**: exarp memory

```python
memory(
    action="save",
    title="Fix: FastMCP return type error",
    content="Issue: Tools returning dicts caused 'await expression' errors. Solution: Always return JSON strings...",
    category="debug"
)
```

**Why**: Project-specific bug fix

---

### Example 5: Task Context (Not Code-Related)

**Use**: agentic-tools memory

```python
mcp_agentic-tools_create_memory(
    workingDirectory="/path/to/project",
    title="User prefers morning standups",
    content="User prefers to have standup meetings in the morning, around 9 AM...",
    category="preference"
)
```

**Why**: General preference, not code-related

---

## Integration with OpenMemory

**exarp memory** integrates with the OpenMemory system:
- Memories are searchable via `search-memory` MCP tool
- Project memories are tied to `project_id: davidl71/project-management-automation`
- User preferences can be global or project-specific

**agentic-tools memory** is separate:
- Stored in `.agentic-tools-mcp/` directory
- Not integrated with OpenMemory
- Accessible via agentic-tools MCP tools

---

## Best Practices

### 1. **Prefer exarp memory for code-related context**
   - Component information
   - Implementation patterns
   - Debug solutions
   - Project-specific preferences

### 2. **Use agentic-tools memory for general context**
   - Cross-project preferences
   - General agent memories
   - Task context not tied to code

### 3. **Be explicit about scope**
   - Project-specific → exarp memory
   - Global/cross-project → agentic-tools memory

### 4. **Search both when needed**
   - Search exarp memory for project context
   - Search agentic-tools memory for general context

---

## Migration Considerations

If you're unsure which to use:

1. **Ask**: "Is this specific to this project's codebase?"
   - Yes → exarp memory
   - No → agentic-tools memory

2. **Ask**: "Would this be useful in other projects?"
   - Yes → agentic-tools memory
   - No → exarp memory

3. **Ask**: "Is this about code/architecture/implementation?"
   - Yes → exarp memory
   - No → Consider agentic-tools memory

---

## Related Documentation

- `.cursor/rules/openmemory.mdc` - OpenMemory integration rules
- `docs/AGENTIC_TOOLS_INTEGRATION_PLAN.md` - Agentic-tools integration
- `docs/MCP_SERVER_DUPLICATE_ANALYSIS.md` - Server comparison

---

## Summary

| Aspect | exarp Memory | agentic-tools Memory |
|--------|--------------|---------------------|
| **Scope** | Project-specific | Cross-project |
| **Focus** | Code/architecture | General context |
| **Storage** | Project memory files | `.agentic-tools-mcp/` |
| **Use for** | Components, implementations, project prefs | Global prefs, task context |
| **Integration** | OpenMemory MCP | Agentic-tools MCP |

**Rule of thumb**: If it's about **this project's code**, use **exarp memory**. If it's **general or cross-project**, use **agentic-tools memory**.

