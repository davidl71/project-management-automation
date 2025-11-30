# Dynamic Tool Loading Implementation

**Status**: ✅ Implemented
**MCP Spec**: [tools/list_changed](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
**Philosophy**: [Stop Converting REST APIs to MCP](https://www.jlowin.dev/blog/stop-converting-rest-apis-to-mcp)

---

## The Problem

From Jeremiah Lowin (FastMCP creator):

> "An API built for humans will poison your AI agent."
> "Context pollution is the silent killer of contemporary agentic workflows."

Exarp exposes **54 tools**. Without curation, this:
- Burns tokens on every LLM reasoning cycle (tool descriptions processed each time)
- Increases latency (more tools = more parsing)
- Causes "API librarian syndrome" (LLM debates which tool to use instead of solving problems)
- Creates hallucination risk (LLM invents plausible-sounding tools)

---

## The Solution: Dynamic Tool Curation

Use the MCP `tools/list_changed` notification to dynamically show/hide tools based on context.

### Context Reduction Results

| Workflow Mode | Tools Visible | Context Reduction |
|---------------|---------------|-------------------|
| Daily Checkin | 11 | **79.6%** |
| Security Review | 14 | **74.1%** |
| Task Management | 14 | **74.1%** |
| Code Review | 16 | **70.4%** |
| Sprint Planning | 20 | **63.0%** |
| Debugging | 20 | **63.0%** |
| Development | 27 | **50.0%** |
| All (legacy) | 54 | 0% |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DYNAMIC TOOL MANAGER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User/LLM                                                               │
│      │                                                                  │
│      ▼                                                                  │
│  ┌────────────────┐                                                     │
│  │  focus_mode()  │  "Switch to security review"                        │
│  └───────┬────────┘                                                     │
│          │                                                              │
│          ▼                                                              │
│  ┌────────────────────────────────────────────────────┐                │
│  │  DynamicToolManager                                │                │
│  │  ├─ current_mode: WorkflowMode                     │                │
│  │  ├─ extra_groups: Set[ToolGroup]                   │                │
│  │  └─ disabled_groups: Set[ToolGroup]                │                │
│  └───────┬────────────────────────────────────────────┘                │
│          │                                                              │
│          ▼                                                              │
│  ┌────────────────────────────────────────────────────┐                │
│  │  notify_tools_changed(ctx)                         │                │
│  │  → sends: notifications/tools/list_changed         │                │
│  └───────┬────────────────────────────────────────────┘                │
│          │                                                              │
│          ▼                                                              │
│  ┌────────────────────────────────────────────────────┐                │
│  │  Client re-fetches: tools/list                     │                │
│  │  → list_tools() filters by manager.is_tool_visible │                │
│  └────────────────────────────────────────────────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tool Groups

| Group | Description | Tools |
|-------|-------------|-------|
| **CORE** | Always visible | server_status, dev_reload |
| **DISCOVERY** | Meta tools | list_tools, get_tool_help, focus_mode |
| **HEALTH** | Project health | scorecard, overview, docs_health, working_copy_health |
| **TASKS** | Task management | alignment, duplicates, sync, clarification, batch_approve |
| **SECURITY** | Security scanning | dependency_scan, dependabot, security_report |
| **AUTOMATION** | Automation | run_automation, git_hooks, pattern_triggers |
| **CONFIG** | Configuration | cursor_rules, cursorignore, simplify_rules |
| **TESTING** | Testing | run_tests, coverage, definition_of_done, problems |
| **ADVISORS** | Advisor system | consult, briefing, list_advisors, podcast |
| **MEMORY** | Session memory | save, recall, search, session_summary |
| **WORKFLOW** | Workflow help | recommend_mode, recommend_model, prompt_tracking |
| **PRD** | PRD tools | generate_prd, prd_alignment |

---

## Workflow Modes

### Minimal Modes (highest context reduction)

**daily_checkin** (9 tools, 82.7% reduction)
- Core + Discovery + Health
- Perfect for: Quick health checks, start of day

**security_review** (12 tools, 76.9% reduction)
- Core + Discovery + Security + Health
- Perfect for: Security audits, dependency updates

**task_management** (10 tools, 80.8% reduction)
- Core + Discovery + Tasks
- Perfect for: Sprint backlog grooming

**code_review** (10 tools, 80.8% reduction)
- Core + Discovery + Testing + Health
- Perfect for: PR reviews, code quality checks

### Balanced Modes

**development** (25 tools, 51.9% reduction) [DEFAULT]
- Core + Discovery + Health + Tasks + Testing + Memory
- Perfect for: General development work

**debugging** (17 tools, 67.3% reduction)
- Core + Discovery + Memory + Testing + Health
- Perfect for: Bug fixing sessions

### Legacy Mode

**all** (52 tools, 0% reduction)
- All tool groups enabled
- Use sparingly (defeats the purpose)

---

## Implementation Status ✅

All components are implemented and wired into `server.py`:

### Files Created/Modified

| File | Description |
|------|-------------|
| `tools/dynamic_tools.py` | Core manager, mode inference, usage tracking |
| `middleware/tool_filter.py` | MCP middleware for filtering tools/list |
| `middleware/__init__.py` | Exports ToolFilterMiddleware |
| `server.py` | Middleware + tool registration |

### Registered Tools

```python
focus_mode(mode, enable_group, disable_group, status)
# Switch workflow modes, enable/disable tool groups

suggest_mode(text, auto_switch)  
# Adaptive mode inference from text or usage patterns

tool_usage_stats()
# View tool usage analytics and patterns
```

### Middleware Chain

```python
# In server.py (line ~270)
mcp.add_middleware(SecurityMiddleware(...))
mcp.add_middleware(LoggingMiddleware(...))
mcp.add_middleware(ToolFilterMiddleware(enabled=True))  # NEW
```

### Key Features

1. **Mode Switching**: `focus_mode(mode="security_review")`
2. **Group Control**: `focus_mode(enable_group="advisors")`
3. **Adaptive Inference**: `suggest_mode(text="I need to check for vulnerabilities")`
4. **Auto-Switch**: `suggest_mode(auto_switch=True)` - switches if confidence > 0.5
5. **Usage Learning**: Tracks tool co-occurrence for recommendations
6. **MCP Compliant**: Uses `tools/list_changed` notification

---

## Usage Examples

### Switch to security mode
```
User: "I need to do a security audit"
AI: [calls focus_mode(mode="security_review")]
→ Only 14 security-relevant tools visible
→ LLM has 74.1% less context to process
```

### Adaptive mode suggestion
```
User: "I want to scan for CVEs"
AI: [calls suggest_mode(text="scan for CVEs")]
→ Returns: {"suggested_mode": "security_review", "confidence": 0.5}
→ Rationale: "Keywords detected: scan, cves"
```

### Auto-switch based on usage
```
# After using security tools repeatedly...
AI: [calls suggest_mode(auto_switch=True)]
→ Detects pattern: recent tools suggest security_review
→ Auto-switches to security_review mode
→ Notifies client via tools/list_changed
```

### Enable specific group
```
User: "Also need the advisor tools"
AI: [calls focus_mode(enable_group="advisors")]
→ Advisors added to current mode
→ Notification sent → client refreshes tool list
```

### Check current status
```
User: "What tools do I have access to?"
AI: [calls focus_mode(status=True)]
→ Returns: mode, visible tools, reduction %, available modes
```

### View usage analytics
```
AI: [calls tool_usage_stats()]
→ Returns: most used tools, tool relationships, mode history
```

---

## Benefits

1. **Token Efficiency**: 50-80% reduction in tool description tokens per turn
2. **Faster Reasoning**: Less tool options = quicker decisions
3. **Reduced Hallucinations**: Can't hallucinate tools that aren't in context
4. **Better UX**: LLM focuses on task, not tool selection
5. **MCP Compliant**: Uses standard list_changed notification

---

## Future Enhancements

1. ~~**Auto-detection**: Infer workflow mode from conversation context~~ ✅ DONE
2. ~~**Adaptive loading**: Track tool usage, pre-load frequently used groups~~ ✅ DONE
3. **Per-tool lazy loading**: Only describe tool fully when called
4. **Tool aliases**: Short names for common operations
5. **Persistence**: Save/restore usage patterns across sessions
6. **Client hints**: Pass client preferences for initial mode selection

---

## References

- [MCP Tools Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [Stop Converting REST APIs to MCP](https://www.jlowin.dev/blog/stop-converting-rest-apis-to-mcp) - Jeremiah Lowin
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

