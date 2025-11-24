# Automa MCP Server Integration Analysis

**Date**: 2025-01-27
**Status**: Analysis Complete - Integration Opportunities Identified

---

## Executive Summary

**Current State**: Automa has **minimal integration** with other MCP servers. It primarily uses:
- Direct file access for Todo2 (instead of agentic-tools MCP)
- Subprocess for git operations (instead of git MCP)
- pathlib for filesystem (instead of filesystem MCP)
- No actual calls to Context7, Tractatus, or Sequential MCP servers

**Opportunity**: Automa could significantly enhance its capabilities by:
1. Using MCP client libraries to call other servers programmatically
2. Replacing direct file access with MCP server calls
3. Adding actual integration with Context7, Tractatus, and Sequential
4. Exposing resources that other servers can use

---

## Current Integration Status

### ✅ What Automa Currently Does

| Integration | Status | Method | Notes |
|------------|--------|--------|-------|
| **Todo2/agentic-tools** | ⚠️ Partial | Direct file read (`.todo2/state.todo2.json`) | Should use agentic-tools MCP |
| **Git** | ⚠️ Partial | Subprocess (`git status`, `git branch`) | Should use git MCP |
| **Filesystem** | ⚠️ Partial | Python `pathlib`/`os` | Should use filesystem MCP |
| **Context7** | ❌ None | Only mentioned in docs | Should actually call Context7 |
| **Tractatus** | ❌ None | Only mentioned in docs | Should actually call Tractatus |
| **Sequential** | ❌ None | Only mentioned in docs | Should actually call Sequential |

### ❌ What's Missing

1. **No MCP Client Usage**: Automa doesn't use MCP client libraries to call other servers
2. **Direct File Access**: Reads Todo2 files directly instead of using agentic-tools MCP
3. **Subprocess Git**: Uses `subprocess` for git instead of git MCP server
4. **No Context7 Calls**: Doesn't verify external library documentation
5. **No Tractatus Calls**: Doesn't use structural analysis before running tools
6. **No Sequential Calls**: Doesn't convert results into implementation workflows

---

## Integration Architecture

### MCP Server Communication Model

**Important**: MCP servers are independent services that communicate with the AI assistant (Cursor) via JSON-RPC over stdio. However, **MCP servers CAN call other MCP servers** using MCP client libraries.

### Two Integration Approaches

#### Approach 1: AI Orchestration (Current)
- AI assistant calls multiple MCP servers
- Automa provides hints in tool descriptions
- Works but requires AI to coordinate

#### Approach 2: Programmatic MCP Client (Recommended)
- Automa uses MCP client library to call other servers
- Direct integration within automa tools
- More powerful and autonomous

---

## Integration Opportunities

### 1. Agentic-Tools MCP Integration

**Current**: Automa reads `.todo2/state.todo2.json` directly

**Problem**:
- Breaks when Todo2 format changes
- Doesn't leverage agentic-tools MCP features
- Can't use advanced task management features

**Solution**: Use agentic-tools MCP client

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def get_todo2_tasks():
    async with stdio_client(StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-agentic-tools"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()

            # List tasks
            result = await session.list_tools()
            tasks = await session.call_tool("list_todos", {
                "project_id": "davidl71/ib_box_spread_full_universal"
            })
            return tasks
```

**Benefits**:
- ✅ Always uses latest Todo2 format
- ✅ Access to advanced task features
- ✅ Better error handling
- ✅ Works across different Todo2 implementations

**Files to Update**:
- `tools/todo2_alignment.py` - Use agentic-tools MCP instead of file read
- `tools/duplicate_detection.py` - Use agentic-tools MCP
- `tools/nightly_task_automation.py` - Use agentic-tools MCP
- `resources/tasks.py` - Use agentic-tools MCP

---

### 2. Git MCP Integration

**Current**: Automa uses `subprocess` for git commands

**Problem**:
- Fragile (depends on git being installed)
- Limited error handling
- Can't use advanced git features

**Solution**: Use git MCP server

```python
async def get_git_status():
    async with stdio_client(StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-git"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Get git status
            status = await session.call_tool("git_status", {})
            return status
```

**Benefits**:
- ✅ Better error handling
- ✅ Works even if git not in PATH
- ✅ Access to advanced git features
- ✅ Consistent interface

**Files to Update**:
- `tools/working_copy_health.py` - Use git MCP instead of subprocess
- `tools/git_hooks.py` - Use git MCP for validation

---

### 3. Filesystem MCP Integration

**Current**: Automa uses Python `pathlib`/`os`

**Problem**:
- Limited workspace awareness
- Can't leverage filesystem MCP features
- Path resolution issues

**Solution**: Use filesystem MCP for workspace operations

```python
async def read_project_file(path: str):
    async with stdio_client(StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Read file with workspace awareness
            content = await session.read_resource(f"file://{path}")
            return content
```

**Benefits**:
- ✅ Better workspace awareness
- ✅ Consistent path resolution
- ✅ Access to filesystem MCP features

**Files to Update**:
- All tools that read/write files
- `tools/docs_health.py` - Use filesystem MCP
- `tools/simplify_rules.py` - Use filesystem MCP

---

### 4. Context7 MCP Integration

**Current**: Only mentioned in documentation, never actually called

**Problem**:
- Can't verify external library documentation
- Can't check if documentation references are current

**Solution**: Actually call Context7 MCP

```python
async def verify_library_docs(library: str):
    async with stdio_client(StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-context7"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Search for library documentation
            result = await session.call_tool("search", {
                "query": f"{library} documentation",
                "limit": 5
            })
            return result
```

**Benefits**:
- ✅ Verify external library references
- ✅ Check documentation currency
- ✅ Validate API usage patterns

**Files to Create/Update**:
- `tools/docs_health.py` - Add Context7 verification step
- `tools/external_tool_hints.py` - Use Context7 to verify hints

---

### 5. Tractatus Thinking MCP Integration

**Current**: Only mentioned in documentation as "use before automa"

**Problem**:
- Can't do structural analysis before running tools
- Can't understand problem structure programmatically

**Solution**: Actually call Tractatus MCP for structural analysis

```python
async def analyze_structure(concept: str):
    async with stdio_client(StdioServerParameters(
        command="npx",
        args=["-y", "tractatus_thinking"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Start structural analysis
            result = await session.call_tool("tractatus_thinking", {
                "operation": "start",
                "concept": concept
            })
            return result
```

**Benefits**:
- ✅ Structural analysis before automation
- ✅ Understand problem dependencies
- ✅ Better tool recommendations

**Files to Create/Update**:
- `tools/docs_health.py` - Add Tractatus analysis before checking
- `tools/todo2_alignment.py` - Add Tractatus analysis for task structure
- New tool: `tools/structural_analysis.py` - Wrapper for Tractatus

---

### 6. Sequential Thinking MCP Integration

**Current**: Only mentioned in documentation as "use after automa"

**Problem**:
- Can't convert analysis results into implementation workflows
- Can't create step-by-step plans programmatically

**Solution**: Actually call Sequential MCP for workflow creation

```python
async def create_workflow(problem: str, analysis_results: dict):
    async with stdio_client(StdioServerParameters(
        command="python3",
        args=["-m", "sequential_thinking"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Create implementation workflow
            result = await session.call_tool("sequentialthinking", {
                "thought": f"Based on analysis: {analysis_results}, how do we solve: {problem}",
                "nextThoughtNeeded": True,
                "thoughtNumber": 1,
                "totalThoughts": 5
            })
            return result
```

**Benefits**:
- ✅ Convert analysis into actionable steps
- ✅ Create implementation workflows
- ✅ Document processes automatically

**Files to Create/Update**:
- `tools/docs_health.py` - Add Sequential workflow for fixes
- `tools/todo2_alignment.py` - Add Sequential workflow for realignment
- New tool: `tools/workflow_generator.py` - Wrapper for Sequential

---

## Implementation Strategy

### Phase 1: MCP Client Infrastructure

1. **Add MCP Client Dependency**
   - Add `mcp` Python package to `pyproject.toml`
   - Create `mcp_client.py` utility module
   - Add connection pooling for efficiency

2. **Create MCP Client Wrapper**
   - Abstract MCP client creation
   - Handle connection errors gracefully
   - Add retry logic

### Phase 2: Replace Direct Access

1. **Agentic-Tools Integration**
   - Replace Todo2 file reads with agentic-tools MCP calls
   - Update all tools that use Todo2

2. **Git Integration**
   - Replace subprocess git with git MCP
   - Update `working_copy_health.py`

3. **Filesystem Integration**
   - Use filesystem MCP for workspace operations
   - Update file reading/writing tools

### Phase 3: Add New Integrations

1. **Context7 Integration**
   - Add Context7 verification to docs health
   - Verify external library references

2. **Tractatus Integration**
   - Add structural analysis before tools
   - Create structural analysis wrapper

3. **Sequential Integration**
   - Add workflow generation after analysis
   - Create workflow generator wrapper

---

## Integration Matrix

| Automa Tool | Agentic-Tools | Git | Filesystem | Context7 | Tractatus | Sequential |
|------------|---------------|-----|------------|----------|-----------|------------|
| `check_documentation_health` | ❌ | ❌ | ✅ Replace | ✅ Add | ✅ Add | ✅ Add |
| `analyze_todo2_alignment` | ✅ Replace | ❌ | ❌ | ❌ | ✅ Add | ✅ Add |
| `detect_duplicate_tasks` | ✅ Replace | ❌ | ❌ | ❌ | ✅ Add | ✅ Add |
| `scan_dependency_security` | ❌ | ❌ | ✅ Replace | ✅ Add | ❌ | ✅ Add |
| `check_working_copy_health` | ❌ | ✅ Replace | ❌ | ❌ | ❌ | ❌ |
| `sync_todo_tasks` | ✅ Replace | ✅ Replace | ✅ Replace | ❌ | ❌ | ❌ |
| `nightly_task_automation` | ✅ Replace | ❌ | ✅ Replace | ❌ | ❌ | ❌ |

**Legend**:
- ✅ **Replace**: Replace current method with MCP integration
- ✅ **Add**: Add new MCP integration
- ❌ **Not Applicable**: Not relevant for this tool

---

## Benefits of Full Integration

### 1. Reliability
- ✅ Always uses latest MCP server features
- ✅ Better error handling
- ✅ Works across different environments

### 2. Capabilities
- ✅ Access to advanced features
- ✅ Better workspace awareness
- ✅ Structural analysis and workflow generation

### 3. Maintainability
- ✅ Less code to maintain (no direct file access)
- ✅ Consistent interfaces
- ✅ Better testing

### 4. Extensibility
- ✅ Easy to add new MCP integrations
- ✅ Can leverage new MCP server features
- ✅ Better plugin architecture

---

## Dependencies

### Required Packages
```toml
[project.dependencies]
mcp = "^1.0.0"  # MCP client library
```

### MCP Servers Required
- `@modelcontextprotocol/server-agentic-tools` (npm)
- `@modelcontextprotocol/server-git` (npm)
- `@modelcontextprotocol/server-filesystem` (npm)
- `@modelcontextprotocol/server-context7` (npm)
- `tractatus_thinking` (npm)
- `sequential_thinking` (Python package)

---

## Risk Assessment

### High Risk
- **Breaking Changes**: MCP client library changes
- **Performance**: Multiple MCP connections
- **Complexity**: More dependencies

### Mitigation
- Use connection pooling
- Add comprehensive error handling
- Provide fallback to direct access
- Extensive testing

---

## Success Metrics

### Phase 1: Infrastructure
- ✅ MCP client wrapper created
- ✅ Connection pooling working
- ✅ Error handling comprehensive

### Phase 2: Replacements
- ✅ All Todo2 file reads replaced
- ✅ All git subprocess calls replaced
- ✅ All filesystem operations use MCP

### Phase 3: New Integrations
- ✅ Context7 verification working
- ✅ Tractatus analysis integrated
- ✅ Sequential workflows generated

---

## Next Steps

1. **Create Todo2 tasks** for all integration work
2. **Add MCP client dependency** to `pyproject.toml`
3. **Create MCP client wrapper** module
4. **Start with agentic-tools integration** (highest impact)
5. **Iterate through other integrations**

---

**Last Updated**: 2025-01-27
