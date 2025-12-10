# Recommended MCP Companion Servers


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

Exarp works best when paired with complementary MCP servers. These are **optional but recommended** for enhanced AI agent workflows.

## 🟢 Required (Core)

| Server | Purpose | Install |
|--------|---------|---------|
| **exarp** | Project management automation | `pip install exarp` |

## 🟡 Recommended (Enhanced Experience)

### Human Interaction MCP

**Purpose**: Enables AI agents to ask clarifying questions, request confirmations, and wait for human input during complex workflows.

**Why it's useful with Exarp**:
- Confirm before batch task operations (merge duplicates, bulk assign)
- Ask clarifying questions when task descriptions are ambiguous
- Get human approval before auto-fixing issues
- Interactive task clarification resolution

**Configuration example**:
```json
{
  "mcpServers": {
    "human": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-human-in-the-loop"]
    }
  }
}
```

**Alternative implementations**:
- `@anthropic/mcp-human-in-the-loop` - Official Anthropic implementation
- Custom: Any MCP server exposing `ask_human`, `confirm`, `wait_for_input` tools

---

### Context7 MCP

**Purpose**: Up-to-date library documentation lookup.

**Why it's useful with Exarp**:
- Get current API docs when implementing automation scripts
- Verify tool patterns match library best practices

**Configuration**:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

---

### Sequential Thinking MCP

**Purpose**: Step-by-step reasoning for complex workflows.

**Why it's useful with Exarp**:
- Plan multi-step automation sequences
- Break down complex refactoring tasks
- Create implementation workflows from Tractatus analysis

---

### Tractatus Thinking MCP

**Purpose**: Logical decomposition of complex problems.

**Why it's useful with Exarp**:
- Analyze why all deployment factors must align
- Decompose fuzzy requirements into measurable components
- Find the ONE missing element preventing task completion

---

## 🔵 Optional (Specialized)

| Server | Purpose | Use Case |
|--------|---------|----------|
| **GitKraken** | Git operations, PRs, issues | Multi-repo workflows |
| **Filesystem** | File operations | Bulk file management |
| **Memory** | Persistent AI memory | Cross-session context |

---

## Full Recommended Stack

```json
{
  "mcpServers": {
    "exarp": {
      "command": "exarp",
      "args": []
    },
    "human": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-human-in-the-loop"]
    },
    "context7": {
      "command": "npx", 
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

---

## Detection Hints for AI Agents

When Exarp's context primer runs, it checks for companion MCPs and suggests them if missing:

```
⚠️ Recommended MCP not detected: human-interaction
   Some operations (batch approve, auto-fix) work better with human confirmation.
   See: docs/RECOMMENDED_MCP_COMPANIONS.md
```

---

## Adding Detection to Your Workflow

The `auto_prime_session()` tool can detect available MCPs and suggest missing ones:

```python
# In auto_primer.py context
RECOMMENDED_COMPANIONS = {
    "human": {
        "tools": ["ask_human", "confirm", "wait_for_input"],
        "benefit": "Enables confirmations for batch operations",
        "install": "npx -y @anthropic/mcp-human-in-the-loop",
    },
    "context7": {
        "tools": ["resolve-library-id", "get-library-docs"],
        "benefit": "Up-to-date library documentation",
        "install": "npx -y @context7/mcp-server",
    },
}
```

---

**Last Updated**: 2025-11-27

