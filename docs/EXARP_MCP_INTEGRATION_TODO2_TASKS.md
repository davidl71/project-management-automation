# Exarp MCP Integration - Todo2 Tasks


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-26
**Status**: Tasks Created

---

## Task Overview

### Task 1: Add MCP Client Infrastructure

**Priority**: High (9/10)
**Tags**: exarp, integration, mcp, infrastructure

**Objective**: Create MCP client infrastructure for calling other MCP servers programmatically

**Acceptance Criteria**:
- `mcp` Python package added to `pyproject.toml`
- `mcp_client.py` utility module created with connection pooling
- Error handling and retry logic implemented
- Connection wrapper abstracts MCP client creation
- Works with all required MCP servers

**Scope**:
- **Included:** MCP client library, connection pooling, error handling, retry logic
- **Excluded:** Actual tool integrations (separate tasks)
- **Clarification Required:** Connection pooling strategy

**Technical Requirements**:
- Add `mcp = "^1.0.0"` to `pyproject.toml`
- Create `mcp-servers/project-management-automation/mcp_client.py`
- Implement connection pooling for efficiency
- Add comprehensive error handling
- Support async/await patterns

**Files/Components**:
- Update: `mcp-servers/project-management-automation/pyproject.toml`
- Create: `mcp-servers/project-management-automation/mcp_client.py`
- Create: `mcp-servers/project-management-automation/tests/test_mcp_client.py`

**Testing Requirements**:
- Test connection to each MCP server
- Test connection pooling
- Test error handling
- Test retry logic
- Verify async/await works correctly

**Dependencies**: None (foundation task)

---

### Task 2: Replace Todo2 File Access with Agentic-Tools MCP

**Priority**: High (9/10)
**Tags**: exarp, integration, agentic-tools, todo2

**Objective**: Replace all direct Todo2 file reads with agentic-tools MCP server calls

**Acceptance Criteria**:
- All Todo2 file reads replaced with agentic-tools MCP calls
- `todo2_alignment.py` uses agentic-tools MCP
- `duplicate_detection.py` uses agentic-tools MCP
- `nightly_task_automation.py` uses agentic-tools MCP
- `resources/tasks.py` uses agentic-tools MCP
- All tools work correctly with MCP integration

**Scope**:
- **Included:** Replace file reads, update all Todo2-using tools
- **Excluded:** New Todo2 features (separate task)
- **Clarification Required:** Migration strategy for existing code

**Technical Requirements**:
- Use MCP client to call agentic-tools MCP
- Replace `.todo2/state.todo2.json` reads with `list_todos` calls
- Replace file writes with `create_todos`/`update_todos` calls
- Maintain backward compatibility during transition
- Add fallback to file access if MCP fails

**Files/Components**:
- Update: `mcp-servers/project-management-automation/tools/todo2_alignment.py`
- Update: `mcp-servers/project-management-automation/tools/duplicate_detection.py`
- Update: `mcp-servers/project-management-automation/tools/nightly_task_automation.py`
- Update: `mcp-servers/project-management-automation/resources/tasks.py`
- Update: `mcp-servers/project-management-automation/tools/batch_task_approval.py`

**Testing Requirements**:
- Test all tools work with agentic-tools MCP
- Test error handling when MCP unavailable
- Test fallback to file access
- Verify task creation/updates work correctly
- Test with different Todo2 project IDs

**Dependencies**: Task 1 (MCP client infrastructure must be ready)

---

### Task 3: Replace Git Subprocess with Git MCP

**Priority**: High (8/10)
**Tags**: exarp, integration, git, mcp

**Objective**: Replace all subprocess git commands with git MCP server calls

**Acceptance Criteria**:
- All `subprocess` git calls replaced with git MCP
- `working_copy_health.py` uses git MCP
- `git_hooks.py` uses git MCP for validation
- Better error handling than subprocess
- Works even if git not in PATH

**Scope**:
- **Included:** Replace subprocess, update git-using tools
- **Excluded:** Git hook script generation (stays as-is)
- **Clarification Required:** Git MCP server availability

**Technical Requirements**:
- Use MCP client to call git MCP server
- Replace `git status`, `git branch`, `git log` subprocess calls
- Add better error handling
- Support async/await patterns
- Add fallback to subprocess if MCP unavailable

**Files/Components**:
- Update: `mcp-servers/project-management-automation/tools/working_copy_health.py`
- Update: `mcp-servers/project-management-automation/tools/git_hooks.py`
- Create: `mcp-servers/project-management-automation/tests/test_git_mcp.py`

**Testing Requirements**:
- Test git status via MCP
- Test git branch via MCP
- Test git log via MCP
- Test error handling
- Test fallback to subprocess
- Verify works without git in PATH

**Dependencies**: Task 1 (MCP client infrastructure must be ready)

---

### Task 4: Replace Filesystem Operations with Filesystem MCP

**Priority**: Medium (7/10)
**Tags**: exarp, integration, filesystem, mcp

**Objective**: Replace filesystem operations with filesystem MCP for better workspace awareness

**Acceptance Criteria**:
- All file read/write operations use filesystem MCP
- `docs_health.py` uses filesystem MCP
- `simplify_rules.py` uses filesystem MCP
- Better workspace awareness
- Consistent path resolution

**Scope**:
- **Included:** Replace pathlib/os operations, update file-using tools
- **Excluded:** Internal file operations (config files, etc.)
- **Clarification Required:** Which operations should use MCP

**Technical Requirements**:
- Use MCP client to call filesystem MCP
- Replace `pathlib` file reads with filesystem MCP
- Replace `pathlib` file writes with filesystem MCP
- Better workspace path resolution
- Add fallback to pathlib if MCP unavailable

**Files/Components**:
- Update: `mcp-servers/project-management-automation/tools/docs_health.py`
- Update: `mcp-servers/project-management-automation/tools/simplify_rules.py`
- Update: `mcp-servers/project-management-automation/tools/pattern_triggers.py`
- Create: `mcp-servers/project-management-automation/tests/test_filesystem_mcp.py`

**Testing Requirements**:
- Test file reads via MCP
- Test file writes via MCP
- Test workspace path resolution
- Test error handling
- Test fallback to pathlib
- Verify workspace awareness works

**Dependencies**: Task 1 (MCP client infrastructure must be ready)

---

### Task 5: Add Context7 MCP Integration

**Priority**: High (8/10)
**Tags**: exarp, integration, context7, documentation

**Objective**: Add actual Context7 MCP integration to verify external library documentation

**Acceptance Criteria**:
- Context7 verification step added to `check_documentation_health_tool`
- External library references verified via Context7
- `external_tool_hints.py` uses Context7 to verify hints
- Documentation currency checked
- API usage patterns validated

**Scope**:
- **Included:** Context7 integration, documentation verification
- **Excluded:** Context7 server setup (assumed configured)
- **Clarification Required:** Context7 search strategy

**Technical Requirements**:
- Use MCP client to call Context7 MCP
- Search for library documentation
- Verify external references in docs
- Check documentation currency
- Validate API usage patterns

**Files/Components**:
- Update: `mcp-servers/project-management-automation/tools/docs_health.py`
- Update: `mcp-servers/project-management-automation/tools/external_tool_hints.py`
- Create: `mcp-servers/project-management-automation/tools/context7_verification.py`
- Create: `mcp-servers/project-management-automation/tests/test_context7_mcp.py`

**Testing Requirements**:
- Test Context7 search for libraries
- Test documentation verification
- Test API usage validation
- Test error handling
- Verify integration with docs health check

**Dependencies**: Task 1 (MCP client infrastructure must be ready)

---

### Task 6: Add Tractatus Thinking MCP Integration

**Priority**: High (8/10)
**Tags**: exarp, integration, tractatus, structural-analysis

**Objective**: Add Tractatus Thinking MCP integration for structural analysis before running tools

**Acceptance Criteria**:
- `structural_analysis.py` wrapper created
- Tractatus analysis added before tools in `docs_health.py`
- Tractatus analysis added to `todo2_alignment.py`
- Problem structure understood programmatically
- Better tool recommendations based on structure

**Scope**:
- **Included:** Tractatus integration, structural analysis wrapper
- **Excluded:** Tractatus server setup (assumed configured)
- **Clarification Required:** When to use Tractatus analysis

**Technical Requirements**:
- Use MCP client to call Tractatus MCP
- Create structural analysis wrapper
- Integrate with existing tools
- Understand problem dependencies
- Provide better recommendations

**Files/Components**:
- Create: `mcp-servers/project-management-automation/tools/structural_analysis.py`
- Update: `mcp-servers/project-management-automation/tools/docs_health.py`
- Update: `mcp-servers/project-management-automation/tools/todo2_alignment.py`
- Create: `mcp-servers/project-management-automation/tests/test_tractatus_mcp.py`

**Testing Requirements**:
- Test Tractatus structural analysis
- Test integration with docs health
- Test integration with task alignment
- Test error handling
- Verify better recommendations

**Dependencies**: Task 1 (MCP client infrastructure must be ready)

---

### Task 7: Add Sequential Thinking MCP Integration

**Priority**: High (8/10)
**Tags**: exarp, integration, sequential, workflow

**Objective**: Add Sequential Thinking MCP integration to convert analysis results into implementation workflows

**Acceptance Criteria**:
- `workflow_generator.py` wrapper created
- Sequential workflow generation added after analysis in `docs_health.py`
- Sequential workflow added to `todo2_alignment.py`
- Analysis results converted into actionable steps
- Implementation workflows documented automatically

**Scope**:
- **Included:** Sequential integration, workflow generator wrapper
- **Excluded:** Sequential server setup (assumed configured)
- **Clarification Required:** Workflow format preferences

**Technical Requirements**:
- Use MCP client to call Sequential MCP
- Create workflow generator wrapper
- Integrate with existing tools
- Convert analysis into steps
- Document processes automatically

**Files/Components**:
- Create: `mcp-servers/project-management-automation/tools/workflow_generator.py`
- Update: `mcp-servers/project-management-automation/tools/docs_health.py`
- Update: `mcp-servers/project-management-automation/tools/todo2_alignment.py`
- Create: `mcp-servers/project-management-automation/tests/test_sequential_mcp.py`

**Testing Requirements**:
- Test Sequential workflow generation
- Test integration with docs health
- Test integration with task alignment
- Test error handling
- Verify actionable workflows created

**Dependencies**: Task 1 (MCP client infrastructure must be ready)

---

## Implementation Order

1. **Task 1** (MCP Client Infrastructure) - Foundation, no dependencies
2. **Task 2** (Agentic-Tools) - Depends on Task 1, highest impact
3. **Task 3** (Git MCP) - Depends on Task 1
4. **Task 4** (Filesystem MCP) - Depends on Task 1
5. **Task 5** (Context7) - Depends on Task 1
6. **Task 6** (Tractatus) - Depends on Task 1
7. **Task 7** (Sequential) - Depends on Task 1

---

## Dependencies Graph

```
Task 1 (MCP Infrastructure)
    ↓
    ├──→ Task 2 (Agentic-Tools)
    ├──→ Task 3 (Git MCP)
    ├──→ Task 4 (Filesystem MCP)
    ├──→ Task 5 (Context7)
    ├──→ Task 6 (Tractatus)
    └──→ Task 7 (Sequential)
```

---

## Success Metrics

### Task 1: Infrastructure
- ✅ MCP client wrapper created
- ✅ Connection pooling working
- ✅ Error handling comprehensive
- ✅ All MCP servers connectable

### Task 2: Agentic-Tools
- ✅ All Todo2 file reads replaced
- ✅ All tools work with MCP
- ✅ Better error handling
- ✅ Access to advanced features

### Task 3: Git MCP
- ✅ All subprocess calls replaced
- ✅ Better error handling
- ✅ Works without git in PATH
- ✅ Access to advanced git features

### Task 4: Filesystem MCP
- ✅ All file operations use MCP
- ✅ Better workspace awareness
- ✅ Consistent path resolution
- ✅ Access to filesystem MCP features

### Task 5: Context7
- ✅ Documentation verification working
- ✅ External references validated
- ✅ API usage patterns checked
- ✅ Integration with docs health

### Task 6: Tractatus
- ✅ Structural analysis integrated
- ✅ Better tool recommendations
- ✅ Problem structure understood
- ✅ Integration with multiple tools

### Task 7: Sequential
- ✅ Workflow generation working
- ✅ Analysis converted to steps
- ✅ Implementation workflows created
- ✅ Integration with multiple tools

---

## Risk Assessment

### High Risk
- **Task 1**: MCP client library complexity
- **Task 2**: Breaking changes to Todo2 integration

### Medium Risk
- **Task 3-7**: MCP server availability
- **All Tasks**: Performance with multiple MCP connections

### Mitigation
- Comprehensive error handling
- Fallback to existing methods
- Connection pooling
- Extensive testing

---

P25-12-25
