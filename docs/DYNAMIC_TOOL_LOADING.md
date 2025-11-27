# Dynamic Tool Loading Implementation

**Status**: Implementation Phase
**MCP Spec**: [tools/list_changed](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
**Philosophy**: [Stop Converting REST APIs to MCP](https://www.jlowin.dev/blog/stop-converting-rest-apis-to-mcp)

---

## The Problem

From Jeremiah Lowin (FastMCP creator):

> "An API built for humans will poison your AI agent."
> "Context pollution is the silent killer of contemporary agentic workflows."

Exarp currently exposes **52 tools** at all times. This:
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
| Daily Checkin | 9 | **82.7%** |
| Security Review | 12 | **76.9%** |
| Task Management | 10 | **80.8%** |
| Sprint Planning | 15 | **71.2%** |
| Development | 25 | **51.9%** |
| All (legacy) | 52 | 0% |

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
| **CONFIG** | Configuration | cursor_rules, cursorignore, simplify_rules, pwa_config |
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

## Integration Guide

### Step 1: Import dynamic tools module

```python
# In server.py
from .tools.dynamic_tools import (
    get_tool_manager,
    focus_mode as _focus_mode,
)
```

### Step 2: Register focus_mode tool

```python
@mcp.tool()
async def focus_mode(
    mode: Optional[str] = None,
    enable_group: Optional[str] = None,
    disable_group: Optional[str] = None,
    status: bool = False,
    ctx: Context = None,
) -> str:
    """Switch workflow mode for context-appropriate tools."""
    result = _focus_mode(mode, enable_group, disable_group, status)
    
    # Send notification if mode changed
    if ctx and (mode or enable_group or disable_group):
        from .context_helpers import notify_tools_changed
        await notify_tools_changed(ctx)
    
    return result
```

### Step 3: Filter tools in list_tools (stdio server)

```python
@stdio_server_instance.list_tools()
async def list_tools() -> List[Tool]:
    """List currently visible tools based on workflow mode."""
    from .tools.dynamic_tools import get_tool_manager
    
    manager = get_tool_manager()
    all_tools = _get_all_tool_definitions()  # Existing tool list
    
    # Filter by visibility
    return [
        tool for tool in all_tools
        if manager.is_tool_visible(tool.name)
    ]
```

### Step 4: Filter tools in FastMCP (decorator approach)

For FastMCP, tools are registered via decorators. Options:

**Option A: Conditional registration** (at startup)
```python
if manager.is_tool_visible("scan_dependency_security"):
    @mcp.tool()
    def scan_dependency_security(...): ...
```

**Option B: Tool filter middleware** (dynamic)
```python
class ToolFilterMiddleware:
    async def __call__(self, request, call_next):
        if request.method == "tools/list":
            response = await call_next(request)
            response.tools = [
                t for t in response.tools
                if manager.is_tool_visible(t.name)
            ]
            return response
        return await call_next(request)
```

**Option C: Custom list_tools handler** (hybrid)
Override the FastMCP default list_tools to filter.

---

## Usage Examples

### Switch to security mode
```
User: "I need to do a security audit"
AI: [calls focus_mode(mode="security_review")]
→ Only 12 security-relevant tools visible
→ LLM has 76.9% less context to process
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
→ Returns current mode, visible tools, reduction %
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

1. **Auto-detection**: Infer workflow mode from conversation context
2. **Adaptive loading**: Track tool usage, pre-load frequently used groups
3. **Per-tool lazy loading**: Only describe tool fully when called
4. **Tool aliases**: Short names for common operations

---

## References

- [MCP Tools Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [Stop Converting REST APIs to MCP](https://www.jlowin.dev/blog/stop-converting-rest-apis-to-mcp) - Jeremiah Lowin
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

