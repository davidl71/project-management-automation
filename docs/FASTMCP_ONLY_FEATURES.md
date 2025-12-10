# FastMCP-Only Features


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Last Updated**: 2025-12-11

This document lists features that are **only available in FastMCP** and cannot be replicated in stdio server mode.

---

## Why FastMCP-Only?

FastMCP provides advanced features through its middleware system and plugin architecture that are not part of the standard MCP protocol. These features enhance the server but are not required for basic functionality.

---

## FastMCP-Only Features List

### 1. Middleware (FastMCP 2 Feature)

**Location**: `project_management_automation/server.py` ~line 344-373

**Features**:
- **SecurityMiddleware**: Rate limiting (120 calls/min), path validation, access control
- **LoggingMiddleware**: Request timing, slow operation detection (5s threshold)
- **ToolFilterMiddleware**: Dynamic tool loading based on workflow mode (reduces context pollution)

**Impact**: 
- ✅ Better security and performance in FastMCP
- ⚠️ Not available in stdio mode (no security middleware, no tool filtering)

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    mcp.add_middleware(SecurityMiddleware(...))
    mcp.add_middleware(LoggingMiddleware(...))
    mcp.add_middleware(ToolFilterMiddleware(enabled=True))
```

---

### 2. Resource Templates (FastMCP 2 Feature)

**Location**: `project_management_automation/server.py` ~line 376-386

**Features**: Dynamic resource template registration

**Impact**: 
- ✅ Enhanced resource discovery in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .resources.templates import register_resource_templates
    register_resource_templates(mcp)
```

---

### 3. Context Primer Resources

**Location**: `project_management_automation/server.py` ~line 388-396

**Features**: AI priming resources for session context

**Impact**: 
- ✅ Better AI context in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .resources.context_primer import register_context_primer_resources
    register_context_primer_resources(mcp)
```

---

### 4. Hint Registry Resources

**Location**: `project_management_automation/server.py` ~line 398-406

**Features**: Dynamic hint loading for tool discovery

**Impact**: 
- ✅ Enhanced tool discovery in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .resources.hint_registry import register_hint_registry_resources
    register_hint_registry_resources(mcp)
```

---

### 5. Auto-Primer Tools

**Location**: `project_management_automation/server.py` ~line 408-416

**Features**: Automatic session priming tools

**Impact**: 
- ✅ Automatic context setup in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .tools.auto_primer import register_auto_primer_tools
    register_auto_primer_tools(mcp)
```

---

### 6. Session Mode Resources

**Location**: `project_management_automation/server.py` ~line 418-426

**Features**: Session mode resources (MODE-002)

**Impact**: 
- ✅ Session management in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .resources.session import register_session_resources
    register_session_resources(mcp)
```

---

### 7. Prompt Discovery Resources and Tools

**Location**: `project_management_automation/server.py` ~line 428-440

**Features**: Resources and tools for prompt discovery

**Impact**: 
- ✅ Enhanced prompt discovery in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .resources.prompt_discovery import (
        register_prompt_discovery_resources,
        register_prompt_discovery_tools,
    )
    register_prompt_discovery_resources(mcp)
    register_prompt_discovery_tools(mcp)
```

---

### 8. Assignee Management Resources and Tools

**Location**: `project_management_automation/server.py` ~line 442-452

**Features**: Resources and tools for task assignee management

**Impact**: 
- ✅ Assignee management in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .resources.assignees import register_assignee_resources
    from .tools.task_assignee import register_assignee_tools
    register_assignee_resources(mcp)
    register_assignee_tools(mcp)
```

---

### 9. Capabilities Resources

**Location**: `project_management_automation/server.py` ~line 454-462

**Features**: Agent priming resources for capabilities

**Impact**: 
- ✅ Better agent priming in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .resources.capabilities import register_capabilities_resources
    register_capabilities_resources(mcp)
```

---

### 10. Session Handoff Tools

**Location**: `project_management_automation/server.py` ~line 464-472

**Features**: Multi-device coordination tools

**Impact**: 
- ✅ Session handoff in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP and mcp:
    from .tools.session_handoff import register_handoff_tools
    register_handoff_tools(mcp)
```

---

### 11. Lifespan Support

**Location**: `project_management_automation/server.py` ~line 313-328

**Features**: Startup and shutdown hooks

**Impact**: 
- ✅ Clean initialization and teardown in FastMCP
- ⚠️ Not available in stdio mode

**Code**:
```python
if not USE_STDIO and FastMCP:
    from .lifespan import exarp_lifespan
    if LIFESPAN_AVAILABLE and exarp_lifespan:
        mcp = FastMCP("exarp", lifespan=exarp_lifespan)
```

---

## Summary

| Feature | FastMCP | Stdio Server | Impact |
|---------|---------|--------------|--------|
| **Core Tools** | ✅ | ✅ | Required - must sync |
| **Core Resources** | ✅ | ✅ | Required - must sync |
| **Core Prompts** | ✅ | ✅ | Required - must sync |
| **Middleware** | ✅ | ❌ | Enhancement only |
| **Resource Templates** | ✅ | ❌ | Enhancement only |
| **Context Primers** | ✅ | ❌ | Enhancement only |
| **Hint Registry** | ✅ | ❌ | Enhancement only |
| **Auto-Primers** | ✅ | ❌ | Enhancement only |
| **Session Resources** | ✅ | ❌ | Enhancement only |
| **Prompt Discovery** | ✅ | ❌ | Enhancement only |
| **Assignee Management** | ✅ | ❌ | Enhancement only |
| **Capabilities** | ✅ | ❌ | Enhancement only |
| **Session Handoff** | ✅ | ❌ | Enhancement only |
| **Lifespan** | ✅ | ❌ | Enhancement only |

---

## Implications

### For Users

- **FastMCP mode** (default): Full feature set with all enhancements
- **Stdio mode** (`EXARP_FORCE_STDIO=1`): Core features only, no enhancements

### For Developers

- **Core features** (tools, resources, prompts): Must be registered in both systems
- **FastMCP-only features**: Only register in FastMCP, no stdio equivalent needed
- **Verification**: Sync script only checks core features, not FastMCP-only enhancements

---

## When to Use Each Mode

### Use FastMCP (Default)
- ✅ Production use
- ✅ When you need security middleware
- ✅ When you need tool filtering
- ✅ When you need advanced features

### Use Stdio Server
- ✅ When FastMCP is not available
- ✅ For debugging MCP protocol issues
- ✅ When you only need core features
- ✅ For compatibility testing

---

## Questions?

- See [MCP Sync Guide](MCP_SYNC_GUIDE.md) for core feature synchronization
- FastMCP-only features are automatically registered when FastMCP is available
- No action needed - these features work automatically in FastMCP mode
